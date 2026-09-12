#!/usr/bin/env python3
"""
fourbar.py -- four-bar / linkage synthesis and analysis helper.

Four-bars are the mechanism FRC teams most often get wrong on paper and then discover in metal:
the coupler path clips the bumper, the transmission angle collapses near the end of travel so the
mechanism binds, or the thing extends past the frame perimeter in a position nobody drew.

THREE MODES
  analyze  -- given link lengths, sweep the crank and report the coupler path, the transmission
              angle (the bind indicator), the required crank torque under a payload, and an
              axis-aligned bounding box of the whole motion (the frame-perimeter check).
  parallel -- size a PARALLELOGRAM four-bar (the common FRC intake/scoring lift, because the
              coupler stays parallel to ground so the end effector never rotates) from the
              horizontal and vertical travel you actually want.
  synth2   -- two-position motion synthesis: give it the start and end pose of the coupler and a
              choice of moving pivot, and it returns the ground pivot and link length.

USAGE
  python fourbar.py analyze
  python fourbar.py analyze --a 6 --b 20 --c 6 --d 20    # the change-point BIND demo
  python fourbar.py parallel --dx 14 --dy 20 --link 24
  python fourbar.py synth2 --p1 4,6 --th1 0 --p2 22,26 --th2 0 --pivot 0,2

CONVENTIONS
  Ground pivot O2 at the origin, O4 at (d, 0). Crank a = O2->A, coupler b = A->B, rocker c = O4->B.
  Coupler point P is given in the coupler frame with origin at A and x-axis along A->B.
  Transmission angle mu = angle between coupler and rocker at B. Textbook guidance: keep
  40 deg <= mu <= 140 deg. Below ~30 deg the linkage is effectively a toggle and will bind or
  need enormous torque. [H] standard mechanism-design practice, not an FRC rule.
"""
import argparse, math, sys

DEG = 180.0 / math.pi


def grashof(a, b, c, d):
    links = sorted([a, b, c, d])
    s, p, q, l = links[0], links[1], links[2], links[3]
    if s + l < p + q:
        cls = "Grashof (crank-rocker or double-crank): at least one link fully rotates"
    elif abs((s + l) - (p + q)) < 1e-9:
        cls = "Change point (special-case Grashof): links can align, motion is ambiguous. AVOID"
    else:
        cls = "non-Grashof (double-rocker): NO link fully rotates -- both links only oscillate"
    return cls, (s + l), (p + q)


def position(a, b, c, d, th2, branch=+1):
    """Closed-form four-bar position solution. Returns (A, B, th3, th4) or None if the crank
    angle is not reachable (the linkage cannot be assembled there)."""
    ax, ay = a * math.cos(th2), a * math.sin(th2)
    dx, dy = d - ax, -ay
    e = math.hypot(dx, dy)
    if e > b + c or e < abs(b - c) or e < 1e-9:
        return None
    cos_ang = (b * b + e * e - c * c) / (2 * b * e)
    cos_ang = max(-1.0, min(1.0, cos_ang))
    ang = math.acos(cos_ang)
    base = math.atan2(dy, dx)
    th3 = base + branch * ang
    bx, by = ax + b * math.cos(th3), ay + b * math.sin(th3)
    th4 = math.atan2(by - 0.0, bx - d)
    return (ax, ay), (bx, by), th3, th4


def transmission_angle(b_pt, a_pt, d, c):
    """Angle at B between coupler BA and rocker BO4."""
    v1 = (a_pt[0] - b_pt[0], a_pt[1] - b_pt[1])
    v2 = (d - b_pt[0], 0.0 - b_pt[1])
    n1 = math.hypot(*v1)
    n2 = math.hypot(*v2)
    if n1 < 1e-9 or n2 < 1e-9:
        return 0.0
    ct = (v1[0] * v2[0] + v1[1] * v2[1]) / (n1 * n2)
    return math.degrees(math.acos(max(-1.0, min(1.0, ct))))


