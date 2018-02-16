from unittest import TestCase

from cashflows import CashFlowStream


class TestFlows(TestCase):

    def test_parity_add_and_scale(self):
        a = CashFlowStream(time_type="int")
        a.random_initialization(n=10, time_range=(0, 10), value_range=(50, 100))
        result = a.scale(2) == a.add(a)
        self.assertTrue(result)

    def test_commutative_property(self):
        a = CashFlowStream(time_type="int")
        b = CashFlowStream(time_type="int")
        a.random_initialization(n=10, time_range=(0, 10), value_range=(50, 100))
        b.random_initialization(n=10, time_range=(0, 10), value_range=(50, 100))
        result = a.add(b) == b.add(a)
        self.assertTrue(result)

    def test_associative_property(self):
        a = CashFlowStream(time_type="int")
        b = CashFlowStream(time_type="int")
        c = CashFlowStream(time_type="int")
        a.random_initialization(n=10, time_range=(0, 10), value_range=(50, 100))
        b.random_initialization(n=10, time_range=(0, 10), value_range=(50, 100))
        c.random_initialization(n=10, time_range=(0, 10), value_range=(50, 100))
        result = (a.add(b)).add(c) == a.add(b.add(c))
        self.assertTrue(result)

    def test_associative_property_scalar(self):
        # Note: test_associative_property_scalar might not pass the test if r, s < 1
        r = 5
        s = 2
        a = CashFlowStream(time_type="int")
        a.random_initialization(n=10, time_range=(0, 10), value_range=(50, 100))
        result = a.scale(s).scale(r) == a.scale(r*s)
        self.assertTrue(result)

    def test_empty_series_definition(self):
        a = CashFlowStream(time_type="int")
        b = CashFlowStream(time_type="int")
        a.random_initialization(n=10, time_range=(0, 10), value_range=(50, 100))
        result = a.add(b) == a
        self.assertTrue(result)

    def test_complement_definition(self):
        a = CashFlowStream(time_type="int")
        b = CashFlowStream(time_type="int")
        a.random_initialization(n=10, time_range=(0, 10), value_range=(50, 100))
        result = a.add(a.neg()) == b
        self.assertTrue(result)

    def test_distributed_property(self):
        r = 0.75
        a = CashFlowStream(time_type="int")
        b = CashFlowStream(time_type="int")
        a.random_initialization(n=10, time_range=(0, 10), value_range=(50, 100))
        b.random_initialization(n=10, time_range=(0, 10), value_range=(50, 100))
        result = (a.add(b)).scale(r) == a.scale(r).add(b.scale(r))
        self.assertTrue(result)

    def test_distributed_property_scalar(self):
        # Note: test_distributed_property_scalar might not pass the test if r, s < 1
        r = 7
        s = 3
        a = CashFlowStream(time_type="int")
        b = CashFlowStream(time_type="int")
        a.random_initialization(n=10, time_range=(0, 10), value_range=(50, 100))
        b.random_initialization(n=10, time_range=(0, 10), value_range=(50, 100))
        result = a.scale(r + s) == a.scale(r).add(a.scale(s))
        self.assertTrue(result)

    def test_get_cash_on_cash_multiple(self):
        a = CashFlowStream(time_type="int")
        a.put(value=-100, time=0)
        a.put(value=50, time=2)
        a.put(value=80, time=4)
        a.put(value=-10, time=4)
        result = a.get_cash_on_cash_multiple() == 1.2
        self.assertTrue(result)

    def test_irr(self):
        a = CashFlowStream(time_type="int")
        a.put(value=-100, time=0)
        a.put(value=50, time=2)
        a.put(value=80, time=4)
        a.put(value=-10, time=4)
        result = a.get_irr() == 5.981718
        self.assertTrue(result)

    def test_xirr(self):
        a = CashFlowStream(time_type="date")
        a.put(value=-100, time="2018-01-01")
        a.put(value=50, time="2020-01-01")
        a.put(value=80, time="2022-01-01")
        a.put(value=-10, time="2022-01-01")
        result = a.get_irr() == 5.9787100000000004
        self.assertTrue(result)
