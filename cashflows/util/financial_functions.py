import scipy.optimize


def xnpv(sorted_flows, rate, year_days=360):
    npv = 0
    for flow in sorted_flows:
        year = (flow.time.value - sorted_flows[0].time.value).days / year_days
        val = flow.value * (1 + rate) ** (-year)
        if flow.type == "outflow":
            val *= -1
        npv += val
    return npv


def xirr(sorted_flows, year_days=360):
    try:
        return scipy.optimize.newton(func=lambda r: xnpv(sorted_flows, r, year_days), x0=0.0)
    except RuntimeError:
        return scipy.optimize.brentq(f=lambda r: xnpv(sorted_flows, r, year_days), a=-1, b=100)
