"""media, mediana si cat de imprastiate/apropaite sunt rezultatele"""
def basic_stats(samples: List[int]) -> Tuple[float, float, float]:
    if not samples:
        return (float("nan"), float("nan"), float("nan"))
    mean = statistics.fmean(samples)
    median = statistics.median(samples)
    stdev = statistics.pstdev(samples)
    return (mean, median, stdev)