def analyze(a=6.0, b=18.0, c=12.0, d=20.0, px=10.0, py=3.0, load_lbf=15.0,
            start_deg=-20.0, end_deg=110.0, step_deg=10.0, branch=1):
    cls, sl, pq = grashof(a, b, c, d)
    rows = []
    xs, ys = [], []
    min_mu = 999.0
    max_tau = 0.0
    prev = None
    for i in range(int((end_deg - start_deg) / step_deg) + 1):
        d2 = start_deg + i * step_deg
        th2 = math.radians(d2)
        sol = position(a, b, c, d, th2, branch)
        if sol is None:
            rows.append((d2, None, None, None, None, None))
            continue
        A, B, th3, th4 = sol
        Px = A[0] + px * math.cos(th3) - py * math.sin(th3)
        Py = A[1] + px * math.sin(th3) + py * math.cos(th3)
        mu = transmission_angle(B, A, d, c)
        min_mu = min(min_mu, mu)
        xs.append(Px)
        ys.append(Py)
        # required crank torque via virtual work: tau2 * dth2 = F . dP  (numeric Jacobian)
        tau = None
        h = math.radians(0.5)
        s2 = position(a, b, c, d, th2 + h, branch)
        if s2:
            A2, B2, th3b, _ = s2
            Px2 = A2[0] + px * math.cos(th3b) - py * math.sin(th3b)
            Py2 = A2[1] + px * math.sin(th3b) + py * math.cos(th3b)
            dPy = (Py2 - Py) / h                      # in/rad
            tau = abs(load_lbf * dPy)                 # in-lb, vertical payload only
            max_tau = max(max_tau, tau)
        rows.append((d2, Px, Py, mu, tau, math.degrees(th3)))
        prev = (Px, Py)
    box = (min(xs), max(xs), min(ys), max(ys)) if xs else (0, 0, 0, 0)
    return dict(a=a, b=b, c=c, d=d, px=px, py=py, load_lbf=load_lbf, grashof=cls,
                sl=sl, pq=pq, rows=rows, min_mu=min_mu, max_torque_inlb=max_tau,
                bbox=box, reach_x=box[1] - box[0], rise_y=box[3] - box[2])


def parallel(dx=14.0, dy=20.0, link=24.0, pivot_height=6.0, load_lbf=15.0):
    """Parallelogram four-bar: a == c, b == d, so the coupler translates without rotating.
    Given desired horizontal reach dx and vertical rise dy, solve for the link angles."""
    need = math.hypot(dx, dy)
    if need > 2 * link:
        return dict(feasible=False, reason="travel %.1f in exceeds 2x link length %.1f in"
                                           % (need, link), link=link, dx=dx, dy=dy)
    # Closed form. Both link-end positions lie on a circle of radius `link`; the travel vector
    # is the chord. chord = 2*link*sin(delta/2), and the chord is perpendicular to the bisector
    # of the two link angles.
    delta = 2.0 * math.asin(min(1.0, need / (2.0 * link)))
    psi = math.atan2(dy, dx)
    th1 = psi - math.pi / 2 - delta / 2
    th2 = th1 + delta
    x1, y1 = link * math.cos(th1), link * math.sin(th1)
    x2, y2 = link * math.cos(th2), link * math.sin(th2)
    gc = pivot_height + min(y1, y2)
    tau = load_lbf * link * max(abs(math.cos(th1)), abs(math.cos(th2)))
    return dict(feasible=True, link=link, dx=dx, dy=dy,
                start_deg=math.degrees(th1), end_deg=math.degrees(th2),
                sweep_deg=math.degrees(delta), ground_clearance_in=gc,
                peak_torque_inlb=tau, load_lbf=load_lbf,
                max_extension_beyond_pivot_in=max(x1, x2),
                check_dx=x2 - x1, check_dy=y2 - y1,
                pivot_height=pivot_height)


