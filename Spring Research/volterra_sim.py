"""Starter simulator for stochastic Volterra equations (SVEs) with the fractional kernel

    X_t = x0 + int_0^t K(t-s) b(X_s) ds + int_0^t K(t-s) sigma(X_s) dW_s,
    K(u) = u^(H-1/2) / Gamma(H+1/2),   0 < H < 1.

b = 0, sigma = 1  -> Riemann-Liouville fBm (rough when H < 1/2).
b = lam(theta - v), sigma = nu sqrt(v) -> rough Heston variance (El Euch & Rosenbaum).

Run:  python3 volterra_sim.py   (self-check + plot)
"""
import numpy as np
from scipy.special import gamma


def kernel_weights(H, dt, N):
    """Per-cell kernel weights for lags k = 1..N, integrated exactly over each cell.

    Kbar_k = mean of K on [(k-1)dt, k dt]         (drift part)
    Kw_k   = RMS  of K on [(k-1)dt, k dt]         (noise part; matches cell variance exactly)
    Exact cell integrals keep the singular kernel finite at lag 1, unlike a left-point Euler.
    """
    k = np.arange(1, N + 1)
    a, g = H + 0.5, gamma(H + 0.5)
    Kbar = dt ** (a - 1) * (k ** a - (k - 1) ** a) / (a * g)
    Kw = np.sqrt(dt ** (2 * H - 1) * (k ** (2 * H) - (k - 1) ** (2 * H)) / (2 * H * g ** 2))
    return Kbar, Kw


def simulate(b, sigma, x0, H, T, N, M, seed=0):
    """M paths on N steps. Returns (t, X) with X of shape (M, N+1).

    ponytail: O(N^2 M) direct convolution. Fine to N~1000; use FFT convolution,
    the hybrid scheme (Bennedsen-Lunde-Pakkanen) or a Markovian multi-factor lift for more.
    """
    rng = np.random.default_rng(seed)
    dt = T / N
    Kbar, Kw = kernel_weights(H, dt, N)
    dW = rng.standard_normal((M, N)) * np.sqrt(dt)
    X = np.empty((M, N + 1))
    X[:, 0] = x0
    B = np.empty((M, N))  # b(X_i) dt
    S = np.empty((M, N))  # sigma(X_i) dW_i
    for n in range(1, N + 1):
        i = n - 1
        B[:, i] = b(X[:, i]) * dt
        S[:, i] = sigma(X[:, i]) * dW[:, i]
        X[:, n] = x0 + B[:, :n] @ Kbar[n - 1::-1] + S[:, :n] @ Kw[n - 1::-1]
    return np.linspace(0, T, N + 1), X


def demo():
    # Self-check: RL fBm has Var(X_T) = T^(2H) / (2H Gamma(H+1/2)^2).
    for H in (0.1, 0.3, 0.5):
        _, X = simulate(lambda x: 0 * x, lambda x: 1 + 0 * x, 0.0, H, 1.0, 200, 10_000, seed=1)
        exact = 1 / (2 * H * gamma(H + 0.5) ** 2)
        rel = abs(X[:, -1].var() / exact - 1)
        print(f"RL fBm H={H}: Var(X_1) sim={X[:, -1].var():.4f} exact={exact:.4f} rel.err={rel:.2%}")
        assert rel < 0.05, rel

    # Rough Heston variance: mean must follow the Volterra ODE, so E[V_T] stays near theta when v0 = theta.
    lam, theta, nu, v0 = 2.0, 0.04, 0.3, 0.04
    t, V = simulate(lambda v: lam * (theta - v), lambda v: nu * np.sqrt(np.maximum(v, 0)),
                    v0, 0.1, 1.0, 300, 5_000, seed=2)
    print(f"rough Heston H=0.1: E[V_1]={V[:, -1].mean():.4f} (theta={theta}), "
          f"P(V<0 somewhere)={np.mean((V < 0).any(1)):.2%}")
    assert abs(V[:, -1].mean() - theta) < 0.005

    try:
        import matplotlib.pyplot as plt
    except ImportError:
        return
    fig, ax = plt.subplots(1, 2, figsize=(11, 4))
    for H in (0.1, 0.3, 0.5):
        tt, X = simulate(lambda x: 0 * x, lambda x: 1 + 0 * x, 0.0, H, 1.0, 1000, 1, seed=3)
        ax[0].plot(tt, X[0], lw=0.8, label=f"H={H}")
    ax[0].set_title("Riemann-Liouville fBm (same noise)"); ax[0].legend()
    ax[1].plot(t, V[:5].T, lw=0.8); ax[1].set_title("Rough Heston variance, H=0.1")
    fig.tight_layout(); fig.savefig("volterra_paths.png", dpi=130)
    print("saved volterra_paths.png")


if __name__ == "__main__":
    demo()
