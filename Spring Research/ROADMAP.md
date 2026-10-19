# Volterra Processes: From Zero to Research

**Target object.** A stochastic Volterra equation (SVE):

$$X_t = X_0 + \int_0^t K(t,s)\,b(X_s)\,ds + \int_0^t K(t,s)\,\sigma(X_s)\,dW_s$$

The kernel $K$ carries memory, so $X$ is generally **not Markov** and **not a semimartingale**. Classical Itô/PDE tools therefore fail. Most of the field is about getting around that. The flagship example is $K(t,s) = (t-s)^{H-1/2}/\Gamma(H+\tfrac12)$, which gives fractional Brownian motion and **rough volatility**.

Plan for about 12–18 months part-time. Each phase has a **gate**: don't move on until you can pass it.

---

## Phase 0: Prerequisites (2–4 months, skip what you know)

| Topic | Primary resource | Alternative |
|---|---|---|
| Real analysis, $L^p$ spaces | Folland, *Real Analysis*, ch. 1–3, 6 | Axler, *Measure, Integration & Real Analysis* (free PDF) |
| Measure-theoretic probability | Williams, *Probability with Martingales* | Durrett, *Probability: Theory and Examples* (free PDF) |
| Gaussian processes, Kolmogorov continuity | Le Gall, *Brownian Motion, Martingales, and Stochastic Calculus*, ch. 1–2 | — |
| Basic numerics + Python/NumPy | Any; you need vectorization, FFT, Monte Carlo | — |

**Videos:** MIT OCW **6.436J Fundamentals of Probability** (Fall 2018 notes) for probability, and **MIT 18.S096 Topics in Mathematics with Applications in Finance (Fall 2013)** on YouTube, which has lectures on Itô calculus.

**Gate:** Prove that Brownian motion has α-Hölder paths for all α < 1/2 using Kolmogorov's criterion.

---

## Phase 1: Stochastic calculus (2–3 months)

- **Core text:** Le Gall, ch. 3–8 (martingales, Itô integral, Itô formula, SDEs). It is concise and rigorous.
- **Companion:** Øksendal, *Stochastic Differential Equations* (gentler, with lots of exercises), or Shreve, *Stochastic Calculus for Finance II* if finance is your end goal.
- **Reference:** Karatzas & Shreve, *Brownian Motion and Stochastic Calculus*.
- **Numerics:** Kloeden & Platen, *Numerical Solution of SDEs*, ch. 9–10 (Euler/Milstein, strong vs. weak order). For a quick entry, read Higham, "An Algorithmic Introduction to Numerical Simulation of SDEs" (*SIAM Review*, 2001). It is short and contains code.

**Problems:**

1. Øksendal, exercises ch. 4–5 (all).
2. Implement Euler–Maruyama for GBM and OU. Empirically verify strong order 1/2 and weak order 1 with a log-log error plot.
3. Show that $\int_0^t (t-s)^{H-1/2}\,dW_s$ is well-defined for H > 0 and compute its variance.

**Gate:** Problem 2 runs, and you can explain why Euler has strong order 1/2.

---

## Phase 2: Deterministic Volterra equations and fractional calculus (1–1.5 months)

You need this because the deterministic theory (resolvents, singular kernels) is reused constantly.

- Brunner, *Volterra Integral Equations: An Introduction to Theory and Applications* (Cambridge, 2017): ch. 1–3, plus the numerical chapters.
- Gripenberg, Londen & Staffans, *Volterra Integral and Functional Equations* (1990). This is the reference for **resolvents of kernels** (ch. 2, 4, 5). Abi Jaber–Larsson–Pulido rely on it heavily.
- Samko, Kilbas & Marichev, *Fractional Integrals and Derivatives*: Riemann–Liouville operators only (ch. 1–2). Use it as a reference; don't read it cover to cover.

**Problems:**

1. Solve x(t) = 1 − λ ∫₀ᵗ K(t−s) x(s) ds for the fractional kernel. Show that the solution is a Mittag-Leffler function.
2. Compute the resolvent of the second kind for $K(t) = e^{-t}$ and for the fractional kernel.
3. Implement a product-integration (fractional Adams) scheme. Check it against the Mittag-Leffler solution, using `scipy` or the `mittag-leffler` pip package.

