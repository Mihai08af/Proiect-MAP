"""Craps"""
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

"""Yahtzee"""
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

"""Tu vs Computer"""
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
