import numpy as np

from .settings import FLOW_TYPES
from .util import Time


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
        if flow_type not in FLOW_TYPES:
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
