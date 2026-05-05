# 문제8 불안정한 미션 컴퓨터

이미지 요구사항을 기준으로 `MissionComputer` 클래스에 시스템 정보/부하 조회 기능을 구현했습니다.

## 파일 구성

- `mars_mission_computer.py`: 문제8 구현 코드
- `setting.txt`: 보너스 과제용 출력 항목 설정 파일
- `README.md`: 실행 방법 및 코드 설명

## 수행 과제 반영

- `MissionComputer` 클래스에 아래 메서드를 구현했습니다.
  - `get_mission_computer_info()`
  - `get_mission_computer_load()`
- `get_mission_computer_info()`는 다음 정보를 JSON으로 출력합니다.
  - 운영체계
  - 운영체계 버전
  - CPU 타입
  - CPU 코어 수
  - 메모리 크기(GB)
- `get_mission_computer_load()`는 다음 정보를 JSON으로 출력합니다.
  - CPU 실시간 사용량(%)
  - 메모리 실시간 사용량(%)
- `if __name__ == '__main__'`에서 `runComputer` 인스턴스를 만들고
  - `get_mission_computer_info()`
  - `get_mission_computer_load()`
  를 순서대로 호출합니다.
- 최종 파일명은 요구대로 `mars_mission_computer.py`입니다.

## 제약사항 반영

- 기본은 표준 라이브러리(`json`, `os`, `platform`, `subprocess`)를 사용했습니다.
- 시스템 정보/부하 조회는 `psutil`이 있으면 우선 사용하고, 없으면 표준 라이브러리 기반으로 대체 조회합니다.
- 시스템 정보/부하 조회는 모두 예외 처리되어, 실패 시에도 프로그램이 중단되지 않고 안전하게 출력합니다.

## 보너스 과제 반영 (`setting.txt`)

`setting.txt`에 키 이름을 적으면 해당 항목만 출력합니다.

예시:

```txt
operating_system
cpu_core_count
cpu_usage_percent
```

- 빈 줄, `#` 주석 줄은 무시됩니다.
- `setting.txt`가 없거나 유효 항목이 없으면 전체 항목을 출력합니다.

## 실행 방법

문제8 폴더에서 실행:

```bash
python3 mars_mission_computer.py
```
