import argparse
import random
import statistics
from collections import Counter
from datetime import datetime
from typing import List, Dict, Tuple

def set_seed(seed: int | None):
    if seed is not None:
        random.seed(seed)

def roll_dice(faces: int) -> int:
    return random.randint(1, faces)

def roll_dices(dice: int, faces: int) -> List[int]:
    return [roll_dice(faces) for _ in range(dice)]

def roll_many(rolls: int, faces: int) -> List[int]:
    return [roll_dice(faces) for _ in range(rolls)]

def ascii_histogram(counts: Dict[int, int], width: int = 30) -> str:
    if not counts:
        return "(Niciun punct de date)"

    max_count = max(counts.values()) or 1
    lines = []
    for face in sorted(counts):
        cnt = counts[face]
        bar_len = int(round(cnt / max_count * width))
        bar = "*" * bar_len
        lines.append(f"{face:>2}: {cnt:>6} {bar}")
    return "\n".join(lines)

def basic_stats(samples: List[int]) -> Tuple[float, float, float]:
    mean = statistics.fmean(samples)
    median = statistics.median(samples)
    stdev = statistics.pstdev(samples)
    return mean, median, stdev

def theoretical_sum_distribution(faces: int, dice: int) -> Dict[int, float]:
    dist = [0.0] * (faces + 1)
    for v in range(1, faces + 1):
        dist[v] = 1.0 / faces

    cur = dist
    for _ in range(2, dice + 1):
        nxt = [0.0] * (len(cur) + faces)
        for s, p in enumerate(cur):
            if p == 0:
                continue
            for v in range(1, faces + 1):
                nxt[s + v] += p / faces
        cur = nxt

    return {s: cur[s] for s in range(dice, dice * faces + 1)}

def experimental_sum_distribution(
    faces: int, dice: int, rolls: int, seed: int | None
) -> Dict[int, float]:
    set_seed(seed)
    sums = [sum(roll_dices(dice, faces)) for _ in range(rolls)]
    cnt = Counter(sums)
    return {k: v / rolls for k, v in sorted(cnt.items())}

def compare_probabilities(
    target_sum: int, faces: int, dice: int,
    rolls: int, seed: int | None
) -> Tuple[float, float, float, int]:
    exp_dist = experimental_sum_distribution(faces, dice, rolls, seed)
    p_exp = exp_dist.get(target_sum, 0.0)

    theory = theoretical_sum_distribution(faces, dice)
    p_theory = theory.get(target_sum, 0.0)

    diff_pp = (p_exp - p_theory) * 100.0
    successes = int(round(p_exp * rolls))
    return p_exp, p_theory, diff_pp, successes

def simulate_craps_once() -> bool:
    def roll2():
        return roll_dice(6) + roll_dice(6)

    first = roll2()
    if first in (7, 11):
        return True
    if first in (2, 3, 12):
        return False

    point = first
    while True:
        s = roll2()
        if s == point:
            return True
        if s == 7:
            return False

def simulate_craps(n: int, seed: int | None) -> Tuple[int, int]:
    set_seed(seed)
    wins = sum(simulate_craps_once() for _ in range(n))
    return wins, n - wins

def simulate_yahtzee(n: int, faces: int, seed: int | None) -> Tuple[int, int]:
    set_seed(seed)
    successes = 0
    for _ in range(n):
        dice = roll_dices(5, faces)
        if len(set(dice)) == 1:
            successes += 1
    return successes, n - successes

def yahtzee_theoretical(faces: int) -> float:
    return 1.0 / (faces ** 4)

def play_sum_game(dice: int, faces: int, seed: int | None) -> str:
    set_seed(seed)
    you = sum(roll_dices(dice, faces))
    comp = sum(roll_dices(dice, faces))
    if you > comp:
        return f"Tu: {you} | Computer: {comp} -> Ai castigat!"
    if you < comp:
        return f"Tu: {you} | Computer: {comp} -> Ai pierdut!"
    return f"Tu: {you} | Computer: {comp} -> Egalitate!"

def simulate_simple_rolls(
    faces: int, rolls: int, seed: int | None
) -> Tuple[Counter, List[int]]:
    set_seed(seed)
    results = roll_many(rolls, faces)
    return Counter(results), results

def summarise_rolls(
    faces: int, rolls: int, counts: Counter, samples: List[int]
) -> str:
    lines = [f"Simulare completa: {rolls} aruncari cu zar de {faces} fete", ""]

    for face in range(1, faces + 1):
        cnt = counts.get(face, 0)
        pct = cnt * 100 / rolls
        lines.append(f"{face:>2}: {cnt:>6} ({pct:5.2f}%)")

    lines += ["", "Histograma (ASCII):",
              ascii_histogram({f: counts.get(f, 0) for f in range(1, faces + 1)}),
              ""]

    mean, median, stdev = basic_stats(samples)
    lines.append(f"Medie: {mean:.2f}")
    lines.append(f"Mediana: {median:.2f}")
    lines.append(f"Deviatie standard: {stdev:.2f}")

    return "\n".join(lines)

def save_report(text: str, out_path: str | None) -> str:
    if out_path is None:
        out_path = f"dice_log_{datetime.now():%Y%m%d_%H%M%S}.txt"
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(text)
    return out_path

def build_parser():
    p = argparse.ArgumentParser("dice_simulator")
    p.add_argument("--faces", type=int, default=6, choices=[6, 8, 10, 12, 20])
    p.add_argument("--dice", type=int, default=2)
    p.add_argument("--rolls", type=int, default=1000)
    p.add_argument("--seed", type=int)

    p.add_argument("--prob", type=int)
    p.add_argument("--game", choices=["craps", "yahtzee", "sum"])
    p.add_argument("--save", action="store_true")
    p.add_argument("--out")
    return p

def main():
    args = build_parser().parse_args()

    if args.game == "craps":
        wins, losses = simulate_craps(args.rolls, args.seed)
        out = f"CRAPS\nVictorii: {wins} | Infrangeri: {losses}"
    elif args.game == "yahtzee":
        s, f = simulate_yahtzee(args.rolls, args.faces, args.seed)
        out = f"YAHTZEE\nExperimental: {s/args.rolls*100:.3f}%\nTeoretic: {yahtzee_theoretical(args.faces)*100:.3f}%"
    elif args.game == "sum":
        out = play_sum_game(args.dice, args.faces, args.seed)
    elif args.prob is not None:
        p_e, p_t, diff, succ = compare_probabilities(
            args.prob, args.faces, args.dice, args.rolls, args.seed
        )
        out = (
            f"Probabilitate suma {args.prob}\n"
            f"Experimental: {p_e*100:.2f}% ({succ}/{args.rolls})\n"
            f"Teoretic: {p_t*100:.2f}%\n"
            f"Diferenta: {diff:+.2f} pp"
        )
    else:
        c, s = simulate_simple_rolls(args.faces, args.rolls, args.seed)
        out = summarise_rolls(args.faces, args.rolls, c, s)

    print(out)
    if args.save:
        print("Salvat in:", save_report(out, args.out))

if __name__ == "__main__":
    main()