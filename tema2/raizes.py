def calc_newton(f, df, x0, tol=1e-10, max_iter=100):
    history = [x0]
    n_f = 0
    n_df = 0
    for iteration in range(max_iter):
        fx = f(history[-1])
        n_f += 1
        dfx = df(history[-1])
        if dfx == 0:
            raise ValueError("Derivative is zero. No solution found.") 
        n_df += 1
        history.append(history[-1] - fx / dfx)
        if (abs(history[-1] - history[-2]) < tol):
            return { "history": history, "iteration": iteration + 1, "count_f": n_f, "count_df": n_df, "convergiu": True }
    return { "history": history, "iteration": iteration + 1, "count_f": n_f, "count_df": n_df, "convergiu": False }

def calc_secante(f, x0, x1, tol=1e-10, max_iter=100):
    history = [x0, x1]
    fx0 = f(history[-2])
    fx1 = f(history[-1])
    n_f = 2
    for iteration in range(max_iter):
        if len(history) > 2:
            fx0 = fx1
            fx1 = f(history[-1])
            n_f += 1
        if fx1 - fx0 == 0:
            raise ValueError("Function values are equal. No solution found.")
        history.append(history[-1] - fx1 * (history[-1] - history[-2]) / (fx1 - fx0))
        if (abs(history[-1] - history[-2]) < tol):
            return { "history": history, "iteration": iteration + 1, "count_f": n_f, "convergiu": True}
    return { "history": history, "iteration": iteration + 1, "count_f": n_f, "convergiu": False }

def calc_bisection(f, a, b, tol=1e-10, max_iter=100):
    fa = f(a)
    fb = f(b)
    if fa * fb >= 0:
        raise ValueError("f(a) and f(b) must have different signs.")
    iteration = 0
    n_f = 2
    history = []
    for iteration in range(max_iter):
        c = (a + b) / 2
        history.append(c)
        if (abs(b - a) / 2 < tol):
            return { "history": history, "iteration": iteration + 1, "count_f": n_f, "convergiu": True }
        fc = f(c)
        n_f += 1
        if fc == 0:
            return { "history": history, "iteration": iteration, "count_f": n_f, "convergiu": True }
        elif fa * fc < 0:
            b = c
            fb = fc
        else:
            a = c
            fa = fc
    return { "history": history, "iteration": iteration + 1, "count_f": n_f,
         "convergiu": False }