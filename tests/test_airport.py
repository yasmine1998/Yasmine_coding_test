import unittest
import os
from io import StringIO
import pandas as pd
from unittest.mock import patch

from src.airport import read_arg_path, convert_dms_to_decimal, calculate_distance, extract, transform, load

class TestAirportDistances(unittest.TestCase):

    def test_convert_dms_to_decimal(self):
        result = convert_dms_to_decimal('514536N')
        self.assertAlmostEqual(result, 51.76, places=2)

    def test_calculate_distance(self):
        row = {
            'latitude_origin': '514536N',
            'longitude_origin': '0000939W',
            'latitude_destination': '523131N',
            'longitude_destination': '0000910W'
        }
        result = calculate_distance(row)
        self.assertAlmostEqual(result, 85.15, places=2)

    def test_transform(self):
        input_df = pd.DataFrame({
            'stationcode': ['AAA', 'BBB'],
            'latitude': ['514536N', '523131N'],
            'longitude': ['0000939W', '0000910W']
        })
        result = transform(input_df)
        self.assertEqual(result.shape[0], 2)

    def test_load(self):
        input_df = pd.DataFrame({
            'origin_airport': ['AAA', 'BBB'],
            'destination_airport': ['CCC', 'DDD'],
            'distance_km': [100, 200],
            'is_less_than_200_km': [True, False]
        })
        output_path = 'test_output.csv'
        load(output_path, input_df)

        with open(output_path, 'r') as f:
            content = f.read()
            self.assertIn('AAA', content)
            self.assertIn('BBB', content)
            self.assertIn('CCC', content)
            self.assertIn('DDD', content)

        # Clean up the test output file after the test
        os.remove(output_path)

if __name__ == '__main__':
    unittest.main()