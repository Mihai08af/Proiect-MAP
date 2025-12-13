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

def roll_many(rolls: int, faces:int) -> List[int]:
    return [roll_dice(faces) for _ in range(rolls)]

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

def basic_stats(samples: List[int]) -> Tuple[float, float, float]:
    if not samples:
        return (float("nan"), float("nan"), float("nan"))
    mean = statistics.fmean(samples)
    median = statistics.median(samples)
    stdev = statistics.pstdev(samples)
    return (mean, median, stdev)

def theoretical_sum_distribution(faces: int, dice: int) -> Dict[int, float]:
    dist = [0.0] * (faces + 1)
    for v in range(1, faces + 1):
        dist[v] = 1.0 / faces

    cur = dist
    for _ in range(2, dice + 1):
        next_len = len(cur) + faces
        nxt = [0.0] * next_len
        for s, p in enumerate(cur):
            if p == 0.0:
                continue
            for v in range(1, faces + 1):
                nxt[s + v] += p * (1.0 / faces)
        cur = nxt

    result: Dict[int, float] = {}
    for s in range(dice, dice * faces + 1):
        result[s] = cur[s] if s < len(cur) else 0.0
    return result

def experimental_sum_distribution(faces: int, dice: int, rolls: int, seed: int | None) -> Dict[int, float]:
    set_seed(seed)
    sums = [sum(roll_dices(dice, faces)) for _ in range(rolls)]
    cnt = Counter(sums)
    return {k: v / rolls for k, v in sorted(cnt.items())}

def compare_probabilities(target_sum: int, faces: int, dice: int, rolls: int, seed: int | None) -> Tuple[float, float, float, int]:
    exp_dist = experimental_sum_distribution(faces, dice, rolls, seed)
    p_exp = exp_dist.get(target_sum, 0.0)
    theory = theoretical_sum_distribution(faces, dice)
    p_theory = theory.get(target_sum, 0.0)
    diff_pp = (p_exp - p_theory) * 100.0
    successes = int(round(p_exp * rolls))
    return p_exp, p_theory, diff_pp, successes

def simulate_craps_once() -> bool:
    def roll2() -> int:
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
    wins = 0
    for _ in range(n):
        if simulate_craps_once():
            wins += 1
    losses = n - wins
    return wins, losses

def simulate_yahtzee(n: int, faces: int, seed: int | None) -> Tuple[int, int]:
    set_seed(seed)
    successes = 0
    for _ in range(n):
        dice = roll_dices(5, faces)
        if len(set(dice)) == 1:
            successes += 1
    failures = n - successes
    return successes, failures

def yahtzee_theoretical(faces: int) -> float:
    return 1.0 / (faces ** 4)

def play_sum_game(dice: int, faces: int, seed: int | None) -> str:
    set_seed(seed)
    you = sum(roll_dices(dice, faces))
    comp = sum(roll_dices(dice, faces))
    if you > comp:
        return f"Tu: {you} | Computer: {comp} -> Ai castigat!"
    elif you < comp:
        return f"Tu: {you} | Computer: {comp} -> Ai pierdut!"
    else:
        return f"Tu: {you} | Computer: {comp} -> Egalitate!"

from typing import Tuple

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

def save_report(text: str, out_path: str | None) -> str:
    if out_path is None:
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        out_path = f"dice_log_{ts}.txt"
    with open(out_path, "w", encoding = "utf-8") as f:
        f.write(text)
    return out_path

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog = "dice_simulator",
        description = "Simulator de zaruri si jocuri de noroc (statistici, probabilitati, histograma ASCII)"
    )
    p.add_argument("--faces", type=int, default=6, choices=[6, 8, 10, 12, 20],
                   help="Numarul de fete ale zarului (implicit: 6)")
    p.add_argument("--dice", type=int, default=2,
                   help="Numarul de zaruri, pentru calcule de suma/probabilitate (implicit: 2)")
    p.add_argument("--rolls", type=int, default=1000,
                   help="Numarul de aruncari/simulari (implicit: 1000)")
    p.add_argument("--seed", type=int, default=None,
                   help="Seed pentru generatorul aleator (optional)")
    
    p.add_argument("--prob", type=int, default=None,
                   help="Calculeaza probabilitatea sumei tinta pentru zaruri.")
    p.add_argument("--game", type=str, choices=["craps", "yahtzee", "sum"],
                   help="Ruleaza un joc: Craps, Yahtzee, Sum (Tu vs Computer).")
    p.add_argument("--save", action="store_true",
                   help="Salveaza rezultatele in fisier.")
    p.add_argument("--out", type=str, default=None,
                   help="Calea catre fisierul de iesire (optional daca --save).")
    return p

def main():
    parser = build_parser()
    args = parser.parse_args()

    if args.game == "craps":
        wins, losses = simulate_craps(args.rolls, args.seed)
        win_rate = wins * 100.0 / args.rolls if args.rolls else 0.0
        output = (
            f"Joc: CRAPS - simulari: {args.rolls}\n"
            f"Victorii: {wins} | Infrangeri: {losses} | Rata victorie: {win_rate:.2f}%"
        )
        print (output)
        if args.save:
            path = save_report(output, args.out)
            print(f"\nRezultate salvate in {path}")
        return
    
    if args.game == "yahtzee":
        successes, failures = simulate_yahtzee(args.rolls, args.faces, args.seed)
        p_exp = successes / args.rolls if args.rolls else 0.0
        p_theory = yahtzee_theoretical(args.faces)
        diff = (p_exp - p_theory) * 100.0
        output = (
            f"Joc: YAHTZEE (o aruncare, 5 zaruri de {args.faces} fete) - simulari: {args.rolls}\n"
            f"Succes (YAHTZEE): {successes} | Esec: {failures}\n"
            f"Experimental: {p_exp*100:.3f}% | Teoretic: {p_theory*100:.3f}% | Diferenta: {diff:+.3f} pp"
        )
        print (output)
        if args.save:
            path = save_report(output, args.out)
            print(f"\nRezultate salvate in {path}")
        return
    
    if args.game == "sum":
        msg = play_sum_game(args.dice, args.faces, args.seed)
        output = f"Joc: SUM - {args.dice} zaruri cu {args.faces} fete\n{msg}"
        print(output)
        if args.save:
            path = save_report(output, args.out)
            print(f"\nRezultate salvate in {path}")
        return
    
    if args.prob is not None:
        p_exp, p_theory, diff_pp, successes = compare_probabilities(
            target_sum=args.prob, faces=args.faces, dice=args.dice, rolls=args.rolls, seed = args.seed
        )
        output = (
            f"Probabilitate pentru suma {args.prob} cu {args.dice} zaruri de {args.faces} fete\n"
            f"Experimental: {p_exp*100:.2f}% ({successes} din {args.rolls})\n"
            f"Teoretic:     {p_theory*100:.2f}%\n"
            f"Diferenta:    {diff_pp:+.2f} pp"
        )
        print (output)
        if args.save:
            path = save_report(output, args.out)
            print(f"\nRezultate salvate in {path}")
        return
    
    counts, samples = simulate_simple_rolls(args.faces, args.rolls, args.seed)
    report = summarise_rolls(args.faces, args.rolls, counts, samples)
    print (report)
    if args.save:
        path = save_report(report, args.out)
        print(f"\nRezultate salvate in {path}")

if __name__ == "__main__":
    main()
