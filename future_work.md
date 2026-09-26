# Future Work

The investigation modelled a damped simple harmonic oscillator using a linear drag
assumption (−b𝑥̇) and estimated the damping coefficient by averaging values calculated
at each peak of the oscillation. The evaluation already identified two weaknesses worth
pursuing further: the unmodelled buoyant force, and the sudden increase in damping when
the mass entered the water. The extensions below turn those weaknesses into concrete
follow-up investigations, roughly in order of how directly they build on the existing method.

## 1. Fitting the damping coefficient by nonlinear regression instead of peak-averaging

The original method (equation 4.18) only uses the amplitude at each peak, discarding the
rest of the ~600 recorded data points, and assumes each peak gives an independent,
equally reliable estimate of *b* before averaging. A more statistically sound approach is to
fit the full model

  𝒳(t) = ½x₀e^(−bt/2m) cos(Ωt + φ) + ε

directly to *every* raw (t, x) pair using nonlinear least squares (`scipy.optimize.curve_fit`),
letting *b*, ω, φ and ε vary simultaneously. This should:
- reduce sensitivity to noise in any single peak,
- allow a proper uncertainty (standard error) on *b* to be reported, which the original
  method has no way of producing,
- give a direct, principled way to compare fit quality against the current method (e.g. via
  residual sum of squares or R²) rather than only the area-under-curve percentage error.

*Implemented in `curve_fit_damped.py` below.*

## 2. Testing linear vs quadratic (velocity-squared) drag

The essay assumes Stokes drag (−b𝑥̇), which is only valid at low Reynolds number. Given the
speed of the mass entering water and the size of the oscillations, the flow may in fact be in
a transitional or turbulent regime, where drag scales with 𝑥̇² instead (Newton drag,
−c𝑥̇|𝑥̇|). This can't be solved in closed form, so it requires numerically integrating

  m𝑥̈ = −kx − c𝑥̇|𝑥̇|

(e.g. with `scipy.integrate.solve_ivp`) and fitting *c* to the data the same way *b* is fitted
in the linear case. Comparing the two models' residuals would let the essay make an
evidence-based claim about which drag law actually describes the system, rather than
assuming linear drag by default — and could explain why the model in Figure 11
under-predicts the amplitude during the rapid initial dip (0 ≤ t ≤ 4s), where speeds are
highest.

*Implemented in `quadratic_drag_model.py` below.*

## 3. Explicitly modelling the buoyant force

The evaluation notes that buoyancy was "not taken into account," but the damped equation
of motion only ever includes −kx and −b𝑥̇. Buoyancy contributes a constant force
(ρ_fluid·V_displaced·g) rather than one that depends on position or velocity, so it would
enter the equation of motion as a constant offset:

  m𝑥̈ = −kx − b𝑥̇ + F_b

Solving this modified ODE shifts the equilibrium position analytically (similar to how ε was
introduced empirically in equation 3.16), but here it would be derived from the mass's
volume and the fluid density rather than fitted after the fact. This turns ε from a fitted
constant into a predicted one, and is a natural next step once the drag law (extension 2)
is settled.

## 4. Relating the damping coefficient to fluid viscosity across multiple fluids

The current investigation only compares air (undamped) against water (damped). Repeating
the damped trial in fluids of different, known viscosity (e.g. water, glycerol–water mixtures
at several concentrations, vegetable oil) would let the essay test Stokes' law directly:

  b_theory = 6πrη

where r is an effective radius of the mass and η is the fluid's dynamic viscosity. Plotting the
experimentally fitted *b* (via extension 1) against η for each fluid and checking for the
predicted linear relationship would substantially strengthen the investigation's claim that
the −b𝑥̇ model is physically justified, rather than just numerically convenient.

*A ready-to-populate template is provided in `viscosity_relationship.py` — it needs new
experimental data (one Tracker dataset per fluid) before it can be run.*

## Suggested order of investigation

1. Re-fit *b* by nonlinear regression (extension 1) — needs no new data, immediately
   improves rigour of the existing dataset.
2. Compare linear vs quadratic drag (extension 2) — needs no new data either, and directly
   addresses the largest source of error identified in the evaluation.
3. Add the buoyancy term (extension 3) — a natural refinement once the correct drag law
   is known.
4. Collect new multi-fluid data and test against Stokes' law (extension 4) — the most
   ambitious extension, requiring new experimental work.
