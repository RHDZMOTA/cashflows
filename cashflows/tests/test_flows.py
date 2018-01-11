from unittest import TestCase

import cashflows


class TestFlows(TestCase):
    def test_cash_inflow(self):
        flow_a = cashflows.Flow(
            flow_type="inflow",
            value=100,
            time=5
        )
        self.assertTrue(isinstance(flow_a, cashflows.Flow))

    def test_cash_outflow(self):
        flow_a = cashflows.Flow(
            flow_type="outflow",
            value=7,
            time=0
        )
        self.assertTrue(isinstance(flow_a, cashflows.Flow))

    def test_combine_infows(self):
        f_type = "inflow"
        t_type = "int"
        common_time = 1
        common_currency = "mxn"
        flow_a = cashflows.Flow(
            flow_type=f_type,
            value=100,
            time=common_time,
            time_type=t_type,
            currency=common_currency
        )
        flow_b = cashflows.Flow(
            flow_type=f_type,
            value=50,
            time=common_time,
            time_type=t_type,
            currency=common_currency
        )
        flow_a.combine(flow_b)
        self.assertTrue(flow_a.value == 100 + 50)

    def test_combine_outflows(self):
        f_type = "outflow"
        t_type = "date"
        common_time = "01/01/2018"
        common_currency = "mxn"
        flow_a = cashflows.Flow(
            flow_type=f_type,
            value=100,
            time=common_time,
            time_type=t_type,
            currency=common_currency
        )
        flow_b = cashflows.Flow(
            flow_type=f_type,
            value=50,
            time=common_time,
            time_type=t_type,
            currency=common_currency
        )
        flow_a.combine(flow_b)
        self.assertTrue(flow_a.value == 100 + 50)

    def test_combine_opposites_no_flip(self):
        common_time = 1
        common_currency = "mxn"
        flow_a = cashflows.Flow(
            flow_type="inflow",
            value=100,
            time=common_time,
            currency=common_currency
        )
        flow_b = cashflows.Flow(
            flow_type="outflow",
            value=50,
            time=common_time,
            currency=common_currency
        )
        flow_a.combine(flow_b)
        self.assertTrue((flow_a.value == 50) and (flow_a.type != flow_b.type))

    def test_combine_opposites_with_flip(self):
        flow_a = cashflows.Flow(
            flow_type="inflow",
            value=100,
            time=1,
            currency="mxn"
        )
        flow_b = cashflows.Flow(
            flow_type="outflow",
            value=50,
            time=1,
            currency="mxn"
        )
        flow_b.combine(flow_a)
        self.assertTrue((flow_b.value == 50) and (flow_a.type == flow_b.type))

    def test_cashflow(self):
        cash_flows = cashflows.CashFlow("int")
        cash_flows.add(flow_type="outflow", value=100, time=0)
        cash_flows.add(flow_type="inflow", value=50, time=2)
        cash_flows.add(flow_type="inflow", value=80, time=4)
        cash_flows.add(flow_type="outflow", value=10, time=4)
        self.assertTrue(isinstance(cash_flows, cashflows.CashFlow))

    def test_profitability(self):
        cash_flows = cashflows.CashFlow("int")
        cash_flows.add(flow_type="outflow",  value=100, time=0)
        cash_flows.add(flow_type="inflow", value=50, time=2)
        cash_flows.add(flow_type="inflow", value=80, time=4)
        cash_flows.add(flow_type="outflow",  value=10, time=4)
        self.assertTrue(cash_flows.get_profitability() == 1.2)

    def test_irr(self):
        cash_flows = cashflows.CashFlow("int")
        cash_flows.add(flow_type="outflow",  value=100, time=0)
        cash_flows.add(flow_type="inflow", value=50, time=2)
        cash_flows.add(flow_type="inflow", value=80, time=4)
        cash_flows.add(flow_type="outflow",  value=10, time=4)
        self.assertTrue(cash_flows.get_irr() == 5.981718)

    def test_xirr(self):
        cash_flows = cashflows.CashFlow("date")
        cash_flows.add(flow_type="outflow", value=100, time="01/01/2018")
        cash_flows.add(flow_type="inflow", value=50, time="01/01/2020")
        cash_flows.add(flow_type="inflow", value=80, time="01/01/2022")
        cash_flows.add(flow_type="outflow", value=10, time="01/01/2022")
        self.assertTrue(cash_flows.get_irr() == 5.9787100000000004)
