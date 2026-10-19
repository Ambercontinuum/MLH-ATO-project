"""Focused tests for the deterministic stop–hazard join."""

import unittest
from unittest.mock import Mock, patch

from main import find_stop_flood_overlaps, generate_gemma_brief


def feature(geometry, **properties):
    return {"type": "Feature", "geometry": geometry, "properties": properties}


class SpatialJoinTests(unittest.TestCase):
    def setUp(self):
        self.layers = {
            "bus_stops": {
                "type": "FeatureCollection",
                "features": [
                    feature({"type": "Point", "coordinates": [0.0, 0.0]}, Stop_ID=8099),
                    feature({"type": "Point", "coordinates": [0.0001, 0.0]}, Stop_ID=8164),
                ],
            },
            "flood_zones": {
                "type": "FeatureCollection",
                "features": [
                    feature(
                        {
                            "type": "Polygon",
                            "coordinates": [[
                                [-0.00005, -0.00005],
                                [0.00005, -0.00005],
                                [0.00005, 0.00005],
                                [-0.00005, 0.00005],
                                [-0.00005, -0.00005],
                            ]],
                        },
                        FLD_AR_ID="hazard-1",
                        FLD_ZONE="AE",
                    )
                ],
            },
            "source_queries": {"bus_stops": "stops", "flood_zones": "flood"},
        }

    def test_nearest_stop_is_joined_to_polygon(self):
        result = find_stop_flood_overlaps(0, 0, 100, self.layers)
        self.assertEqual(len(result["findings"]), 1)
        self.assertEqual(result["findings"][0]["stop_id"], 8099)
        self.assertEqual(result["findings"][0]["flood_area_id"], "hazard-1")
        self.assertEqual([r["id"] for r in result["source_records"]], [8099, "hazard-1"])

    def test_nearby_polygon_does_not_count_when_stop_is_outside(self):
        self.layers["bus_stops"]["features"][0]["geometry"]["coordinates"] = [0.0001, 0]
        result = find_stop_flood_overlaps(0, 0, 100, self.layers)
        self.assertEqual(result["findings"], [])
        self.assertEqual(result["source_records"], [])

    @patch.dict("os.environ", {"GEMMA_API_KEY": "test-key"})
    @patch("main.requests.post")
    def test_gemma_receives_verified_evidence(self, post):
        result = find_stop_flood_overlaps(0, 0, 100, self.layers)
        post.return_value = Mock()
        post.return_value.json.return_value = {
            "choices": [{"message": {"content": "Verify stop 8099 on site."}}]
        }
        self.assertEqual(generate_gemma_brief(result), "Verify stop 8099 on site.")
        self.assertEqual(post.call_args.kwargs["json"]["model"], "gemma-4-31B-it")
        self.assertIn("8099", post.call_args.kwargs["json"]["messages"][1]["content"])


if __name__ == "__main__":
    unittest.main()
