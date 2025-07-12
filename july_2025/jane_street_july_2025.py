import marimo

__generated_with = "0.14.10"
app = marimo.App(width="full")


@app.cell
def _():
    import marimo as mo
    import sympy as sy
    import numpy as np

    return mo, np, sy


@app.cell
def _(mo, np):
    def slow_lane_expected_value(a, l):
        size = 0
        s1 = []
        s2 = []
        while size < l:
            curr_s1 = np.random.uniform(1, 2, 10_000_000)
            curr_s2 = np.random.uniform(1, 2, 10_000_000)

            mask1 = np.logical_and(curr_s1 < a, curr_s2 < a)
            curr_s1 = curr_s1[mask1]
            curr_s2 = curr_s2[mask1]

            mask2 = curr_s2 < curr_s1

            curr_s1 = curr_s1[mask2]
            curr_s2 = curr_s2[mask2]

            assert curr_s1.size == curr_s2.size

            curr_size = curr_s1.size

            amount_remaining = l - (size + curr_size)

            if amount_remaining > curr_size:
                s1.append(curr_s1)
                s2.append(curr_s2)

            else:
                s1.append(curr_s1[:amount_remaining])
                s2.append(curr_s2[:amount_remaining])

            size = sum(len(l) for l in s1)

        s1 = np.concatenate(s1)
        s2 = np.concatenate(s2)

        m = lambda a: (a**4 - 4 * a + 3) / (6 * (a - 1) ** 2)

        simulated = np.mean(s2**2)
        analytic = m(a)

        return simulated, analytic

    simulated, analytic = slow_lane_expected_value(1.5, 100_000_000)

    mo.md(f"""
    # Slow lane Calulcation

    Simulted value is: {simulated:.8f}

    analytic value is: {analytic: .8f}

    error: {np.abs(analytic-simulated)/simulated}

    """)
    return


@app.cell
def _(mo, np):
    def fast_lane_expected_value(a, l):
        size = 0
        s1 = []
        s2 = []
        while size < l:
            curr_s1 = np.random.uniform(1, 2, 10_000_000)
            curr_s2 = np.random.uniform(1, 2, 10_000_000)

            mask1 = np.logical_and(curr_s1 > a, curr_s2 > a)
            curr_s1 = curr_s1[mask1]
            curr_s2 = curr_s2[mask1]

            mask2 = curr_s2 < curr_s1

            curr_s1 = curr_s1[mask2]
            curr_s2 = curr_s2[mask2]

            assert curr_s1.size == curr_s2.size

            curr_size = curr_s1.size

            amount_remaining = l - (size + curr_size)

            if amount_remaining > curr_size:
                s1.append(curr_s1)
                s2.append(curr_s2)

            else:
                s1.append(curr_s1[:amount_remaining])
                s2.append(curr_s2[:amount_remaining])

            size = sum(len(l) for l in s1)

        s1 = np.concatenate(s1)
        s2 = np.concatenate(s2)

        m = lambda a: (2 - a) ** 2 / 6

        simulated = np.mean(s2**2 - a * (2 * s2 - a))
        analytic = m(a)

        return simulated, analytic

    simulated_fast, analytic_fast = fast_lane_expected_value(1.5, 100_000_000)

    mo.md(f"""
    # Fast lane Calulcation

    Simulted value is: {simulated_fast:.8f}

    analytic value is: {analytic_fast: .8f}

    error: {np.abs(analytic_fast-simulated_fast)/analytic_fast}

    """)
    return


@app.cell
def _(mo, np, sols):
    def expected_value_full_verification(a, l):
        def cost(s1, s2, a) -> float:
            if s1 < a and s2 < a and s2 < s1:
                return s2**2
            elif s1 > a and s2 > a and s2 < s1:
                return s2**2 - a * (2 * s2 - a)
            else:
                return 0

        s1 = np.random.uniform(1, 2, l)
        s2 = np.random.uniform(1, 2, l)

        c = np.array([cost(one, two, a) for one, two in zip(s1, s2)])

        simulated = np.mean(c)

        m = lambda a: (2 * a**4 - 8 * a**3 + 24 * a**2 - 36 * a + 19) / 12

        analytic = m(a)

        return simulated, analytic

    simulated_full, analytic_full = expected_value_full_verification(
        float(sols[2]), 100_000_000
    )

    mo.md(f"""
    # Full Expected Cost Calculation

    Simulted value is: {simulated_full:.8f}

    analytic value is: {analytic_full: .8f}

    error: {np.abs(analytic_full-simulated_full)/analytic_full}

    """)
    return


@app.cell
def _(mo, sy):
    a = sy.symbols("a", real=True)
    E = sy.Rational(1, 12) * (2 * a**4 - 8 * a**3 + 24 * a**2 - 36 * a + 19)

    dEda = E.diff(a)

    sols = sy.solve(sy.Eq(0, dEda), a)

    mo.md(f"""
    {complex(sols[0])}

    {complex(sols[1])}

    {complex(sols[2])}
    """)
    return E, a, dEda, sols


@app.cell
def _(a, dEda):
    d2Eda2 = dEda.diff(a)
    return


@app.cell
def _(E, a, np, sols):
    from matplotlib import pyplot as plt

    fig = plt.figure()
    ax = fig.add_subplot(111)
    a_space = np.linspace(1, 2, 1000)
    ax.plot(a_space, [E.subs({a: a_val}) for a_val in a_space])
    ax.scatter([sols[2]], [E.subs({a: sols[2]})], color="red", s=20)
    fig
    return


@app.cell
def _(sols):
    f"{float(sols[2]):.10f}"
    return


@app.cell
def _(sols):
    float(sols[2])
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
