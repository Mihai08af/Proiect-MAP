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
    
    p.add_argument("--prob", type=int, default=None
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
        if args_save:
            path = save_report(output, args.out)
            print(f"\nRezultate salvate in {path}")
        return
    
    if args.game == "sum":
        msg = play_sum_game(args.dice, args.faces, args.seed)
        output = f"Joc: SUM - {args.dice} zaruri cu {args.faces} fete\n{msg}"
        print(output)
        if args_save:
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
        if args_save:
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
    