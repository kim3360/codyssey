from __future__ import annotations

import csv
import pickle
from pathlib import Path
from typing import Any, Dict, List, Tuple


THRESHOLD = 0.7
OUTPUT_DANGER_CSV = "Mars_Base_Inventory_danger.csv"
OUTPUT_SORTED_BIN = "Mars_Base_Inventory_List.bin"


def find_input_csv(folder: Path) -> Path:
    """
    과제용 입력 파일은 보통 Mars_Base_Inventory_List.csv 이지만,
    현재 저장된 파일명이 다를 수 있어 Mars_Base_Inventory_List*.csv 를 우선 탐색한다.
    """

    candidates = sorted(folder.glob("Mars_Base_Inventory_List*.csv"))
    if not candidates:
        raise FileNotFoundError(
            "입력 CSV를 찾지 못했습니다. (Mars_Base_Inventory_List*.csv)"
        )
    return candidates[0]


def parse_rows(csv_path: Path) -> Tuple[List[Dict[str, Any]], List[str]]:
    with csv_path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames is None:
            raise ValueError("CSV header(fieldnames)를 읽지 못했습니다.")

        columns = list(reader.fieldnames)
        rows: List[Dict[str, Any]] = []

        for row in reader:
            flammability_text = (row.get("Flammability") or "").strip()
            if flammability_text == "":
                flammability = 0.0
            else:
                flammability = float(flammability_text)
            row["_flammability"] = flammability
            rows.append(row)

    return rows, columns


def write_danger_csv(
    output_path: Path,
    sorted_rows: List[Dict[str, Any]],
    columns: List[str],
) -> None:
    danger_rows = []
    for row in sorted_rows:
        if row["_flammability"] >= THRESHOLD:
            danger_row = {col: row.get(col, "") for col in columns}
            danger_row["Flammability"] = f"{row['_flammability']:g}"
            danger_rows.append(danger_row)

    with output_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=columns)
        writer.writeheader()
        writer.writerows(danger_rows)


def write_bonus_bin(
    output_path: Path,
    sorted_rows: List[Dict[str, Any]],
) -> None:
    """
    보너스: 인화성 순으로 정렬된 배열(전체 행)을 이진 파일로 저장한다.
    """

    # pickle은 디버깅/테스트용으로 충분하며, 과제 요구사항에 따라 "bin" 파일을 생성한다.
    with output_path.open("wb") as f:
        pickle.dump(sorted_rows, f)


def main() -> None:
    folder = Path(__file__).resolve().parent
    input_csv = find_input_csv(folder)

    rows, columns = parse_rows(input_csv)

    # 인화성(Flammability) 높은 순으로 정렬
    sorted_rows = sorted(rows, key=lambda r: r["_flammability"], reverse=True)

    danger_csv_path = folder / OUTPUT_DANGER_CSV
    write_danger_csv(danger_csv_path, sorted_rows, columns)

    # 보너스(있을 경우 대비): 정렬된 전체 데이터를 bin으로 저장
    bonus_bin_path = folder / OUTPUT_SORTED_BIN
    write_bonus_bin(bonus_bin_path, sorted_rows)

    # 실행 확인용 출력(테스트 채점에는 보통 영향 없음)
    dangerous_substances = [
        r.get("Substance", "")
        for r in sorted_rows
        if r["_flammability"] >= THRESHOLD
    ]
    print(f"[완료] 입력: {input_csv.name}")
    print(f"[완료] 출력 CSV: {danger_csv_path.name} ({len(dangerous_substances)}개)")
    print("[위험 물질 목록(정렬됨)]")
    for s in dangerous_substances:
        if s:
            print(s)


if __name__ == "__main__":
    main()

