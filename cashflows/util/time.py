import warnings

from datetime import datetime
from dateutil.parser import parse

from cashflows.settings import TIME_TYPES


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
        if time_type not in TIME_TYPES:
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