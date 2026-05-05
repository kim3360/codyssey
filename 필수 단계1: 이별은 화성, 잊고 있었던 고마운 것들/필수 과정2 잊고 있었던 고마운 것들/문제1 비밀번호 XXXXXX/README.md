# 문제1 비밀번호 XXXXXX

이미지의 요구사항에 맞춰 zip 암호를 브루트포스(무차별 대입)로 찾는 코드를 작성했습니다.

## 파일 구성

- `door_hacking.py`: 암호 해제 코드
- `README.md`: 요구사항 정리 및 실행 방법

## 수행과제 반영

- `unlock_zip()` 함수 구현
- 대상 zip 파일명: `emergency_storage_key.zip` (기본값)
- 암호 후보 규칙: 소문자 + 숫자 조합의 6자리
- 암호 해제 시작 시간/종료 시간/소요 시간 출력
- 암호 발견 시 `password.txt` 파일에 저장
- 전체 코드를 `door_hacking.py`로 저장

## 제약사항 반영

- Python 3.x
- 표준 라이브러리만 사용
  - `itertools`, `string`, `time`, `zipfile`, `pathlib`
- 파일 처리 예외 대응
  - zip 파일 없음
  - 손상된 zip 파일
  - 해제 실패 반복

## 보너스 반영

- 일정 주기(`progress_step`)마다 시도 횟수와 현재 후보 비밀번호를 출력
  - 기본값: 10,000회마다 로그 출력

## 실행 방법

1. `emergency_storage_key.zip` 파일을 같은 폴더에 둡니다.
2. 아래 명령어로 실행합니다.

```bash
python3 door_hacking.py
```

3. 성공 시:
   - 콘솔에 비밀번호 출력
   - `password.txt`에 비밀번호 저장

## 참고

- 경우의 수는 `36^6 = 2,176,782,336` 이므로 실제 해제 시간은 길 수 있습니다.
- 필요하면 `unlock_zip(progress_step=5000)`처럼 진행 로그 주기를 조정할 수 있습니다.
