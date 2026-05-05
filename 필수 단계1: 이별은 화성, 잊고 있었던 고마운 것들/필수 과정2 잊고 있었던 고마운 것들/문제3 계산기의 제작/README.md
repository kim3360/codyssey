# 문제3 계산기의 제작

Python 3와 **표준 라이브러리**로 계산 로직을 만들고, 화면은 **PyQt6**로 구성한 미니 계산기입니다.

## 폴더 구성

| 파일 | 역할 |
|------|------|
| `calculator.py` | 계산만 담당하는 `Calculator` 클래스 (PyQt 없음) |
| `main.py` | 창·버튼·표시줄 등 **UI**와 실행 진입점 |
| `README.md` | 이 문서 |

로직과 화면을 나누면, 과제에서 요구하는 **핵심 클래스**를 `calculator.py`에 두기 쉽고, UI만 바꾸거나 로직만 단독 테스트하기도 좋습니다.

## 실행 방법

이 폴더에서:

```bash
pip install PyQt6
python3 main.py
```

## `calculator.py` — `Calculator` 클래스

### 상태 변수(내부)

- `_entry`: 지금 입력 중인 수를 나타내는 **문자열** (예: `'123'`, `'3.14'`).
- `_stored`: 연산의 **왼쪽 피연산자** (이전에 확정한 값).
- `_pending_op`: 아직 `=` 로 끝나지 않은 연산 종류 (`'add'`, `'subtract'`, `'multiply'`, `'divide'`).
- `_fresh`: 직전에 연산자를 눌렀는지 여부. `True`이면 다음 숫자가 **새 수**로 시작합니다.
- `_error`: 0으로 나누기 등으로 **Error** 상태인지 여부.
- `_last_pretty`: `=` 직후 화면에 `12 + 3 = 15`처럼 **한 줄 수식**을 잠시 보여 주기 위한 문자열.

### 연산 구현

- `_BINOPS`: `operator.add` 등으로 사칙연산을 묶어 두고, `Decimal`끼리 계산합니다.
- `getcontext().prec = 40`으로 중간 계산 자릿수를 넉넉히 잡습니다.

### 주요 메서드

| 메서드 | 설명 |
|--------|------|
| `reset()` | 전부 초기화 (AC에 해당). |
| `clear_entry()` | 지금 치고 있던 수만 0으로 (C). 진행 중인 연산은 유지. |
| `is_ac_label()` | 버튼에 `AC`를 쓸지 `C`를 쓸지 판단. |
| `display_value()` | 화면에 그릴 **한 줄 문자열**. 천 단위 콤마, 연산자 표시, `=` 결과 줄 포함. |
| `press_digit` / `press_decimal` | 숫자·소수점 입력 (소수점은 한 수에 하나만). |
| `add` / `subtract` / `multiply` / `divide` | 연산자 선택·이어 계산(체인). |
| `negative_positive()` | 부호 반전. |
| `percent()` | 현재 값을 100으로 나눔. |
| `equal()` | `=` 실행. 오류 시 `Error` 처리. |

### 표시·예외

- `_format_with_commas`: 정수 부분에 **천 단위 콤마**를 넣습니다.
- `_format_result_for_output`: 소수 아래가 **7자리 넘으면** 소수 **6자리**에서 반올림 후 문자열로 만듭니다.
- `ZeroDivisionError`, `InvalidOperation`, `OverflowError` 등은 잡아서 `Error` 상태로 둡니다.

## `main.py` — PyQt 창

- `CalculatorWindow`: `QVBoxLayout`으로 **표시 영역**과 **버튼 그리드**를 쌓습니다.
- `specs` 리스트에 버튼 글자, 격자 위치, 역할(`ac`, `sign`, `add` …), 배경색을 정의하고, 반복문으로 `QPushButton`을 만들어 연결합니다.
- `partial(self._tap_op, 'add')`처럼 **연산자 이름**을 넘겨 `Calculator`의 같은 이름 메서드를 호출합니다.
- `_sync()`: `Calculator.display_value()`를 읽어 라벨에 올리고, **AC/C** 문구를 갱신합니다.
- `_fit_display_font`: 글자가 길면 글자 크기를 줄여서 **한 줄에 들어가게** 맞춥니다 (보너스에 가까운 동작).

## 의존성

- **필수 (UI 실행)**: PyQt6 (`pip install PyQt6`)
- **로직만**: `calculator.py`는 표준 라이브러리만 사용합니다.
