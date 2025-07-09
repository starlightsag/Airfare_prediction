import joblib
import numpy as np
import pandas as pd

# Load trained model and encoders
model = joblib.load("fare_model.pkl")
encoders = joblib.load("encoders.pkl")

def encode_input(input_df):
    """
    Safely encode categorical columns. If unseen category, map to most common class.
    """
    for col in encoders:
        le = encoders[col]
        # Handle unseen categories
        input_df[col] = input_df[col].apply(lambda x: x if x in le.classes_ else le.classes_[0])
        input_df[col] = le.transform(input_df[col])
    return input_df

def apply_dynamic_adjustment(base_fare, demand_factor=1.0, time_factor=1.0, competitor_factor=1.0):
    """
    Apply dynamic adjustments to the predicted fare.
    """
    adjusted_fare = base_fare * demand_factor * time_factor * competitor_factor
    return round(adjusted_fare, 2)

def predict_fare(input_dict):
    """
    Predict fare using pre-trained model and encoders.
    input_dict should have keys:
    ['Journey_day', 'Airline', 'Class', 'Source', 'Departure', 'Total_stops', 'Destination', 'Duration_in_hours', 'Days_left']
    """
    try:
        input_df = pd.DataFrame([input_dict])

        # Encode categorical columns safely
        input_df = encode_input(input_df)

        # Ensure column order
        feature_order = ['Journey_day', 'Airline', 'Class', 'Source', 'Departure',
                         'Total_stops', 'Destination', 'Duration_in_hours', 'Days_left']
        input_array = input_df[feature_order]

        # Predict base fare
        base_fare = model.predict(input_array)[0]

        # Example adjustment factors (could be based on real-time data)
        demand_factor = 1.2 if input_dict.get("Journey_day", "").lower() in ["friday", "saturday"] else 1.0
        time_factor = 1.0 if input_dict.get("Days_left", 30) > 7 else 1.15  # Increase if booking late
        competitor_factor = np.random.uniform(0.95, 1.05)  # Random adjustment simulating market shifts

        # Apply adjustments
        final_fare = apply_dynamic_adjustment(base_fare, demand_factor, time_factor, competitor_factor)

        return round(final_fare, 2), round(base_fare, 2)

    except Exception as e:
        return f"Error in fare prediction: {str(e)}"

# Example usage
if __name__ == "__main__":
    test_input = {
        'Journey_day': 'Monday',
        'Airline': 'Indigo',
        'Class': 'Economy',
        'Source': 'Delhi',
        'Departure': 'After 6 PM',
        'Total_stops': 'non-stop',
        'Destination': 'Mumbai',
        'Duration_in_hours': 2.2,
        'Days_left': 5
    }

    final_fare, base_fare = predict_fare(test_input)
    print(f"Base Fare: ₹{base_fare} | Final Adjusted Fare: ₹{final_fare}")
