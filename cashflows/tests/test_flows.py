from unittest import TestCase

import cashflows


class TestFlows(TestCase):
    def test_cash_inflow(self):
        flow_a = cashflows.FlowConf(
            flow_type="inflow",
            time=5,
            value=100,
            currency="mxn"
        )
        self.assertTrue(isinstance(flow_a, cashflows.FlowConf))

    def test_cash_outflow(self):
        flow_a = cashflows.FlowConf(
            flow_type="outflow",
            time=0,
            value=7,
            currency="mxn"
        )
        self.assertTrue(isinstance(flow_a, cashflows.FlowConf))

    def test_combine_infows(self):
        f_type = "inflow"
        common_time = 1
        common_currency = "mxn"
        flow_a = cashflows.FlowConf(
            flow_type=f_type,
            time=common_time,
            value=100,
            currency=common_currency
        )
        flow_b = cashflows.FlowConf(
            flow_type=f_type,
            time=common_time,
            value=50,
            currency=common_currency
        )
        flow_a.combine(flow_b)
        self.assertTrue(flow_a.value == 100 + 50)

    def test_combine_outflows(self):
        f_type = "outflow"
        common_time = 1
        common_currency = "mxn"
        flow_a = cashflows.FlowConf(
            flow_type=f_type,
            time=common_time,
            value=100,
            currency=common_currency
        )
        flow_b = cashflows.FlowConf(
            flow_type=f_type,
            time=common_time,
            value=50,
            currency=common_currency
        )
        flow_a.combine(flow_b)
        self.assertTrue(flow_a.value == 100 + 50)

    def test_combine_opposites_no_flip(self):
        common_time = 1
        common_currency = "mxn"
        flow_a = cashflows.FlowConf(
            flow_type="inflow",
            time=common_time,
            value=100,
            currency=common_currency
        )
        flow_b = cashflows.FlowConf(
            flow_type="outflow",
            time=common_time,
            value=50,
            currency=common_currency
        )
        flow_a.combine(flow_b)
        self.assertTrue((flow_a.value == 50) and (flow_a.type != flow_b.type))

    def test_combine_opposites_with_flip(self):
        flow_a = cashflows.FlowConf(
            flow_type="inflow",
            time=1,
            value=100,
            currency="mxn"
        )
        flow_b = cashflows.FlowConf(
            flow_type="outflow",
            time=1,
            value=50,
            currency="mxn"
        )
        flow_b.combine(flow_a)
        self.assertTrue((flow_b.value == 50) and (flow_a.type == flow_b.type))

    def test_cashflow(self):
        cash_flows = cashflows.CashFlow()
        cash_flows.add("outflow", 0, 100, "mxn")
        cash_flows.add("inflow", 2, 50, "mxn")
        cash_flows.add("inflow", 4, 80, "mxn")
        cash_flows.add("outflow", 4, 10, "mxn")
        self.assertTrue(isinstance(cash_flows, cashflows.CashFlow))

    def test_profitability(self):
        cash_flows = cashflows.CashFlow()
        cash_flows.add("outflow", 0, 100, "mxn")
        cash_flows.add("inflow", 2, 50, "mxn")
        cash_flows.add("inflow", 4, 80, "mxn")
        cash_flows.add("outflow", 4, 10, "mxn")
        self.assertTrue(cash_flows.get_profitability() == 1.2)

    def test_irr(self):
        cash_flows = cashflows.CashFlow()
        cash_flows.add("outflow", 0, 100, "mxn")
        cash_flows.add("inflow", 2, 50, "mxn")
        cash_flows.add("inflow", 4, 80, "mxn")
        cash_flows.add("outflow", 4, 10, "mxn")
        self.assertTrue(cash_flows.get_irr() == 5.981718)
