# 문제5 내일 날씨는 맑음

이미지 요구사항에 맞춰 MySQL에 화성 날씨 데이터를 적재하고, 결과를 PNG 이미지로 저장하는 코드를 작성했습니다.

## 파일 구성

- `mars_weather_summary.py`: 테이블 생성, CSV 적재, 요약 PNG 생성
- `README.md`: 실행 방법과 요구사항 반영 내용

## 수행과제 반영

- MySQL 연동 코드 구현
- `mars_weather` 테이블 자동 생성
  - `weather_id INT AUTO_INCREMENT PRIMARY KEY`
  - `mars_date DATETIME UNIQUE`
  - `temp INT`
  - `storm INT`
- `mars_weathers_data.csv`를 읽어 데이터 입력
  - 각 행을 INSERT로 처리
  - 중복 날짜는 `ON DUPLICATE KEY UPDATE`로 갱신
- 결과 그래프를 `mars_weather_summary.png`로 저장

## 제약사항/보너스 반영

- Python 코드 스타일(함수 snake_case, 클래스 CapWord) 준수
- 보너스: `MySQLHelper` 클래스로 DB 연결/쿼리 로직을 분리

## 필요 라이브러리

```bash
pip install mysql-connector-python matplotlib
```

## 실행 방법

1. MySQL에서 `mars` 데이터베이스를 미리 생성합니다.
2. `mars_weathers_data.csv`를 같은 폴더에 둡니다.
3. `mars_weather_summary.py`의 DB 접속 정보(`user`, `password`, `database`)를 환경에 맞게 수정합니다.
4. 실행합니다.

```bash
python3 mars_weather_summary.py
```

실행 후 같은 폴더에 `mars_weather_summary.png`가 생성됩니다.
