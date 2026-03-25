LOG_FILENAME = "mission_computer_main.log"


def to_seconds(timestamp_text):
    # "2023-08-27 11:35:00" -> 초(기준일 00:00:00부터 경과 초)
    # 날짜는 동일하다는 가정으로 시:분:초만 사용
    time_part = timestamp_text.split(" ")[1]
    h, m, s = time_part.split(":")
    return int(h) * 3600 + int(m) * 60 + int(s)


def parse_csv_lines(log_text):
    # CSV를 최소한으로 파싱한다. (timestamp,event,message)
    lines = [line.strip() for line in log_text.splitlines() if line.strip()]
    if not lines:
        return []
    # 첫 줄은 header
    body = lines[1:]
    rows = []
    for line in body:
        parts = line.split(",", 2)  # message에 콤마가 있어도 3덩어리만 분리
        if len(parts) < 3:
            continue
        timestamp, event, message = parts[0], parts[1], parts[2]
        rows.append(
            {
                "timestamp": timestamp,
                "event": event,
                "message": message,
                "seconds": to_seconds(timestamp),
            }
        )
    rows.sort(key=lambda x: x["seconds"])
    return rows


def extract_subject(message, trigger_word):
    # "Oxygen tank unstable." -> "Oxygen tank"
    # "Oxygen tank explosion." -> "Oxygen tank"
    msg = (message or "").strip()
    lowered = msg.lower()
    trigger = trigger_word.lower()

    # trigger 위치를 찾아 그 앞부분을 subject로 사용
    idx = lowered.rfind(" " + trigger)
    if idx == -1:
        # 문장 맨 앞이 trigger인 경우 등 예외
        if lowered.startswith(trigger):
            return ""
        return None

    subject = msg[:idx].strip()
    if subject.endswith("."):
        subject = subject[:-1].strip()
    return subject if subject else None


def analyze_accident(rows, lookback_minutes=60):
    results = []
    lookback_seconds = lookback_minutes * 60

    for exp in rows:
        if "explosion" not in exp["message"].lower():
            continue

        exp_seconds = exp["seconds"]
        window_start = exp_seconds - lookback_seconds
        explosion_subject = extract_subject(exp["message"], "explosion")

        latest_candidate = None
        for r in rows:
            if r["seconds"] < window_start:
                continue
            if r["seconds"] >= exp_seconds:
                break
            if "unstable" not in r["message"].lower():
                continue

            unstable_subject = extract_subject(r["message"], "unstable")
            if explosion_subject and unstable_subject:
                if unstable_subject.lower() != explosion_subject.lower():
                    continue

            latest_candidate = r

        if latest_candidate is None:
            results.append(
                f"사고원인(한 줄 요약): 폭발({exp['timestamp']}) 직전 {lookback_minutes}분 내 unstable 징후를 찾지 못함."
            )
            continue

        diff_sec = exp_seconds - latest_candidate["seconds"]
        subject = (
            explosion_subject
            or extract_subject(latest_candidate["message"], "unstable")
            or "Unknown"
        )
        results.append(
            f"사고원인(한 줄 요약): {subject} 불안정({latest_candidate['timestamp']})이(가) 폭발({exp['timestamp']})로 이어짐. (약 {diff_sec}초 전)"
        )

    return results


def main():
    print("Hello Mars")

    try:
        with open(LOG_FILENAME, "r", encoding="utf-8") as f:
            log_text = f.read()
    except FileNotFoundError:
        print(f"오류: 로그 파일을 찾지 못했습니다. 파일명: {LOG_FILENAME}")
        return
    except UnicodeDecodeError:
        print("오류: 로그 파일 인코딩이 UTF-8이 아닙니다.")
        return

    print("\n[mission_computer_main.log - 전체 내용 출력]\n")
    print(log_text)

    try:
        rows = parse_csv_lines(log_text)
        summaries = analyze_accident(rows, lookback_minutes=60)
    except Exception as e:
        print(f"오류: 로그 분석 중 문제가 발생했습니다. ({e})")
        return

    print("\n[사고원인 분석 결과]\n")
    for line in summaries:
        print(line)


if __name__ == "__main__":
    main()