**Gate:** You can state what the resolvent R is and why X = (I + R ∗) applied to the forcing term.

---

## Phase 3: Fractional Brownian motion and Gaussian Volterra processes (2 months)

- **Start:** Nourdin, *Selected Aspects of Fractional Brownian Motion* (Springer, 2012). It is short and the best entry point.
- **Then:** Mishura, *Stochastic Calculus for Fractional Brownian Motion and Related Processes* (LNM 1929), ch. 1–2. It covers the Mandelbrot–Van Ness and Molchan–Golosov **Volterra representations** of fBm.
- **Key papers:**
  - Decreusefond & Üstünel (1999), "Stochastic analysis of the fractional Brownian motion," *Potential Analysis*.
  - Alòs, Mazet & Nualart (2001), "Stochastic calculus with respect to Gaussian processes," *Annals of Probability*. **This is the paper that defines Gaussian Volterra processes.**
  - Decreusefond (2005), "Stochastic integration with respect to Volterra processes," *Ann. IHP*.
- **Malliavin calculus** (needed later for rough vol): Nualart, *The Malliavin Calculus and Related Topics*, ch. 1 and 5. For a gentler start, try Nualart & Nualart, *Introduction to Malliavin Calculus* (2018).

**Problems:**

1. Prove that fBm is not a semimartingale for H ≠ 1/2, using the p-variation argument.
2. Simulate fBm exactly with **Davies–Harte / circulant embedding**, and also with Cholesky. Compare cost against N.
3. Estimate H from simulated paths using the variogram/log-increment regression. You will reuse this in Phase 5 on real data.
4. Compare RL fBm (`volterra_sim.py`) with true fBm. Where do they differ, and why does it matter at t near 0?

**Gate:** Problems 2 and 3 work, and you can write down the Molchan–Golosov kernel.

---

## Phase 4: Stochastic Volterra equations, the core theory (2–3 months)

Read in this order:

1. Berger & Mizel (1980), "Volterra equations with Itô integrals I & II," *J. Integral Equations*. This is the historical origin.
2. Protter (1985), "Volterra equations driven by semimartingales," *Annals of Probability*.
3. Zhang, Xicheng (2010), "Stochastic Volterra equations in Banach spaces and stochastic partial differential equation," *J. Funct. Anal.*. It covers singular kernels.
4. **Abi Jaber, Larsson & Pulido (2019), "Affine Volterra processes," *Annals of Applied Probability*.** ⭐ This is the modern centerpiece. It covers existence, the Riccati–Volterra characteristic function, and the rough Heston process. Read it twice.
5. Abi Jaber & El Euch (2019), "Markovian structure of the Volterra Heston model," and "Multifactor approximation of rough volatility models" (*SIAM J. Financial Math.*). They introduce the **Markovian lift**, which is the main trick for simulating SVEs.

**Problems:**

1. Reproduce the existence proof (Picard iteration) for Lipschitz b and σ with a kernel in L²_loc.
2. Derive E[X_t] for an affine SVE. It solves a deterministic Volterra equation; check it against `volterra_sim.py`.
3. Derive the Riccati–Volterra equation for the rough Heston characteristic function. Solve it with the fractional Adams scheme from Phase 2.
4. Write $K(t) = \int e^{-xt}\,\mu(dx)$ for the fractional kernel (completely monotone). Discretize μ into n exponentials and simulate the resulting n-dimensional Markov SDE.

**Gate:** Problem 3 produces the rough Heston characteristic function, and Fourier pricing gives sensible implied vols.

---

## Phase 5: Rough volatility, the main application area (2–3 months)

- **Start here:** Gatheral, Jaisson & Rosenbaum (2018), "Volatility is rough," *Quantitative Finance*.
- Bayer, Friz & Gatheral (2016), "Pricing under rough volatility," *Quant. Finance*. Defines the rough Bergomi model.
- El Euch & Rosenbaum (2019), "The characteristic function of rough Heston models," *Math. Finance*.
- **Book:** Bayer, Friz, Fukasawa, Gatheral, Jacquier & Rosenbaum (eds.), *Rough Volatility* (SIAM, 2024). This is the field's reference book.
- Alòs & García Lorite, *Malliavin Calculus in Finance* (CRC, 2021). It covers short-time ATM skew asymptotics.
- **Literature list:** The "Rough Volatility" literature page maintained by the community (search "rough volatility literature list"). It is the best map of the field.

