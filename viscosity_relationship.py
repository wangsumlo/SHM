"""
Future Work extension 4: test whether the fitted damping coefficient b scales
with fluid viscosity as predicted by Stokes' law, b_theory = 6*pi*r*eta.

This is a TEMPLATE. It needs one new Tracker dataset per fluid (e.g. water,
a couple of glycerol-water mixtures, vegetable oil) before it can produce a
real result. Fill in `fluids` below with each dataset's file path and the
fluid's known dynamic viscosity, then run.
"""
import numpy as np
import matplotlib.pyplot as plt

from curve_fit_damped import load_data, fit_damped_model

# --- fill in once new data has been collected -------------------------------
# eta values in Pa*s (dynamic viscosity). Water at room temp is ~0.001 Pa*s;
# glycerol-water mixtures and vegetable oil are much higher and give a wider,
# more convincing spread of points for the b-vs-eta plot.
fluids = [
    # {"name": "water",            "path": "path/to/water_data.xlsx",    "eta": 0.001},
    # {"name": "30% glycerol",     "path": "path/to/glycerol30.xlsx",    "eta": 0.0025},
    # {"name": "60% glycerol",     "path": "path/to/glycerol60.xlsx",    "eta": 0.011},
    # {"name": "vegetable oil",    "path": "path/to/oil_data.xlsx",      "eta": 0.05},
]

r = 0.02  # effective radius of the mass (m) - measure directly for the real object
m = 0.3


def stokes_b(eta, r):
    return 6 * np.pi * r * eta


def main():
    if not fluids:
        print("No fluid datasets configured yet - add entries to `fluids` above "
              "once new experimental data has been collected.")
        return

    etas = []
    b_fitted = []
    b_errs = []

    for fluid in fluids:
        time, displacement = load_data(fluid["path"])
        params, errors = fit_damped_model(time, displacement, m=m)
        b_fit = params[1]
        b_err = errors[1]
        etas.append(fluid["eta"])
        b_fitted.append(b_fit)
        b_errs.append(b_err)
        print(f"{fluid['name']}: eta = {fluid['eta']:.5f} Pa.s, "
              f"fitted b = {b_fit:.4f} +/- {b_err:.4f}")

    etas = np.array(etas)
    b_fitted = np.array(b_fitted)
    b_errs = np.array(b_errs)
    b_theory = stokes_b(etas, r)

    plt.errorbar(etas, b_fitted, yerr=b_errs, fmt="o", color="r", label="Fitted b")
    plt.plot(etas, b_theory, color="k", linestyle="--", label="Stokes' law prediction")
    plt.xlabel("Dynamic viscosity, eta [Pa.s]")
    plt.ylabel("Damping coefficient, b")
    plt.title("Damping coefficient vs fluid viscosity")
    plt.legend()
    plt.show()


if __name__ == "__main__":
    main()
