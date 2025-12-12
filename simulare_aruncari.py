def simulate_simple_rolls(faces: int, rolls: int, seed: int | None) -> Tuple[Counter, List[int]]:
    set_seed(seed)
    results = roll_many(rolls, faces)
    counts = Counter(results)
    return counts, results

def summarise_rolls(faces: int, rolls: int, counts: Counter, samples: List[int]) -> str:
    total = rolls
    lines = []
    lines.append(f"Simulare completa: {rolls} aruncari cu zar de {faces} fete")
    lines.append("")

    for face in range(1, faces + 1):
        cnt = counts.get(face, 0)
        pct = (cnt * 100.0 / total) if total else 0.0
        lines.append(f"{face:>2}: {cnt:>6} ({pct:5.2f}%)")

    lines.append("")
    lines.append("Histograma (ASCII):")
    hist_counts = {f: counts.get(f, 0) for f in range(1, faces + 1)}
    lines.append(ascii_histogram(hist_counts, width=30))

    lines.append("")
    mean, median, stdev = basic_stats(samples)
    lines.append(f"Medie: {mean:.2f}")
    lines.append(f"Mediana: {median:.2f}")
    lines.append(f"Deviatie standard: {stdev:.2f}")

    return "\n".join(lines)