**Videos** (search YouTube by speaker and title):

- Jim Gatheral, "Volatility is rough" and "Rough volatility: an overview" (many conference versions)
- Mathieu Rosenbaum, talks on rough volatility and Hawkes-process microfoundations
- Eduardo Abi Jaber, talks on affine Volterra processes and Markovian lifts
- Peter Friz, talks on rough paths and rough volatility
- Bloomberg Quant seminars and QuantMinds talks on rough vol

**Problems:**

1. Download realized-variance data (the Oxford-Man library closed in mid-2022; use VOLARE, the SPX series bundled with the R package `highfrequency`, or compute it yourself from intraday data). Estimate H; you should get roughly 0.1.
2. Implement rough Bergomi with the **hybrid scheme** (Bennedsen, Lunde & Pakkanen 2017, *Finance & Stochastics*). Reproduce the ATM skew $\sim T^{H-1/2}$ power law.
3. Compare your result with Ryan McCrickerd's `rough_bergomi` GitHub repo and the "Turbocharging Monte Carlo pricing for the rough Bergomi model" paper.
4. Calibrate rough Heston to an SPX implied-vol surface using your Phase 4 characteristic function.

**Gate:** You have a working rough Bergomi pricer plus the skew power-law plot.

---

## Phase 6: Numerical analysis of SVEs (1–2 months)

- Zhang, Xicheng (2008), "Euler schemes and large deviations for stochastic Volterra equations with singular kernels," *JDE*.
- Richard, Tan & Yang (2021), "Discrete-time simulation of stochastic Volterra equations," *SPA*. It gives strong rates with singular kernels.
- Alfonsi & Kebaier, "Approximation of stochastic Volterra equations with kernels of completely monotone type" (*Math. Comp.*, 2024).
- Alfonsi, "Nonnegativity preserving convolution kernels. Application to stochastic Volterra equations in closed convex domains" (on fixing negative variance).
- Ma & Wu (2022), "A fast algorithm for simulation of rough volatility models," *Quant. Finance*. It uses sum-of-exponentials.

**Problems:**

1. Measure the strong convergence rate of `volterra_sim.py` against N. Theory predicts roughly $N^{-H}$; check it.
2. Replace the O(N²) loop with FFT convolution or a multi-factor lift and benchmark both.
3. `volterra_sim.py` shows rough Heston variance going negative on most paths. Fix this with one method from the papers above.

---

## Phase 7: Research frontier (pick 1–2 threads)