def synth2(p1, th1_deg, p2, th2_deg, pivot_local):
    """Two-position MOTION synthesis by the dyad/perpendicular-bisector method.
    pivot_local = (u, v), the moving pivot expressed in the coupler frame."""
    t1, t2 = math.radians(th1_deg), math.radians(th2_deg)
    u, v = pivot_local
    A1 = (p1[0] + u * math.cos(t1) - v * math.sin(t1),
          p1[1] + u * math.sin(t1) + v * math.cos(t1))
    A2 = (p2[0] + u * math.cos(t2) - v * math.sin(t2),
          p2[1] + u * math.sin(t2) + v * math.cos(t2))
    mx, my = (A1[0] + A2[0]) / 2, (A1[1] + A2[1]) / 2
    dx, dy = A2[0] - A1[0], A2[1] - A1[1]
    n = math.hypot(dx, dy)
    if n < 1e-9:
        return dict(ok=False, reason="the two positions of this moving pivot coincide; "
                                     "pick a different pivot_local")
    # perpendicular bisector direction
    pxd, pyd = -dy / n, dx / n
    picks = []
    for t in (-12.0, -8.0, -4.0, 0.0, 4.0, 8.0, 12.0):
        gx, gy = mx + pxd * t, my + pyd * t
        L = math.hypot(A1[0] - gx, A1[1] - gy)
        swept = math.degrees(
            math.atan2(A2[1] - gy, A2[0] - gx) - math.atan2(A1[1] - gy, A1[0] - gx))
        while swept > 180:
            swept -= 360
        while swept < -180:
            swept += 360
        picks.append((t, (gx, gy), L, swept))
    return dict(ok=True, A1=A1, A2=A2, midpoint=(mx, my),
                bisector_dir=(pxd, pyd), picks=picks, chord=n)


def fmt_analyze(r):
    L = []
    P = L.append
    P("=" * 79)
    P("FOUR-BAR ANALYSIS   crank a=%.2f  coupler b=%.2f  rocker c=%.2f  ground d=%.2f (in)"
      % (r["a"], r["b"], r["c"], r["d"]))
    P("  coupler point P at (%.2f, %.2f) in the coupler frame; payload %.1f lbf vertical"
      % (r["px"], r["py"], r["load_lbf"]))
    P("=" * 79)
    P("  Grashof: %s" % r["grashof"])
    P("           s+l = %.2f  vs  p+q = %.2f" % (r["sl"], r["pq"]))
    P("")
    P("  crank deg      Px      Py   trans.angle   crank torque(in-lb)   coupler deg")
    for (d2, Px, Py, mu, tau, th3) in r["rows"]:
        if Px is None:
            P("  %8.0f    ---     ---   NOT ASSEMBLABLE at this crank angle" % d2)
        else:
            flag = "  <-- BIND RISK" if mu < 40 else ""
            P("  %8.0f  %6.2f  %6.2f   %8.1f      %14.1f   %10.1f%s"
              % (d2, Px, Py, mu, tau if tau else 0.0, th3, flag))
    P("")
    P("  minimum transmission angle .............. %.1f deg  --> %s"
      % (r["min_mu"], "OK (>=40)" if r["min_mu"] >= 40 else
         ("MARGINAL (30-40)" if r["min_mu"] >= 30 else "TOGGLE / WILL BIND. Redesign.")))
    P("  peak crank torque under %.0f lbf ......... %.1f in-lb (%.2f Nm)"
      % (r["load_lbf"], r["max_torque_inlb"], r["max_torque_inlb"] * 0.112984829))
    P("  coupler-point bounding box .............. x [%.2f, %.2f]  y [%.2f, %.2f]"
      % r["bbox"])
    P("  horizontal reach %.2f in, vertical rise %.2f in" % (r["reach_x"], r["rise_y"]))
    P("  FRAME-PERIMETER CHECK: compare max x above against your frame half-width plus the")
    P("  BUMPER thickness. 2026 R102/R104 baseline [H]; BIOCORE extension rules are UNKNOWN")
    P("  until 2027-01-09. Do not cut tube against this until the manual exists.")
    return "\n".join(L)


