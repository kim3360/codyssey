# 로그 분석 보고서 (mission_computer_main.log)

## 1. Python 개발 도구 선택 및 설치

로그 분석을 위해 로컬에서 Python 실행 환경을 준비했다.

대표적으로 아래 도구들을 비교할 수 있다.

- **VS Code + Python 확장**: 가볍고 프로젝트 폴더 기준 실행이 쉬움, 확장 기능으로 디버깅/가상환경 관리가 편리함
- **PyCharm**: 전용 IDE로 Python 생산성이 좋지만 상대적으로 무거울 수 있음
- **Jupyter Notebook**: 데이터 분석/시각화에 강하지만, 과제용 단일 스크립트 구현에는 불편할 수 있음

본 과제에서는 **VS Code + Python(확장)** 조합을 기준으로 개발/실행했다. (사용한 IDE/환경이 다르면 문서의 문장만 조정하면 된다.)

## 2. 설치 확인: `Hello Mars` 출력

`main.py` 실행 시 다음을 출력해 설치가 정상 동작함을 확인했다.

```text
Hello Mars
```

## 3. 로그 파일 로딩 및 전체 출력

`mission_computer_main.log`는 `timestamp,event,message` 형태의 CSV 로그이며, 프로그램은 다음을 수행한다.

1. 로그 파일을 열어 **전체 내용을 화면에 출력**
2. CSV 헤더(`timestamp,event,message`)를 기준으로 파싱
3. 파싱된 로그를 시간순 정렬 후 분석

## 4. 예외 처리

파일 처리 및 파싱 과정에서 발생할 수 있는 대표 예외를 `main.py`에서 처리한다.

- `FileNotFoundError`: 로그 파일 경로가 존재하지 않을 때
- `UnicodeDecodeError`: 인코딩 문제로 읽기 실패할 때
- `csv.Error`: CSV 파싱 중 오류가 발생할 때
- `ValueError`: 날짜/시간 포맷 변환 실패 등 데이터 형식 문제가 있을 때
- 그 외 예외: 예상치 못한 런타임 오류 fallback

## 5. 사고 원인 분석

사고 원인은 `mission_computer_main.log`의 메시지 내용에서 **직전 징후(unstable)와 사고 이벤트(explosion)의 관계**를 규칙 기반으로 추정하여 분석했다.

### 5-1. 분석 규칙(로직)

`main.py`의 분석 로직은 다음과 같다.

1. 로그의 각 행을 `timestamp` 기준으로 정렬한다. (시간 순 분석을 위해)
2. `message`에 `explosion`이 포함된 행들을 사고(폭발) 이벤트로 수집한다.
3. 각 폭발 이벤트의 발생 시각을 `T`라고 할 때, `T - lookback(기본 60분)` ~ `T` 구간에서 `unstable`이 포함된 행만 후보로 추린다.
4. 폭발 이벤트 문장과 `unstable` 문장에서 대상이 동일한지를 최대한 맞추기 위해, 문장에서 아래처럼 “대상명”을 추출한다.
   - `Oxygen tank explosion.` → 대상 `Oxygen tank`
   - `Oxygen tank unstable.` → 대상 `Oxygen tank`
5. 위 조건을 만족하는 `unstable` 후보가 여러 개면, 그 중 **가장 최근(timestamp가 가장 큰 값)** 을 사고 원인 후보로 선택한다.

이 과정을 폭발 이벤트마다 반복하여 “사고 원인(한 줄 요약)”을 생성한다.

### 5-2. 로그 기반 결론(해석 근거)

로그에서 폭발 이벤트와 직전 징후가 다음과 같이 관측된다.

- `2023-08-27 11:35:00` `INFO` : `Oxygen tank unstable.`
- `2023-08-27 11:40:00` `INFO` : `Oxygen tank explosion.`

따라서 **산소 탱크(Oxygen tank)가 불안정해진 징후(unstable)가 폭발(explosion)로 이어진 것으로 해석**했다.

또한 두 이벤트 사이 시간 차는 다음과 같다.

- `11:35:00` → `11:40:00` = 약 **300초 전**

`main.py` 실행 결과(요약 출력 포맷) 기준으로는 아래 형태로 보고된다.

- `사고원인(한 줄 요약): Oxygen tank 불안정(2023-08-27 11:35:00)이(가) 폭발(2023-08-27 11:40:00)로 이어짐. (약 300초 전)`

### 5-3. 사용한 주요 코드

사고 원인 추정은 `main.py`의 규칙 기반 로직으로 구현했다.

#### (1) 문장(메시지)에서 대상 추출: `extract_subject()`

```python
def extract_subject(message: str, trigger_word: str) -> Optional[str]:
    # "Oxygen tank unstable."  -> "Oxygen tank"
    # "Oxygen tank explosion." -> "Oxygen tank"
    msg = (message or "").strip()
    pattern = r"^(.*?)\s+" + re.escape(trigger_word) + r"\b\.?\s*$"
    m = re.match(pattern, msg, flags=re.IGNORECASE)
    return m.group(1).strip() if m else None
```

#### (2) 폭발별로 직전 `unstable` 후보 찾기 및 최신 선택: `analyze_accident()`

```python
def analyze_accident(rows: list[LogRow], lookback_minutes: int = 60) -> list[str]:
    results: list[str] = []
    # rows는 timestamp 기준으로 정렬되어 있으므로 exp 시간 이전까지만 확인한다.
    for exp in rows:
        if "explosion" not in exp.message.lower():
            continue

        exp_time = exp.timestamp
        window_start = exp_time - timedelta(minutes=lookback_minutes)
        explosion_subject = extract_subject(exp.message, "explosion")

        # 후보 리스트 대신 "가장 최근 unstable 1개"만 저장
        latest_candidate = None

        for r in rows:
            # window_start보다 이전이면 볼 필요 없음
            if r.timestamp < window_start:
                continue
            # exp_time 이상이면 더 볼 필요 없음(정렬되어 있으므로 종료)
            if r.timestamp >= exp_time:
                break
            if "unstable" not in r.message.lower():
                continue

            unstable_subject = extract_subject(r.message, "unstable")
            if explosion_subject and unstable_subject:
                if unstable_subject.lower() != explosion_subject.lower():
                    continue

            # 가장 최근 unstable 갱신
            if latest_candidate is None or r.timestamp > latest_candidate.timestamp:
                latest_candidate = r

        if latest_candidate is None:
            results.append(
                f"사고원인(한 줄 요약): 폭발({exp_time}) 직전 {lookback_minutes}분 내 unstable 징후를 찾지 못함."
            )
            continue

        diff_sec = int((exp_time - latest_candidate.timestamp).total_seconds())
        subject = explosion_subject or extract_subject(latest_candidate.message, "unstable") or "Unknown"
        results.append(
            f"사고원인(한 줄 요약): {subject} 불안정({latest_candidate.timestamp})이(가) 폭발({exp_time})로 이어짐. (약 {diff_sec}초 전)"
        )

    return results
```

## 6. 재현 방법

프로젝트 폴더(코테)에서 아래 명령을 실행한다.

```bash
python3 main.py
```

실행하면 로그 전체 출력과 함께 사고원인 분석 결과(한 줄 요약)가 화면에 출력된다.
