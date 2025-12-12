def save_report(text: str, out_path: str | None) -> str:
    if out_path is None:
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        out_path = f"dice_log_{ts}.txt"
    with open(out_path, "W", encoding = "utf-8") as f:
        f.write(text)
    return out_path