def fmt_parallel(r):
    L = []
    P = L.append
    P("=" * 79)
    P("PARALLELOGRAM FOUR-BAR SIZING  (coupler stays parallel: end effector never rotates)")
    P("=" * 79)
    if not r.get("feasible"):
        P("  INFEASIBLE: %s" % r["reason"])
        P("  Try: longer links, or a two-stage / virtual four-bar, or an elevator instead.")
        return "\n".join(L)
    P("  target travel ......... dx %.1f in, dy %.1f in   link length %.1f in"
      % (r["dx"], r["dy"], r["link"]))
    P("  start link angle ...... %+7.1f deg" % r["start_deg"])
    P("  end link angle ........ %+7.1f deg" % r["end_deg"])
    P("  swept angle ........... %7.1f deg   <- this is what your gearbox must deliver"
      % r["sweep_deg"])
    P("  ground clearance at the low position .. %.1f in (pivot at %.1f in)"
      % (r["ground_clearance_in"], r["pivot_height"]))
    if r["ground_clearance_in"] < 1.0:
        P("      --> BELOW 1 in. This drags on carpet or on the field border. Raise the pivot.")
    P("  peak torque at the pivot under %.0f lbf .. %.0f in-lb (%.1f Nm)"
      % (r["load_lbf"], r["peak_torque_inlb"], r["peak_torque_inlb"] * 0.112984829))
    P("  max horizontal extension past the pivot .. %.1f in" % r["max_extension_beyond_pivot_in"])
    P("  closure check: achieved dx %.3f, dy %.3f in (must match the target)"
      % (r["check_dx"], r["check_dy"]))
    P("  --> feed the peak torque into: python elevator_arm.py arm --ratio ... --mass ...")
    return "\n".join(L)


def fmt_synth2(r):
    L = []
    P = L.append
    P("=" * 79)
    P("TWO-POSITION MOTION SYNTHESIS  (dyad / perpendicular-bisector method)")
    P("=" * 79)
    if not r.get("ok"):
        P("  FAILED: %s" % r["reason"])
        return "\n".join(L)
    P("  moving pivot at position 1 .... (%.2f, %.2f)" % r["A1"])
    P("  moving pivot at position 2 .... (%.2f, %.2f)" % r["A2"])
    P("  chord length .................. %.2f in" % r["chord"])
    P("  Every ground pivot on the perpendicular bisector below is a valid solution.")
    P("  Pick by packaging: the one that fits inside your frame and gives a sane link length.")
    P("")
    P("   offset(in)     ground pivot          link length     swept angle")
    for (t, g, Ln, sw) in r["picks"]:
        P("   %+8.1f     (%7.2f, %7.2f)      %8.2f       %+8.1f deg" % (t, g[0], g[1], Ln, sw))
    P("")
    P("  RULE OF THUMB [H]: swept angle between 60 and 120 deg keeps the gearbox reasonable and")
    P("  the transmission angle healthy. Under 30 deg means a huge gear ratio; over 150 deg")
    P("  usually means the mechanism sweeps through the frame.")
    P("  Then run: python fourbar.py analyze --a <link> --b ... to check the full path.")
    return "\n".join(L)


def _pt(s):
    x, y = s.split(",")
    return (float(x), float(y))


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("mode", choices=["analyze", "parallel", "synth2"], nargs="?", default="analyze")
    p.add_argument("--a", type=float, default=6.0)
    p.add_argument("--b", type=float, default=18.0)
    p.add_argument("--c", type=float, default=12.0)
    p.add_argument("--d", type=float, default=20.0)
    p.add_argument("--px", type=float, default=10.0)
    p.add_argument("--py", type=float, default=3.0)
    p.add_argument("--load", type=float, default=15.0)
    p.add_argument("--start", type=float, default=-20.0)
    p.add_argument("--end", type=float, default=110.0)
    p.add_argument("--step", type=float, default=10.0)
    p.add_argument("--dx", type=float, default=14.0)
    p.add_argument("--dy", type=float, default=20.0)
    p.add_argument("--link", type=float, default=24.0)
    p.add_argument("--pivot-height", type=float, default=6.0)
    p.add_argument("--p1", type=_pt, default=(4.0, 6.0))
    p.add_argument("--p2", type=_pt, default=(22.0, 26.0))
    p.add_argument("--th1", type=float, default=0.0)
    p.add_argument("--th2", type=float, default=0.0)
    p.add_argument("--pivot", type=_pt, default=(0.0, 2.0))
    a = p.parse_args()
    if a.mode == "analyze":
        print(fmt_analyze(analyze(a.a, a.b, a.c, a.d, a.px, a.py, a.load,
                                  a.start, a.end, a.step)))
    elif a.mode == "parallel":
        print(fmt_parallel(parallel(a.dx, a.dy, a.link, a.pivot_height, a.load)))
    else:
        print(fmt_synth2(synth2(a.p1, a.th1, a.p2, a.th2, a.pivot)))
