import argparse
import pandas as pd
from geopy.distance import geodesic


def main():
    path = read_arg_path()
    df_airport = extract(path)
    result_df = transform(df_airport)
    load("data/output_airport_distance.csv", result_df)


def read_arg_path():
    parser = argparse.ArgumentParser(
        prog='ComputeDistances',
        description='Compute distances between airports')
    parser.add_argument('file')
    args = parser.parse_args()
    return args.file

def convert_dms_to_decimal(dms):
    degrees = int(dms[:2])
    minutes = int(dms[2:4])
    seconds = int(dms[4:6])
    decimal_degrees = degrees + (minutes / 60) + (seconds / 3600)
    return decimal_degrees

# Function to calculate distance between two airports
def calculate_distance(row):
    try:
        origin_coords = (convert_dms_to_decimal(row['latitude_origin']), convert_dms_to_decimal(row['longitude_origin']))
        destination_coords = (convert_dms_to_decimal(row['latitude_destination']), convert_dms_to_decimal(row['longitude_destination']))
        distance = geodesic(origin_coords, destination_coords).kilometers
        return distance
    except (ValueError, TypeError):
        return None

def extract(file_path):
    return pd.read_csv(file_path)

def transform(df_airport):
    # Remove duplicate rows
    df_airport = df_airport.drop_duplicates()

    # Merge the DataFrame with itself to get all combinations
    combinations = df_airport.merge(df_airport, how='cross', suffixes=('_origin', '_destination'))

    # Filter out rows where origin and destination are the same
    combinations = combinations[combinations['stationcode_origin'] != combinations['stationcode_destination']]
    
    # Apply the calculate_distance function to calculate distances
    combinations['distance_km'] = combinations.apply(calculate_distance, axis=1)

    # Add a new column based on the condition (distance > 200)
    combinations['is_less_than_200_km'] = combinations['distance_km'].apply(lambda x: x < 200)
    
    # Rename columns as requested
    combinations = combinations.rename(columns={'stationcode_origin': 'origin_airport', 'stationcode_destination': 'destination_airport'})
                                    
    # Keep only necessary columns
    result_df = combinations[['origin_airport', 'destination_airport', 'distance_km', 'is_less_than_200_km']]

    return result_df

def load(output_path, transformed_df):
    transformed_df.to_csv(output_path, index=False)

if __name__ == '__main__':
    main()