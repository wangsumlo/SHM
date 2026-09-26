"""
Future Work extension 1: fit the damped SHM model to the raw data directly by
nonlinear regression, instead of estimating b by averaging values calculated
at each peak (the method used in the original essay, equation 4.18).

Compares the regression estimate of b (with a standard error) against the
peak-averaging estimate, and reports the residual sum of squares for both so
the two methods can be judged on fit quality rather than assumption.
"""
import numpy as np
import pandas as pd
from scipy.optimize import curve_fit


def load_data(file_directory):
    """Same loading logic as graphs.py / undamped.py, tidied up."""
    df = pd.read_excel(file_directory, usecols="A,B,C")
    time = df.iloc[:-1, 0].to_numpy(dtype=float)
    displacement = df.iloc[:-1, 2].to_numpy(dtype=float)
    return time, displacement


def damped_model(t, x0, b, omega, phi, epsilon, m=0.3):
    """
    Equation (4.13)/(4.14) generalised with a free phase phi, so the fit
    isn't forced to assume the peak occurs exactly at t = 0.
    """
    gamma = -b / (2 * m)
    return x0 * np.exp(gamma * t) * np.cos(omega * t + phi) + epsilon


def fit_damped_model(time, displacement, m=0.3, initial_guess=None):
    """
    Fits x0, b, omega, phi, epsilon simultaneously by nonlinear least squares.

    initial_guess: optional (x0, b, omega, phi, epsilon) tuple. Reasonable
    starting values are provided based on the essay's own derived constants
    (omega = 8.52, initial b guess of ~0.4 from the peak-averaging method).
    """
    if initial_guess is None:
        x0_guess = (displacement.max() - displacement.min()) / 2
        eps_guess = displacement.mean()
        initial_guess = (x0_guess, 0.4, 8.52, 0.0, eps_guess)

    popt, pcov = curve_fit(
        lambda t, x0, b, omega, phi, epsilon: damped_model(t, x0, b, omega, phi, epsilon, m=m),
        time, displacement, p0=initial_guess, maxfev=10000
    )
    perr = np.sqrt(np.diag(pcov))
    return popt, perr


def residual_sum_of_squares(time, displacement, params, m=0.3):
    predicted = damped_model(time, *params, m=m)
    return np.sum((displacement - predicted) ** 2)


def peak_averaging_b(t_peaks, x_peaks, x0=0.17, m=0.3):
    """
    Reproduces the essay's original method (equation 4.18/4.19) for
    comparison, given arrays of peak times and peak displacements.
    """
    t_peaks = np.asarray(t_peaks, dtype=float)
    x_peaks = np.asarray(x_peaks, dtype=float)
    b_values = -(2 * m / t_peaks) * np.log(2 * x_peaks / x0)
    return np.mean(b_values)


if __name__ == "__main__":
    excel_sheet2 = "G:/My Drive/Maths/Maths EE/skeleton/EEdata2.xlsx"
    time, displacement = load_data(excel_sheet2)

    params, errors = fit_damped_model(time, displacement)
    x0_fit, b_fit, omega_fit, phi_fit, eps_fit = params
    x0_err, b_err, omega_err, phi_err, eps_err = errors

    print("Nonlinear regression fit (extension 1):")
    print(f"  x0    = {x0_fit:.4f} +/- {x0_err:.4f}")
    print(f"  b     = {b_fit:.4f} +/- {b_err:.4f}")
    print(f"  omega = {omega_fit:.4f} +/- {omega_err:.4f}")
    print(f"  phi   = {phi_fit:.4f} +/- {phi_err:.4f}")
    print(f"  eps   = {eps_fit:.4f} +/- {eps_err:.4f}")

    rss_regression = residual_sum_of_squares(time, displacement, params)
    print(f"  Residual sum of squares (regression fit): {rss_regression:.6f}")

    # Original essay values from equation (4.18), Tables 1 and 2, for comparison.
    t_peaks = [0.340, 0.998, 1.929, 2.893, 3.857, 4.788, 5.719, 6.650, 7.615, 8.546]
    x_peaks = [0.243, 0.231, 0.226, 0.222, 0.221, 0.217, 0.219, 0.218, 0.217, 0.214]
    b_peak_method = peak_averaging_b(t_peaks, x_peaks)
    print(f"\nPeak-averaging method (original essay): b = {b_peak_method:.4f}")

    # Residual sum of squares if we use the peak-averaging b with the essay's
    # fixed x0, omega, phi=0, eps, for a like-for-like comparison.
    fixed_params = (0.17, b_peak_method, 8.52, 0.0, 0.213)
    rss_peak_method = residual_sum_of_squares(time, displacement, fixed_params)
    print(f"Residual sum of squares (peak-averaging fit): {rss_peak_method:.6f}")
