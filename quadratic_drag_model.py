"""
Future Work extension 2: test whether linear drag (-b*v) or quadratic drag
(-c*v*|v|) better describes the damped oscillator, by numerically integrating
each equation of motion and fitting it to the raw data.

Linear drag has a closed-form solution (used throughout the essay). Quadratic
drag does not, so this script integrates both models numerically with
solve_ivp so they can be compared on equal footing using the same fitting
procedure and the same error metric (residual sum of squares).
"""
import numpy as np
import pandas as pd
from scipy.integrate import solve_ivp
from scipy.optimize import minimize

from curve_fit_damped import load_data  # reuse the same data loader


def simulate_linear_drag(t_eval, x0, v0, k, b, m=0.3, epsilon=0.213):
    """m*x'' = -k*(x - epsilon) - b*x'  (equilibrium shifted to epsilon)."""
    def rhs(t, y):
        x, v = y
        a = (-k * (x - epsilon) - b * v) / m
        return [v, a]

    sol = solve_ivp(rhs, (t_eval[0], t_eval[-1]), [x0, v0],
                     t_eval=t_eval, rtol=1e-8, atol=1e-8)
    return sol.y[0]


def simulate_quadratic_drag(t_eval, x0, v0, k, c, m=0.3, epsilon=0.213):
    """m*x'' = -k*(x - epsilon) - c*x'*|x'|"""
    def rhs(t, y):
        x, v = y
        a = (-k * (x - epsilon) - c * v * abs(v)) / m
        return [v, a]

    sol = solve_ivp(rhs, (t_eval[0], t_eval[-1]), [x0, v0],
                     t_eval=t_eval, rtol=1e-8, atol=1e-8)
    return sol.y[0]


def fit_model(simulate_fn, time, displacement, m, epsilon, initial_guess):
    """
    Generic fitter: minimises residual sum of squares between the simulated
    trajectory and the raw data, varying (k, drag_coefficient) with the
    initial position/velocity fixed from the data itself.
    """
    x0 = displacement[0]
    v0 = (displacement[1] - displacement[0]) / (time[1] - time[0])  # finite-difference estimate

    def loss(params):
        k, coeff = params
        predicted = simulate_fn(time, x0, v0, k, coeff, m=m, epsilon=epsilon)
        return np.sum((displacement - predicted) ** 2)

    result = minimize(loss, initial_guess, method="Nelder-Mead")
    return result.x, result.fun


if __name__ == "__main__":
    excel_sheet2 = "G:/My Drive/Maths/Maths EE/skeleton/EEdata2.xlsx"
    time, displacement = load_data(excel_sheet2)

    m = 0.3
    epsilon = 0.213
    k_guess = 21.8  # from springconstant.py

    (k_lin, b_lin), rss_lin = fit_model(
        simulate_linear_drag, time, displacement, m, epsilon,
        initial_guess=(k_guess, 0.4)
    )
    print("Linear drag fit:")
    print(f"  k = {k_lin:.3f}, b = {b_lin:.4f}")
    print(f"  Residual sum of squares = {rss_lin:.6f}")

    (k_quad, c_quad), rss_quad = fit_model(
        simulate_quadratic_drag, time, displacement, m, epsilon,
        initial_guess=(k_guess, 1.0)
    )
    print("\nQuadratic drag fit:")
    print(f"  k = {k_quad:.3f}, c = {c_quad:.4f}")
    print(f"  Residual sum of squares = {rss_quad:.6f}")

    print("\nComparison:")
    better = "linear" if rss_lin < rss_quad else "quadratic"
    print(f"  Lower residual sum of squares: {better} drag model")
    print("  (A meaningfully lower RSS for one model, especially over the")
    print("   rapid-damping region 0 <= t <= 4s, supports that drag law.)")
