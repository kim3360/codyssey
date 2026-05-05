# 문제4 계산기의 핵심코어 제작

이미지의 요구사항에 맞춰 계산기 핵심 로직을 `calculator.py`로 구현했습니다.

## 파일 구성

- `calculator.py`: `Calculator` 클래스 기반 계산기 핵심 코어
- `README.md`: 요구사항 반영 및 사용 설명

## 수행과제 반영

- `Calculator` 클래스 구현
- 사칙연산 메서드 구현
  - `add()`
  - `subtract()`
  - `multiply()`
  - `divide()`
- 추가 기능 메서드 구현
  - `reset()`
  - `negative_positive()`
  - `percent()`
- 숫자 누적 입력 구현
  - `press_digit(digit)`
- 소수점 입력 구현
  - `press_decimal()`
  - 이미 소수점이 있으면 추가 입력되지 않음
- 결과 출력 메서드 구현
  - `equal()`
  - 화면 출력값은 `display_value()`로 확인

## 제약사항 반영

- Python 3.x 기준
- 표준 라이브러리만 사용 (`decimal`)
- 경고 없이 실행 가능
- 수학 예외 처리 포함
  - 0으로 나누기 시 `Error`
  - 연산 중 예외 시 `Error`

## 보너스 반영

- 결과값 소수점이 6자리를 초과하면 소수점 6자리에서 반올림
- 화면 출력용 문자열은 천 단위 구분기호(콤마) 적용

## 간단 사용 예시

```python
from calculator import Calculator

calc = Calculator()
calc.press_digit('1')
calc.press_digit('2')
calc.add()
calc.press_digit('3')
calc.equal()

print(calc.display_value())  # 15
```
