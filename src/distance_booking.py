import argparse
import json
import pandas as pd

def lambda_handler(event: dict, context):
    path_airport = "data/output_airport_distance.csv"
    airport_distance = pd.read_csv(path_airport)

    with open(event) as f:
      event_file = json.load(f)
    
    # Create a new list of dictionaries with required keys for each booking
    booking_list = [{'booking_id': d['Booking']["Info"]["BookingId"], 'Journeys': d['Booking']["Journeys"]} for d in event_file["detail"]["Events"]]  

    # Use a list to extract airport combinations for the specified booking
    airport_combinations = [
        (segment['AirportOrig'], segment['AirportDest'], booking['booking_id'])
        for booking in booking_list
        for journey in booking['Journeys']
        for segment in journey['Segments']
    ]

    # Create a DataFrame from the combinations with booking_id
    df_combinations = pd.DataFrame(airport_combinations, columns=['origin_airport', 'destination_airport', 'booking_id'])

    # Merge with airport_distance to get distances for the specified combinations
    merged_distances = pd.merge(df_combinations, airport_distance, on=['origin_airport', 'destination_airport'], how='inner')

    # Calculate the sum of distances for the specified combinations
    sum_of_distances = merged_distances.groupby('booking_id')['distance_km'].sum()

    final_result = [{'booking_id': booking['booking_id'], 'distance_km': sum_of_distances.get(booking['booking_id'], 0)} for booking in booking_list]

    return {"status": 200, "body": final_result}


if __name__ == '__main__':
    response = lambda_handler("data/test_event2.json",None)
    print(response)