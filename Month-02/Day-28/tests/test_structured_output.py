"""Test suite for structured output extraction, repair, and tool dispatching."""
import sys
import os
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from structured_output.validator import OutputValidator
from structured_output.structured_llm import StructuredLLM
from tools.dispatcher import ToolDispatcher


class TestStructuredOutputAndTools(unittest.TestCase):

    def test_json_clean_and_repair(self):
        dirty_json = """
        ```json
        {
            "name": "Alex",
            "age": 30,
        }
        ```
        """
        parsed = OutputValidator.parse_and_validate(dirty_json, required_keys=("name", "age"))
        self.assertEqual(parsed["name"], "Alex")
        self.assertEqual(parsed["age"], 30)

    def test_structured_llm_extraction(self):
        sllm = StructuredLLM()
        minutes = sllm.extract_meeting_minutes("Notes: discussed architecture and next steps.")
        self.assertEqual(minutes.topic, "GenAI Architecture Review")
        self.assertEqual(len(minutes.action_items), 2)
        self.assertEqual(minutes.action_items[0].assignee, "Alice")

    def test_tool_dispatcher_mortgage(self):
        dispatcher = ToolDispatcher()
        res = dispatcher.dispatch(
            "calculate_mortgage",
            {"principal": 300000, "annual_rate": 0.06, "years": 30}
        )
        self.assertTrue(res["success"])
        self.assertAlmostEqual(res["output"]["monthly_payment"], 1798.65, places=1)

    def test_tool_dispatcher_stock(self):
        dispatcher = ToolDispatcher()
        res = dispatcher.dispatch("lookup_stock_ticker", {"symbol": "AAPL"})
        self.assertTrue(res["success"])
        self.assertEqual(res["output"]["symbol"], "AAPL")
        self.assertEqual(res["output"]["price"], 232.50)


if __name__ == "__main__":
    unittest.main()
