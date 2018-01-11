import warnings
import numpy as np
import matplotlib.pyplot as plt

from .financial_functions import *
from dateutil.parser import parse
from datetime import datetime

flow_types = ["inflow", "outflow"]  # TODO: externalize this.
time_types = ["int", "date"]


class Time(object):

    def __init__(self, value, time_type="date"):
        self.time_type = self.validate_time_type(time_type)
        self.value = self.validate_value(value, time_type)

    def __str__(self):
        return str(self.value)

    def to_string(self):
        return str(self)

    def __eq__(self, other):
        if not isinstance(other, Time):
            return False
        return other.value == self.value

    def __lt__(self, other):
        if not isinstance(other, Time):
            raise ValueError("Cannot perform operation.")
        return self.value < other.value

    def equals(self, other):
        return other == self

    @staticmethod
    def validate_time_type(time_type):
        if time_type not in time_types:
            raise ValueError("Invalid time_type.")
        return time_type

    @staticmethod
    def validate_value(value, time_type):
        if time_type == "int":
            if not isinstance(value, int):
                warnings.warn("Time value must be integer, casting was applied to fix this.")
                value = int(value)
            return value
        if time_type == "date":
            if isinstance(value, str):
                value = parse(value)
            if isinstance(value, datetime):
                return value
        raise ValueError("Value parameter is not a valid type.")


class Flow(object):
    def __init__(self, flow_type, value, time, time_type="int", currency="mxn"):
        self.type = self.validate_flow_type(flow_type)
        self.time = Time(time, time_type)
        self.value = self.validate_value(value)
        self.currency = self.validate_currency(currency)

    def __str__(self):
        return "Flow(type: {this_type}, time: {this_time}, value: {this_value}, currency: {this_currency})".format(
            this_type=self.type,
            this_time=self.time.to_string(),
            this_value=self.value,
            this_currency=self.currency
        )

    def to_string(self):
        return str(self)

    def combine(self, flow_conf):
        if not isinstance(flow_conf, Flow):
            raise ValueError('flow_conf param is not an instance of FlowConf.')
        if not flow_conf.time.equals(self.time):
            raise ValueError('flow_conf param is not in the same time.')
        if not flow_conf.currency == self.currency:
            raise ValueError('flow_conf param is not in the same currency.')
        adjustment = 1 if self.type == flow_conf.type else -1
        new_val = self.value + adjustment * flow_conf.value
        self.type = self.type if new_val > 0 else flow_conf.type
        self.value = np.abs(new_val)

    @staticmethod
    def validate_flow_type(flow_type):
        if not isinstance(flow_type, str):
            raise ValueError('String value expected.')
        if flow_type not in flow_types:
            raise ValueError('flow_type parameter must be a valid type.')
        return flow_type

    @staticmethod
    def validate_value(value):
        value = float(value)
        return value

    @staticmethod
    def validate_currency(currency):
        # TODO: add validation
        return currency


class CashFlow(object):

    def __init__(self, time_type, annual_factor=None):
        self.annual_factor = annual_factor if annual_factor else 1
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

    def add(self, flow_type, value, time, currency="mxn"):
        self.add_flow_obj(Flow(flow_type, value, time, self.time_type, currency))

    def add_inflow(self, value, time, currency="mxn"):
        self.add_flow_obj(Flow("inflow", value, time, self.time_type, currency))

    def add_outflow(self, value, time, currency="mxn"):
        self.add_flow_obj(Flow("outflow", value, time, self.time_type, currency))

    def _query_flow_type(self, flow_type, attr):
        if flow_type not in flow_types:
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

    def plot(self):
        sorted_flows = self.get_sorted_flows()
        plt.axhline(y=0)
        if self.time_type == "int":
            plt.bar(x=np.arange(len(sorted_flows)), height=sorted_flows)
        else:
            w = int((sorted_flows[-1].time.value - sorted_flows[0].time.value).days / (2 * len(sorted_flows)))
            plt.bar(
                [flow.time.value for flow in self.get_sorted_flows()],
                [flow.value for flow in self.get_sorted_flows()],
                width=w, alpha=0.7
            )
        plt.title("CashFlow Graphic Representation")
        plt.ylabel(self.flows[0].currency)
        plt.xlabel("Time units")
        plt.grid()
        plt.show()
