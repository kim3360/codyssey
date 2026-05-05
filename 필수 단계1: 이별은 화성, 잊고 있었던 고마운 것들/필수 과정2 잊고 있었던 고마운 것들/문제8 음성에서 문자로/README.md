# 문제8 음성에서 문자로

문제7의 녹음 파일(`records/*.wav`)을 STT로 텍스트 변환하고, 결과를 CSV 파일로 저장하는 코드입니다.

## 파일 구성

- `jarvis.py`: 음성 → 텍스트(STT) 변환 및 CSV 저장
- `README.md`: 요구사항 반영 내용과 실행 방법

## 수행과제 반영

- 문제7에서 녹음된 음성파일 목록을 출력
- 각 음성파일에 대해 STT를 수행하고 인식 결과 확인
- 음성파일별 CSV 저장
  - 파일명: 원본 음성과 같은 이름 + `.csv`
  - 저장 항목: `time`, `recognized_text`
- 전체 내용은 `jarvis.py`에 구현

## 제약사항 반영

- 표준 라이브러리 사용: `csv`, `datetime`, `pathlib`
- STT 부분은 외부 라이브러리 사용 가능 조건에 맞춰 `speech_recognition` 사용
- 함수/메서드 이름은 snake_case 사용
- 클래스 이름은 CapWord 사용 (`JarvisStt`)
- 예외 처리 포함
  - 라이브러리 미설치
  - STT 인식 실패
  - 폴더 내 녹음 파일 없음

## 보너스 과제 반영

- 키워드 입력 시, 저장된 CSV 파일 전체에서 해당 단어를 검색해 출력

## 실행 방법

1. 의존성 설치

```bash
pip install SpeechRecognition
```

2. `records` 폴더에 `.wav` 파일 준비 (문제7 결과물)

3. 실행

```bash
python3 jarvis.py
```

4. (선택) 키워드 입력 시 CSV 파일 내 검색 결과를 출력