| Thread | Entry point |
|---|---|
| Rough paths and signatures | Friz & Hairer, *A Course on Rough Paths* (2nd ed., 2020); Lyons, Caruana & Lévy, *Differential Equations Driven by Rough Paths* |
| Signature methods / ML for SVEs | Search "signature methods rough volatility" and "neural SDE Volterra"; use the `iisignature` / `esig` Python packages |
| Volterra control and BSDEs | Search "linear-quadratic control Volterra Abi Jaber", "backward stochastic Volterra integral equations" (Yong) |
| Path-dependent PDEs | Viens & Zhang (2019), "A martingale approach for fractional Brownian motion and related path dependent PDEs," *AAP* |
| Hawkes processes → rough vol | Jaisson & Rosenbaum (2016), "Rough fractional diffusions as scaling limits of nearly unstable heavy tailed Hawkes processes," *AAP* |
| Volterra in other fields | Anomalous diffusion and viscoelasticity (physics), turbulence (Barndorff-Nielsen's Ambit/BSS processes), neuroscience |

**How to find open problems:** Read the "Conclusion / further research" sections of the last two years of arXiv papers. Search arXiv for `"stochastic Volterra"` in categories math.PR and q-fin.MF, sorted by date, and skim abstracts weekly.

---

## Tools

- `volterra_sim.py` (in this folder): an SVE simulator with a self-check. Run `python3 volterra_sim.py`.
- Python: `numpy`, `scipy`, `fbm` (pip; Davies–Harte fBm), `iisignature`.
- Julia's `DifferentialEquations.jl` and MATLAB are alternatives. Stay with Python unless you need speed.
- Write everything in LaTeX from day one and keep a running "derivations" notebook. That becomes your first paper's appendix.

## Weekly rhythm that works

- 60% reading plus problems with pen and paper
- 30% code that reproduces a figure from the paper you are reading
- 10% skimming new arXiv papers

Reproducing a paper's figure is the single best test that you understood it.

---

## Appendix: Free access (checked October 2026)

✅ = free and legal (link checked); 🔁 = paid, use the free substitute listed; 🏛 = paid with no full free substitute, so use a library or interlibrary loan.

### Books and courses

| Roadmap item | Status | Free link / substitute |
|---|---|---|
| Axler, *Measure, Integration & Real Analysis* | ✅ | [measure.axler.net/MIRA.pdf](https://measure.axler.net/MIRA.pdf) (official open access) |
| Durrett, *Probability: Theory and Examples* (5th ed.) | ✅ | [services.math.duke.edu/~rtd/PTE/PTE5_011119.pdf](https://services.math.duke.edu/~rtd/PTE/PTE5_011119.pdf) (author's site) |
| Folland, Williams | 🔁 | Use Axler + Durrett above |
| Le Gall, *Brownian Motion, Martingales, and Stochastic Calculus* | 🔁 | Mörters & Peres, *Brownian Motion* draft: [stat.berkeley.edu/~aldous/205B/bmbook.pdf](https://www.stat.berkeley.edu/~aldous/205B/bmbook.pdf) for Brownian motion; MIT 18.S096 for Itô calculus |
| Øksendal, Shreve, Karatzas & Shreve | 🔁 | MIT 18.S096 lectures plus Higham (2001); Le Gall/Øksendal are worth a library loan |
| MIT 18.S096 (Fall 2013), videos and notes | ✅ | [ocw.mit.edu/courses/18-s096-…-fall-2013](https://ocw.mit.edu/courses/18-s096-topics-in-mathematics-with-applications-in-finance-fall-2013/); newer version: [18.642 (Fall 2024)](https://ocw.mit.edu/courses/18-642-topics-in-mathematics-with-applications-in-finance-fall-2024/) |
| MIT 6.436J Fundamentals of Probability | ✅ | [ocw.mit.edu/courses/6-436j-fundamentals-of-probability-fall-2018](https://ocw.mit.edu/courses/6-436j-fundamentals-of-probability-fall-2018/) |
| Kloeden & Platen | 🔁 | Higham (2001), [author PDF](https://webhomes.maths.ed.ac.uk/~dhigham/Publications/P42.pdf) |
| Brunner; Gripenberg–Londen–Staffans; Samko–Kilbas–Marichev | 🏛 | Partial substitute: Section 2 of Abi Jaber–Larsson–Pulido (arXiv:1708.08796) reviews kernels and resolvents |
| Nourdin; Mishura (fBm books) | 🔁 | Decreusefond & Üstünel, "Fractional Brownian motion: theory and applications" (ESAIM Proc. 1998, free at esaim-proc.org), plus the free fBm papers below |
| Nualart, *Malliavin Calculus and Related Topics* | 🔁 | Eulalia Nualart's Wisconsin lecture notes ([course page](https://people.math.wisc.edu/~tgkurtz/NualartLectures.htm)); "An introduction to Malliavin calculus," [arXiv:2502.07941](https://arxiv.org/abs/2502.07941) |
| *Rough Volatility* (SIAM, 2024) | 🔁 | [Rough Volatility Network](https://sites.google.com/site/roughvol/home): literature list, slides and code |
| Alòs & García Lorite, *Malliavin Calculus in Finance* | 🏛 | — |
| Friz & Hairer, *A Course on Rough Paths* | ✅ | Author-hosted 1st-edition draft: [hairer.org/notes/RoughPaths.pdf](https://hairer.org/notes/RoughPaths.pdf) |
| Lyons, Caruana & Lévy (Saint-Flour) | 🔁 | Use Friz & Hairer above |

### Papers

| Paper | Status | Free link |
|---|---|---|
| Berger & Mizel (1980) | 🔁 | Zhang (2010) below covers the general theory |
| Protter (1985), *Ann. Probab.* | ✅ | Project Euclid, IMS back issue: [euclid.aop/1176991173](https://projecteuclid.org/euclid.aop/1176991173) |
| Decreusefond & Üstünel (1999), *Potential Anal.* | 🔁 | Their free ESAIM Proc. 1998 survey (above) covers the same results |
| Alòs, Mazet & Nualart (2001), *Ann. Probab.* | ✅ | [Project Euclid](https://projecteuclid.org/journals/annals-of-probability/volume-29/issue-2/Stochastic-Calculus-with-Respect-to-Gaussian-Processes/10.1214/aop/1008956692.full) |
| Decreusefond (2005), *Ann. IHP* | ✅ | [arXiv:math/0302047](https://arxiv.org/abs/math/0302047) · [Numdam](https://www.numdam.org/item/AIHPB_2005__41_2_123_0) |
| Zhang (2010), SVEs in Banach spaces | ✅ | [arXiv:0812.0834](https://arxiv.org/abs/0812.0834) |
| Zhang (2008), Euler schemes, *JDE* | 🔁 | Richard–Tan–Yang below covers its results and extends them |
| **Abi Jaber, Larsson & Pulido (2019)** | ✅ | [arXiv:1708.08796](https://arxiv.org/abs/1708.08796) |
| Abi Jaber & El Euch, Markovian structure | ✅ | [arXiv:1803.00477](https://arxiv.org/abs/1803.00477) |
| Abi Jaber & El Euch, Multifactor approximation | ✅ | [arXiv:1801.10359](https://arxiv.org/abs/1801.10359) |
| Gatheral, Jaisson & Rosenbaum, "Volatility is rough" | ✅ | [arXiv:1410.3394](https://arxiv.org/abs/1410.3394) |
| Bayer, Friz & Gatheral, "Pricing under rough volatility" | ✅ | [WIAS Preprint 2071](https://www.wias-berlin.de/preprint/2071/wias_preprints_2071.pdf) |
| El Euch & Rosenbaum, rough Heston characteristic function | ✅ | [arXiv:1609.02108](https://arxiv.org/abs/1609.02108) |
| Bennedsen, Lunde & Pakkanen, hybrid scheme | ✅ | [arXiv:1507.03004](https://arxiv.org/abs/1507.03004) |
| McCrickerd & Pakkanen, "Turbocharging…" | ✅ | [arXiv:1708.02563](https://arxiv.org/abs/1708.02563) · code: [github.com/ryanmccrickerd/rough_bergomi](https://github.com/ryanmccrickerd/rough_bergomi) |
| Richard, Tan & Yang (2021), *SPA* | ✅ | [arXiv:2004.00340](https://arxiv.org/abs/2004.00340) |
| Alfonsi & Kebaier, completely monotone kernels | ✅ | [arXiv:2102.13505](https://arxiv.org/abs/2102.13505) |
| Alfonsi, nonnegativity-preserving kernels | ✅ | [arXiv:2302.07758](https://arxiv.org/abs/2302.07758) |
| Ma & Wu (2022), *Quant. Finance* | 🔁 | No preprint found; the sum-of-exponentials idea is covered free in Alfonsi–Kebaier and Abi Jaber–El Euch |
| Viens & Zhang (2019), *AAP* | ✅ | [arXiv:1712.03637](https://arxiv.org/abs/1712.03637) |
| Jaisson & Rosenbaum (2016), *AAP* | ✅ | [arXiv:1504.03100](https://arxiv.org/abs/1504.03100) |

### Data and software

| Item | Status | Link |
|---|---|---|
| Oxford-Man realized library | ❌ closed mid-2022 | Replacements: [VOLARE](https://volare.unime.it/) (open realized-measure archive; check that your index is covered) and the R package `highfrequency` (SPX realized variance, 2000–2019) |
| `fbm`, `iisignature`, `esig`, `mittag-leffler` | ✅ | `pip install fbm iisignature esig mittag-leffler` ([PyPI](https://pypi.org/project/fbm/)) |

**Bottom line:** Every paper in the roadmap is free, except three older journal papers (Berger–Mizel, Zhang 2008, Ma–Wu), and each of those has a free substitute that covers the same material. Of the books, the probability prerequisites and Friz–Hairer are free. The only real gaps are the textbooks on deterministic Volterra equations and fractional calculus (Brunner, Gripenberg et al., Samko et al.) and the two Malliavin-in-finance books. Get those through a library.
