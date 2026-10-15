def calc_newton(f, df, x0, tol=1e-10):
    history = [x0]
    iteration = 0
    while iteration == 0 or abs(history[-1] - history[-2]) >= tol:
        fx = f(history[-1])
        dfx = df(history[-1])
        if dfx == 0:
            raise ValueError("Derivative is zero. No solution found.")
        history.append(history[-1] - fx / dfx)
        iteration += 1
    return history[-1]

def calc_secante(f, x0, x1, tol=1e-10):
    history = [x0, x1]
    iteration = 0
    while iteration == 0 or abs(history[-1] - history[-2]) >= tol:
        fx0 = f(history[-2])
        fx1 = f(history[-1])
        if fx1 - fx0 == 0:
            raise ValueError("Function values are equal. No solution found.")
        history.append(history[-1] - fx1 * (history[-1] - history[-2]) / (fx1 - fx0))
        iteration += 1
    return history[-1]

def calc_bisection(f, a, b, tol=1e-10):
    if f(a) * f(b) >= 0:
        raise ValueError("f(a) and f(b) must have different signs.")
    iteration = 0
    history = [(a, b)]
    while (b - a) / 2 > tol:
        c = (a + b) / 2
        if f(c) == 0:
            return c
        elif f(a) * f(c) < 0:
            b = c
        else:
            a = c
        iteration += 1
        history.append((a, b))
    return (a + b) / 2