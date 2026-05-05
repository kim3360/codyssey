# 문제7 살아난 미션 컴퓨터

`mars_mission_computer.py`는 화성 기지 환경 센서값을 주기적으로 수집하고 출력하는 프로그램입니다.

## 파일 구성

- `mars_mission_computer.py`: 문제7 수행 코드
- `README.md`: 실행 방법 및 코드 설명

## 요구사항 반영 내용

- `MissionComputer` 클래스 구현
- `env_values` 딕셔너리로 6개 환경 데이터 관리
- `DummySensor`를 `ds` 이름으로 인스턴스화
- `get_sensor_data()`에서 센서값 수집 후 JSON 형태로 출력
- 5초 주기로 반복 출력
- 전체 파일명을 `mars_mission_computer.py`로 작성

## 보너스 반영

- 콘솔에서 `q` 입력 시 루프 중지
- 중지 시 `System stoped...` 출력
- 최근 5분 수집 데이터 평균값 출력 기능 포함

## 코드 동작 구조

### 1) `DummySensor`

- `set_env()`
  - `random.uniform()`으로 아래 범위의 더미 값을 생성합니다.
    - 내부 온도: 18 ~ 30
    - 외부 온도: 0 ~ 21
    - 내부 습도: 50 ~ 60
    - 외부 광량: 500 ~ 715
    - 내부 CO2: 0.02 ~ 0.1
    - 내부 O2: 4 ~ 7
- `get_env()`
  - 현재 환경값 사본(dict copy) 반환

### 2) `MissionComputer`

- `__init__()`
  - `env_values` 초기화
  - `self.ds = DummySensor()` 생성
  - 정지 플래그, 5분 샘플 저장소, 마지막 평균 출력 시각 초기화

- `_wait_for_stop_key()`
  - 별도 스레드에서 사용자 입력 감시
  - `q` 입력 시 `_should_stop = True`

- `_print_five_minute_average()`
  - 최근 5분 샘플의 항목별 평균 계산
  - JSON 형식으로 출력

- `get_sensor_data()`
  - 정지 키 감시 스레드 시작
  - 반복 루프에서 센서값 갱신/출력
  - `(수집시각, 데이터)` 형태로 샘플 저장
  - 최근 5분 데이터만 유지
  - 5분마다 평균 출력
  - 5초 간격 유지
  - 종료 시 `System stoped...` 출력

## 실행 방법

문제7 폴더에서 아래 명령어를 실행합니다.

```bash
python3 mars_mission_computer.py
```

종료하려면 콘솔에 `q`를 입력하고 Enter를 누릅니다.

## 개발 환경

- Python 3.x
- 표준 라이브러리만 사용 (`json`, `random`, `threading`, `time`)
