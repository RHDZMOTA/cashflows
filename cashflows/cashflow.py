import copy

import numpy as np

from .settings import FLOW_TYPES
from .util import Time


class CashFlow(object):

    def __init__(self, value, time, time_type="int", currency="mxn"):
        """Class that represent a single cashflow.

        :param value: Number of monetary units (float).
        :param time: Time unit/value of the cash-flow. May be integer representing the number of time-intervals from
        the origin or string representing a tentative datetime object (preferred format: "%Y-%m-%d").
        :param time_type: Indicates the nature of the time parameter. Values: ("int", "date").
        :param currency: Indicates the currency.
        """
        self.time = Time(time, time_type)
        self.value = self.validate_value(value)
        self.currency = self.validate_currency(currency)

    def __str__(self):
        return "Flow(type: {this_type}, time: {this_time}, value: {this_value}, currency: {this_currency})".format(
            this_type=self.get_type(),
            this_time=self.time.to_string(),
            this_value=np.abs(self.value),
            this_currency=self.currency
        )

    def __eq__(self, other):
        return (self.value == other.value) and (self.time == other.time)

    def get_type(self):
        if self.value < 0:
            return FLOW_TYPES.get("outflow")
        return FLOW_TYPES.get("inflow")

    def clone(self):
        return copy.deepcopy(self)

    def add(self, flow_conf, inplace=False):
        if not isinstance(flow_conf, CashFlow):
            raise ValueError('flow_conf param is not an instance of FlowConf.')
        if not flow_conf.time.equals(self.time):
            raise ValueError('flow_conf param is not in the same time.')
        if not flow_conf.currency == self.currency:
            raise ValueError('flow_conf param is not in the same currency.')
        new_val = self.value + flow_conf.value
        if not inplace:
            new_cash_flow = self.clone()
            new_cash_flow.value = new_val
            return new_cash_flow
        self.value = new_val

    def neg(self):
        return self.scale(rate=-1)

    def scale(self, rate, inplace=False):
        new_val = rate * self.value
        if not inplace:
            new_cash_flow = self.clone()
            new_cash_flow.value = new_val
            return new_cash_flow
        self.value = new_val

    @staticmethod
    def validate_value(value):
        value = float(value)
        return value

    @staticmethod
    def validate_currency(currency):
        # TODO: add validation
        return currency
