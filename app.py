import streamlit as st
from pricing_engine import predict_fare
from PIL import Image

# Set page config
st.set_page_config(
    page_title="Airfare Predictor",
    page_icon="✈️",
    layout="wide"
)

# ---------- Center the Logo ----------
logo = Image.open("logo.png")
logo_col1, logo_col2, logo_col3 = st.columns([1, 2, 1])
with logo_col2:
    st.image(logo, use_container_width=False, width=250)

# ---------- Add Styling ----------
st.markdown(
    """
    <style>
    .form-container {
        background-color: #f0f2f6;
        padding: 25px;
        border-radius: 15px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        border: 1px solid #d9d9d9;
        margin-top: 20px;
    }
    .center-header {
        text-align: center;
        color: #333333;
    }

    @media (prefers-color-scheme: dark) {
        .form-container {
            background-color: #1e1e1e;
            border: 1px solid #444;
        }
        .center-header {
            color: #f0f2f6;
        }
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ---------- Start the Form Container ----------
st.markdown('<div class="form-container">', unsafe_allow_html=True)

# Centered Header
st.markdown("<h2 class='center-header'>Flight Search</h2>", unsafe_allow_html=True)

# Row 1
col_a, col_b = st.columns(2)
with col_a:
    journey_day = st.selectbox("Day of Journey", ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])
with col_b:
    airline = st.selectbox("Airline", ["Indigo", "Air India", "SpiceJet", "Vistara", "GoAir", "Jet Airways"])

# Row 2
col_c, col_d = st.columns(2)
with col_c:
    flight_class = st.selectbox("Class", ["Economy", "Business"])
with col_d:
    source = st.selectbox("Source City", ["Delhi", "Mumbai", "Chennai", "Kolkata", "Bangalore"])

# Row 3
col_e, col_f = st.columns(2)
with col_e:
    destination = st.selectbox("Destination City", ["Delhi", "Mumbai", "Chennai", "Kolkata", "Bangalore"])
with col_f:
    departure = st.selectbox("Departure Time", ["Before 6 AM", "6 AM - 12 PM", "12 PM - 6 PM", "After 6 PM"])

# Row 4
col_g, col_h = st.columns(2)
with col_g:
    total_stops = st.selectbox("Total Stops", ["non-stop", "1 stop", "2 stops"])
with col_h:
    duration = st.number_input("Flight Duration (in hours)", min_value=1.0, max_value=15.0, value=2.5, step=0.1)

# Row 5
days_left = st.slider("Days Left to Departure", min_value=0, max_value=180, value=30)

# Predict Button with Loading Spinner
if st.button("🔍 Predict Fare"):
    with st.spinner("Predicting fare..."):
        if source == destination:
            st.error("Source and Destination cannot be the same. Please select different cities.")
        else:
            input_data = {
                "Journey_day": journey_day,
                "Airline": airline,
                "Class": flight_class,
                "Source": source,
                "Departure": departure,
                "Total_stops": total_stops,
                "Destination": destination,
                "Duration_in_hours": duration,
                "Days_left": days_left
            }

            # Example dynamic pricing adjustment
            days_left_discount = max(0.8, 1.0 - (days_left / 200))
            result = predict_fare(input_data)

            if isinstance(result, tuple):
                final_fare, base_fare = result
                adjusted_fare = round(final_fare * days_left_discount, 2)

                st.success(f"Predicted Base Fare: ₹{base_fare}")
                st.info(f"Dynamic Adjusted Fare (after early booking discount): ₹{adjusted_fare}")
            else:
                st.error(result)

# ---------- End the Form Container ----------
st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.write("---")
st.caption("Prototype dynamic pricing engine | For demonstration purposes only")
