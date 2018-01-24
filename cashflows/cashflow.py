from datetime import timedelta

import matplotlib.pyplot as plt
import numpy as np

from .flow import Flow
from .settings import FLOW_TYPES, DEFAULT_CURRENCY
from .util.financial_functions import xnpv, xirr


class CashFlow(object):

    def __init__(self, time_type, annual_factor=None, currency=DEFAULT_CURRENCY):
        self.annual_factor = annual_factor if annual_factor else 1
        self.currency = currency
        self.time_type = time_type
        self.max_time = None
        self.flows = []

    def __str__(self):
        return "{\n\t" + "\n\t".join([flow.to_string() for flow in self.flows]) + "\n}"

    def to_string(self):
        return str(self)

    def add_flow_obj(self, new_flow):
        if not isinstance(new_flow, Flow):
            raise ValueError('new_flow is not a FlowConf instance.')
        found = False
        for i in range(len(self.flows)):
            flow = self.flows[i]
            if flow.time == new_flow.time:
                flow.combine(new_flow)
                self.flows[i] = flow
                found = True
                break
        if self.time_type != new_flow.time.time_type:
            raise ValueError("New flow has different time_type.")
        if not found:
            self.flows.append(new_flow)
        if not self.max_time:
            self.max_time = new_flow.time
        if new_flow.time > self.max_time:
            self.max_time = new_flow.time

    def add(self, flow_type, value, time, currency=DEFAULT_CURRENCY):
        self.add_flow_obj(Flow(flow_type, value, time, self.time_type, currency))

    def add_inflow(self, value, time, currency=DEFAULT_CURRENCY):
        self.add_flow_obj(Flow("inflow", value, time, self.time_type, currency))

    def add_outflow(self, value, time, currency=DEFAULT_CURRENCY):
        self.add_flow_obj(Flow("outflow", value, time, self.time_type, currency))

    def _query_flow_type(self, flow_type, attr):
        if flow_type not in FLOW_TYPES:
            raise ValueError('flow_type not available.')
        return [getattr(flow, attr) for flow in self.flows if flow.type == flow_type]

    def get_profitability(self):
        if not self.flows:
            raise ValueError('No flows registered.')
        inflow = sum(self._query_flow_type(flow_type="inflow", attr="value"))
        outflow = sum(self._query_flow_type(flow_type="outflow", attr="value"))
        if outflow > 0:
            return inflow/outflow
        return float("nan")

    def get_sorted_flows(self):
        if not self.flows:
            raise ValueError('No flows registered.')
        sorted_flows = None
        if self.time_type == "int":
            sorted_flows = np.zeros(self.max_time.value + 1)
            for flow in self.flows:
                factor = 1 if flow.type == "inflow" else -1
                sorted_flows[flow.time.value] = factor * flow.value
        if self.time_type == "date":
            flow_index = enumerate([f.time for f in self.flows])
            sorted_flows = [self.flows[i[0]] for i in sorted(flow_index, key=lambda x: x[-1])]
        return sorted_flows

    def get_irr(self, annual=True, percentage=True, decimals=6):
        sorted_flows = self.get_sorted_flows()
        percentage_factor = 100 if percentage else 1
        if self.time_type == "int":
            if annual:
                return round(percentage_factor * self.annual_factor * np.irr(sorted_flows), decimals)
            return round(percentage_factor * np.irr(sorted_flows), decimals)
        if self.time_type == "date":
            return round(percentage_factor * xirr(sorted_flows, year_days=365), decimals)

    def get_npv(self, rate):
        sorted_flows = self.get_sorted_flows()
        if self.time_type == "int":
            return np.npv(rate, sorted_flows)
        if self.time_type == "date":
            return xnpv(sorted_flows, rate, year_days=365)

    def plot(self, title="", x_label="", y_label=""):
        sorted_flows = self.get_sorted_flows()
        plt.axhline(y=0)
        if self.time_type == "int":
            plt.bar(x=np.arange(len(sorted_flows)), height=sorted_flows)
        else:
            w = int((sorted_flows[-1].time.value - sorted_flows[0].time.value).days / (2 * len(sorted_flows)))
            x_values = [flow.time.value for flow in sorted_flows]
            y_values = []
            for flow in sorted_flows:
                s = flow.value
                if flow.type == "outflow":
                    s *= -1
                y_values.append(s)
            plt.bar(x_values, y_values, width=w, alpha=0.7)
            axes = plt.gca()
            axes.set_xlim([min(x_values) - timedelta(days=w), max(x_values) + timedelta(days=w)])
        plt.title("CashFlow Graphic Representation" if not title else title)
        plt.ylabel(self.flows[0].currency if not y_label else y_label)
        plt.xlabel("Time units" if not x_label else x_label)
        plt.grid()
        plt.show()
