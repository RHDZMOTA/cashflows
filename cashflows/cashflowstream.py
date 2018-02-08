import copy
from datetime import timedelta

import matplotlib.pyplot as plt
from numpy import abs, zeros, arange, irr, npv
from numpy.random import rand, randint


from .cashflow import CashFlow
from .settings import FLOW_TYPES, DEFAULT_CURRENCY
from .util.financial_functions import xnpv, xirr


class CashFlowStream(object):

    def __init__(self, time_type, annual_factor=None, name="", currency=DEFAULT_CURRENCY):
        """Create an stream of cashflow objects and perform financial operations over it.

        :param time_type: [string] whether the stream will contain CashFlow object with time_type "int" or "date".
        :param annual_factor: [float] When working with "int" time_type the annual factor needs to be specified for
        generating interest rates (e.g. annual_factor=1 will take each time unit as a year, annual_fator=12 will take
        each time unit as a month).
        :param currency: [string] the currency of the stream.
        """
        self.annual_factor = annual_factor if annual_factor else 1
        self.currency = currency
        self.time_type = time_type
        self.max_time = None
        self.flows = []
        self.name = name

    def __str__(self):
        return "{\n\t" + "\n\t".join([str(flow) for flow in self.flows]) + "\n}"

    def __eq__(self, other):
        if not isinstance(other, CashFlowStream):
            return False
        if self.get_order() != other.get_order():
            return False
        for this, that in zip(self.get_sorted_flows(), other.get_sorted_flows()):
            if this != that:
                return False
        return True

    def get_order(self):
        return len(self.flows)

    def clone(self):
        return copy.deepcopy(self)

    def scale(self, rate, inplace=False):
        new_flows = [flow.scale(rate) for flow in self.flows]
        if not inplace:
            new_series = self.clone()
            new_series.flows = new_flows
            return new_series
        self.flows = new_flows

    def translate(self, value=0, inplace=False):
        # TODO: translate in time axis.
        flows = copy.deepcopy(self.flows)
        for flow in flows:
            flow.value += value
        if not inplace:
            new_series = self.clone()
            new_series.flows = flows
            return new_series
        self.flows = flows

    def add(self, other, inplace=False):
        if self.time_type != other.time_type:
            raise ValueError("Cannot add two time series with different time_type.")
        new_series = self.clone()
        for flow in other.flows:
            new_series.input_cashflow_obj(flow)
        if not inplace:
            return new_series
        self.flows = new_series.flows

    def neg(self, inplace=False):
        new_series = self.clone()
        for flow in new_series.flows:
            flow.scale(rate=-1, inplace=True)
        if not inplace:
            return new_series
        self.flows = new_series.flows

    def diff(self, other, inplace=False):
        return self.add(other=other.neg(), inplace=inplace)

    def random_initialization(self, n, time_range, value_range, out_prob=0.7, inplace=True):
        other = self.clone()
        for i in range(n):
            time = randint(time_range[0], time_range[-1])
            value = randint(value_range[0], value_range[-1])
            if rand() < out_prob:
                value *= -1
            other.put(value=value, time=time, currency=self.currency)
        if not inplace:
            return other
        self.flows = other.flows

    def _purge(self):
        new_flows = []
        for flow in self.flows:
            if flow.value == 0.:
                continue
            new_flows.append(flow)
        self.flows = new_flows

    def input_cashflow_obj(self, new_flow):
        if not isinstance(new_flow, CashFlow):
            raise ValueError('new_flow is not a FlowConf instance.')
        found = False
        for i in range(len(self.flows)):
            flow = self.flows[i]
            if flow.time == new_flow.time:
                flow.add(new_flow, inplace=True)
                self.flows[i] = flow
                found = True
                break
        if self.time_type != new_flow.time.time_type:
            raise ValueError("New flow has different time_type.")
        if not found:
            self.flows.append(new_flow)
        else:
            self._purge()
        if not self.max_time:
            self.max_time = new_flow.time
        if new_flow.time > self.max_time:
            self.max_time = new_flow.time

    def put(self, value, time, currency=DEFAULT_CURRENCY):
        self.input_cashflow_obj(CashFlow(value, time, self.time_type, currency))

    def input_inflow(self, value, time, currency=DEFAULT_CURRENCY):
        if value < 0:
            raise ValueError("Parameter value must be grater than zero.")
        self.input_cashflow_obj(CashFlow(value, time, self.time_type, currency))

    def input_outflow(self, value, time, currency=DEFAULT_CURRENCY):
        if value < 0:
            raise ValueError("Parameter value must be grater than zero.")
        self.input_cashflow_obj(CashFlow(-value, time, self.time_type, currency))

    def _query_flow_type(self, flow_type, attr):
        if flow_type not in FLOW_TYPES:
            raise ValueError('flow_type not available.')
        return [getattr(flow, attr) for flow in self.flows if flow.get_type() == flow_type]

    def get_cash_on_cash_multiple(self):
        if not self.flows:
            raise ValueError('No flows registered.')
        inflow = sum(self._query_flow_type(flow_type=FLOW_TYPES.get("inflow"), attr="value"))
        outflow = abs(sum(self._query_flow_type(flow_type=FLOW_TYPES.get("outflow"), attr="value")))
        if outflow != 0.0:
            return inflow/outflow
        return float("nan")

    def get_sorted_flows(self):
        if not self.flows:
            return []
        flow_index = enumerate([f.time for f in self.flows])
        sorted_flows = [self.flows[i[0]] for i in sorted(flow_index, key=lambda x: x[-1])]
        return sorted_flows

    def get_irr(self, annual=True, percentage=True, decimals=6):
        sorted_flows = self.get_sorted_flows()
        percentage_factor = 100 if percentage else 1
        if self.time_type == "int":
            flows_with_zeros = zeros(self.max_time.value + 1)
            for flow in sorted_flows:
                flows_with_zeros[flow.time.value] = flow.value
            if annual:
                return round(percentage_factor * self.annual_factor * irr(flows_with_zeros), decimals)
            return round(percentage_factor * irr(flows_with_zeros), decimals)
        if self.time_type == "date":
            return round(percentage_factor * xirr(sorted_flows, year_days=365), decimals)

    def get_npv(self, rate):
        sorted_flows = self.get_sorted_flows()
        if self.time_type == "int":
            flows_with_zeros = zeros(self.max_time.value + 1)
            for flow in sorted_flows:
                flows_with_zeros[flow.time.value] = flow.value
            return npv(rate, flows_with_zeros)
        if self.time_type == "date":
            return xnpv(sorted_flows, rate, year_days=365)

    def plot(self, title="", x_label="", y_label=""):
        sorted_flows = self.get_sorted_flows()
        plt.axhline(y=0)
        if self.time_type == "int":
            flows_with_zeros = zeros(self.max_time.value + 1)
            for flow in sorted_flows:
                flows_with_zeros[flow.time.value] = flow.value
            plt.bar(x=arange(len(flows_with_zeros)), height=flows_with_zeros)
        else:
            w = int((sorted_flows[-1].time.value - sorted_flows[0].time.value).days / (2 * len(sorted_flows)))
            x_values = [flow.time.value for flow in sorted_flows]
            y_values = []
            for flow in sorted_flows:
                y_values.append(flow.value)
            plt.bar(x_values, y_values, width=w, alpha=0.7)
            axes = plt.gca()
            axes.set_xlim([min(x_values) - timedelta(days=w), max(x_values) + timedelta(days=w)])
        plt.title("CashFlow Graphic Representation" if not title else title)
        plt.ylabel(self.flows[0].currency if not y_label else y_label)
        plt.xlabel("Time units" if not x_label else x_label)
        plt.grid()
        plt.show()
