# 문제2 카이사르의 암호

`password.txt`의 암호문을 카이사르 방식으로 해독해 `result.txt`로 저장하는 코드입니다.

## 파일 구성

- `caesar_cipher.py`: 해독 코드
- `README.md`: 요구사항 및 실행 방법

## 수행과제 반영

- `password.txt`를 읽어 암호문을 가져옵니다.
- `caesar_cipher_decode(target_text)` 함수를 구현했습니다.
- 쉬프트(0~25)를 바꿔가며 해독 결과를 반복 출력합니다.
- 사용자가 번호를 입력해 최종 결과를 선택할 수 있습니다.
- 선택한 결과를 `result.txt`에 저장합니다.

## 제약사항 반영

- Python 표준 라이브러리만 사용
  - `string`, `pathlib`
- 경고 없이 실행 가능하도록 예외 처리 포함
  - `password.txt` 없음
  - `password.txt` 비어 있음
  - 잘못된 번호 입력

## 보너스 반영

- 간단한 사전(`DICTIONARY_WORDS`)을 두고,
- 해독 결과에 키워드가 발견되면 반복을 중단할 수 있도록 구현했습니다.

## 실행 방법

1. 같은 폴더에 `password.txt`를 둡니다.
2. 아래 명령어를 실행합니다.

```bash
python3 caesar_cipher.py
```

3. 출력된 결과 번호 중 하나를 입력합니다.
4. 최종 해독문은 `result.txt`에 저장됩니다.
