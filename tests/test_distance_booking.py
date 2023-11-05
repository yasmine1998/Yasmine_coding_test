import unittest
from src.distance_booking import lambda_handler

class TestLambdaHandler(unittest.TestCase):

    def test_lambda_handler(self):
        first_file = "data/test_event.json"
        second_file = "data/test_event2.json"
        response1 = lambda_handler(first_file ,None)
        response2 = lambda_handler(second_file ,None)
        expected_result1 = {'status': 200, 'body': [{'booking_id': 11111111, 'distance_km': 878.3185627120531}]}
        expected_result2 = {'status': 200, 'body': [{'booking_id': 11111111, 'distance_km': 878.3185627120531}, {'booking_id': 222222222, 'distance_km': 1654.6764554180818}]}
        self.assertEqual(response1, expected_result1)
        self.assertEqual(response2, expected_result2)

if __name__ == '__main__':
    unittest.main()