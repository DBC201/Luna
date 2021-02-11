# The Fibonacci retracement levels are 23.6%, 38.2%, 61.8%, and 78.6%.
# While not officially a Fibonacci ratio, 50% is also used.
# 23.6%, 38.2%, 50%, 61.8%, 78.6%, 100%, 161.8%, 261.8%,  423.6%
# and 70.2% for luck

fib_ratios = [0.236, 0.382, 0.5, 0.618, 0.702, 0.786, 1]


def fib_breaking_points(min_val, max_val):
    margin = max_val - min_val
    breaking_points = []
    for ratio in fib_ratios:
        breaking_points.append(min_val+(margin*ratio))
    return breaking_points
