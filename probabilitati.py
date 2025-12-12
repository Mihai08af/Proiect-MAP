"""Distributia teoretica a sumei pt zaruri cu fete"""
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
        result[s] = cur[s] if s < len(cur else 0.0)
    return result

"""Simuleaza sume"""
def experimental_sum_distribution(faces: int, dice: int, rolls: int, seed: int | None) -> Dict[int, float]:
    set_seed(seed)
    sums = [sum(roll_dices(dice, faces) for _ in range(rolls))]
    cnt = Counter(sums)
    return {k: v / rolls for k, v in sorted(cnt.items())}

def compare_probabilities(target_sum: int, dice: int, rolls: int, seed: int | None) -> Tuple[float, float, float, int]:
    exp_dist = experimental_sum_distribution(faces, dice, rolls, seed)
    p_exp = exp_dist.get(target_sum, 0.0)
    theory = theoretical_sum_distribution(faces, dice)
    p_theory = theory.get(target_sum, 0.0)
    diff_pp = (p_exp - p_theory) * 100.0
    successes = int(round(p_exp * rolls))
    return p_exp, p_theory, diff_pp, successes
