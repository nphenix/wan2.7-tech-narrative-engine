import importlib.util
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def _load_pipeline_module():
    file_path = ROOT / "pipeline.py"
    spec = importlib.util.spec_from_file_location("wan27_pipeline_test", file_path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


pipeline_module = _load_pipeline_module()
PAGE_DEFINITIONS = pipeline_module.PAGE_DEFINITIONS


class PageDefinitionsTest(unittest.TestCase):
    def test_page_definitions_match_user_confirmed_11_page_structure(self) -> None:
        self.assertEqual(11, len(PAGE_DEFINITIONS))
        page_ids = [page["page_id"] for page in PAGE_DEFINITIONS]
        self.assertEqual(
            [
                "page_1_opening",
                "page_2_wan27_api",
                "page_3_copaw_agentscope_architecture",
                "page_4_six_skill_flow",
                "page_5_ai_drama_factory_value",
                "page_6_capability_layers",
                "page_7_main_proof",
                "page_8_single_page_flow",
                "page_9_review_gates",
                "page_10_deliverables",
                "page_11_closing",
            ],
            page_ids,
        )

    def test_page_definitions_have_expected_layout_templates_for_key_pages(self) -> None:
        pages_by_id = {page["page_id"]: page for page in PAGE_DEFINITIONS}
        self.assertEqual("hero_opening", pages_by_id["page_1_opening"]["layout_template"])
        self.assertEqual("uml_capability_map", pages_by_id["page_2_wan27_api"]["layout_template"])
        self.assertEqual("uml_component_architecture", pages_by_id["page_3_copaw_agentscope_architecture"]["layout_template"])
        self.assertEqual("uml_activity_flow", pages_by_id["page_4_six_skill_flow"]["layout_template"])
        self.assertEqual("value_cards", pages_by_id["page_5_ai_drama_factory_value"]["layout_template"])
        self.assertEqual("layer_mapping", pages_by_id["page_6_capability_layers"]["layout_template"])
        self.assertEqual("uml_system_architecture", pages_by_id["page_7_main_proof"]["layout_template"])
        self.assertEqual("uml_gated_activity", pages_by_id["page_8_single_page_flow"]["layout_template"])
        self.assertEqual("uml_state_gate", pages_by_id["page_9_review_gates"]["layout_template"])
        self.assertEqual("delivery_matrix", pages_by_id["page_10_deliverables"]["layout_template"])
        self.assertEqual("closing_manifesto", pages_by_id["page_11_closing"]["layout_template"])


if __name__ == "__main__":
    unittest.main()
