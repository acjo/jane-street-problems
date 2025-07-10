import marimo

__generated_with = "0.14.10"
app = marimo.App(width="full")


@app.cell
def _():
    import marimo as mo
    import sympy as sy
    return mo, sy


@app.cell
def _(mo, sy):
    a = sy.symbols("a", real=True)
    expr = (
        sy.Rational(7, 3) * sy.Rational(1, 2) * (a - 1) ** 2
        + (sy.Rational(7, 3) - 3 * a + a**2) * sy.Rational(1, 2) * (2 - a) ** 2
    )
    mo.md(rf"${sy.latex(expr.simplify())}$")
    return (a,)


@app.cell
def _(a):
    def speed2pos(s, t):
        if s <= a:
            return 0.5
        else:
            return 1.5
    return


@app.function
def update(i, s1, s2, car1_traj, car1_point, car2_traj, car2_point):
    car1_traj.set_data()


@app.cell
def _(S1, xddot):
    (S1 - xddot) ** 2
    return


@app.cell
def _(S1, xddot):
    (S1 - xddot)
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
