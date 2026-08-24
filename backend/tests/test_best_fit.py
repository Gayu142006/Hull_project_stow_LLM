import unittest
from app.optimization.best_fit import calculate_best_fit

class TestBestFit(unittest.TestCase):

    def test_best_fit_success(self):
        item = {
            "item_id": "ITEM001",
            "length_cm": 20,
            "width_cm": 15,
            "height_cm": 10,
            "weight_kg": 2.5,
            "category": "general"
        }
        
        locations = [
            {
                "location_id": "A-01",
                "available_length_cm": 22,
                "available_width_cm": 17,
                "available_height_cm": 12,
                "weight_capacity_kg": 10,
                "status": "AVAILABLE"
            },
            {
                "location_id": "A-02",
                "available_length_cm": 15,
                "available_width_cm": 15,
                "available_height_cm": 10,
                "weight_capacity_kg": 10,
                "status": "AVAILABLE"
            }
        ]
        
        result = calculate_best_fit(item, locations)
        
        self.assertEqual(result["recommended_location"], "A-01")
        self.assertGreater(result["space_utilisation_percent"], 60)
        self.assertEqual(len(result["alternative_locations"]), 0)

    def test_best_fit_heavy_item(self):
        item = {
            "item_id": "ITEM002",
            "length_cm": 20,
            "width_cm": 15,
            "height_cm": 10,
            "weight_kg": 20, # Heavy
            "category": "general"
        }
        
        locations = [
            {
                "location_id": "A-01",
                "available_length_cm": 22,
                "available_width_cm": 17,
                "available_height_cm": 12,
                "weight_capacity_kg": 10, # Not enough capacity
                "status": "AVAILABLE"
            }
        ]
        
        result = calculate_best_fit(item, locations)
        
        self.assertIsNone(result["recommended_location"])
        
    def test_best_fit_rotations(self):
        # Item needs to be rotated to fit
        item = {
            "item_id": "ITEM003",
            "length_cm": 10,
            "width_cm": 20,
            "height_cm": 15,
            "weight_kg": 2.5,
            "category": "general"
        }
        
        locations = [
            {
                "location_id": "A-01",
                "available_length_cm": 22, # width 20 fits here
                "available_width_cm": 17,  # height 15 fits here
                "available_height_cm": 12, # length 10 fits here
                "weight_capacity_kg": 10,
                "status": "AVAILABLE"
            }
        ]
        
        result = calculate_best_fit(item, locations)
        
        self.assertEqual(result["recommended_location"], "A-01")

if __name__ == '__main__':
    unittest.main()
