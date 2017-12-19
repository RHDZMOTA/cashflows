import numpy as np
import matplotlib.pyplot as plt

flow_types = ["inflow", "outflow"]  # TODO: externalize this.


class FlowConf(object):
    def __init__(self, flow_type, time, value, currency):
        self.type = self.validate_flow_type(flow_type)
        self.time = self.validate_time(time)
        self.value = self.validate_value(value)
        self.currency = self.validate_currency(currency)

    def __str__(self):
        return "Flow(type: {this_type}, time: {this_time}, value: {this_value}, currency: {this_currency})".format(
            this_type=self.type,
            this_time=self.time,
            this_value=self.value,
            this_currency=self.currency
        )

    def to_string(self):
        return str(self)

    def combine(self, flow_conf):
        if not isinstance(flow_conf, FlowConf):
            print("Raise error: flow_conf param is not an instance of FlowConf.")  # TODO: raise error
        if not flow_conf.time == self.time:
            print("Raise error: flow_conf param is not in the same time.")  # TODO: raise error
        if not flow_conf.currency == self.currency:
            print("Raise error: flow_conf param is not in the same currency.")  # TODO: raise error
        adjustment = 1 if self.type == flow_conf.type else -1
        new_val = self.value + adjustment * flow_conf.value
        self.type = self.type if new_val > 0 else flow_conf.type
        self.value = np.abs(new_val)

    @staticmethod
    def validate_flow_type(flow_type):
        if not isinstance(flow_type, str):
            print("Raise error: string expected.")  # TODO: raise error string value expected.
        if flow_type not in flow_types:
            print("Raise error: flow_type parameter must be either '' or ''.")   # TODO: nature parameter.
        return flow_type

    @staticmethod
    def validate_time(time):
        int_time = int(time)
        if not isinstance(time, int):
            print("Warning: Time must be integer, casting was applied to fix this.")  # TODO: Warning
        return int_time

    @staticmethod
    def validate_value(value):
        value = float(value)
        return value

    @staticmethod
    def validate_currency(currency):
        # TODO: add validation
        return currency


class CashFlow(object):

    def __init__(self, annual_factor=None):
        self.annual_factor = annual_factor if annual_factor else 1
        self.max_time = 0
        self.flows = []

    def __str__(self):
        return "{\n\t" + "\n\t".join([flow.to_string() for flow in self.flows]) + "\n}"

    def to_string(self):
        return str(self)

    def add_flow_obj(self, new_flow):
        if not isinstance(new_flow, FlowConf):
            print("Raise error here.")  # TODO: raise error
        found = False
        for i in range(len(self.flows)):
            flow = self.flows[i]
            if flow.time == new_flow.time:
                flow.combine(new_flow)
                self.flows[i] = flow
                found = True
                break
        if not found:
            self.flows.append(new_flow)
        if new_flow.time > self.max_time:
            self.max_time = new_flow.time

    def add(self, flow_type, time, value, currency):
        self.add_flow_obj(FlowConf(flow_type, time, value, currency))

    def _query_flow_type(self, flow_type, attr):
        if flow_type not in flow_types:
            print("Raise error: flow_type not available.")  # TODO: raise error.
        return [getattr(flow, attr) for flow in self.flows if flow.type == flow_type]

    def get_profitability(self):
        if not self.flows:
            print("Raise error: no flows registered.")  # TODO: raise error.
        inflow = sum(self._query_flow_type(flow_type="inflow", attr="value"))
        outflow = sum(self._query_flow_type(flow_type="outflow", attr="value"))
        if outflow > 0:
            return inflow/outflow
        return float("nan")

    def get_sorted_flows(self):
        if not self.flows:
            print("Raise error: no flows registered.")  # TODO: raise error.
        sorted_flows = np.zeros(self.max_time + 1)
        for flow in self.flows:
            factor = 1 if flow.type == "inflow" else -1
            sorted_flows[flow.time] = factor * flow.value
        return sorted_flows

    def get_irr(self):
        sorted_flows = self.get_sorted_flows()
        return round(100 * self.annual_factor * np.irr(sorted_flows), 6)

    def plot(self):
        sorted_flows = self.get_sorted_flows()
        plt.axhline(y=0)
        plt.bar(x=np.arange(len(sorted_flows)), height=sorted_flows)
        plt.title("CashFlow Graphic Representation")
        plt.ylabel(self.flows[0].currency)
        plt.xlabel("Time units")
        plt.grid()
        plt.show()