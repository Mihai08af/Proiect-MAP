def ascii_histogram(counts: Dict[int, int], width: int = 30) -> str:
    if not counts:
        return "(Niciun punct de date)"
max_count = max(counts.values()) or 1
lines = []
for face in sorted(counts):
    cnt = counts[face]
    bar_len = int(round(cnt / max_count * width))
    bar = "*" * bar_len if bar_len > 0 else ""
    lines.append(f"{face:>2}: {cnt:>6} {bar}")
return "\n".join(lines)
