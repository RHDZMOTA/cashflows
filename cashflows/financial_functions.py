import numpy as np
import scipy.optimize


def xnpv(sorted_flows, rate, year_days=360):
    npv = 0
    for flow in sorted_flows:
        year = (flow.time.value - sorted_flows[0].time.value).days / year_days
        val = (1 if flow.type == "inflow" else -1) * flow.value * np.power(1 + rate, -year)
        npv += val
    return npv


def xirr(sorted_flows, year_days=360):
    try:
        return scipy.optimize.newton(lambda r: xnpv(sorted_flows, r, year_days), 0.0)
    except RuntimeError:
        return scipy.optimize.brentq(lambda r: xnpv(sorted_flows, r, year_days), -1, 100)
