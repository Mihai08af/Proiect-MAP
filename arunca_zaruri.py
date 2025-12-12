"""Setez seed-ul Random number generator"""
def set_seed(seed: int | None):
    if seed is not None:
        random.seed(seed)

"""Sa arunce un zar"""
def roll_dice(faces: int) -> int:
    return random.randint(1, faces)

"""Sa arunce zaruri"""
def roll_dices(dice: int, faces: int) -> List[int]:
    return [roll_dice(faces) for _ in range(dice)]

"""Sa arunce zaruri de 'rolls' ori"""
def roll_many(rolls: int, faces:int) -> List[int]:
    return [roll_dice(faces) for _ in range(rolls)]
