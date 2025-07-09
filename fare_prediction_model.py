import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
import joblib

# Load dataset
df = pd.read_csv("Cleaned_dataset.csv")

# Drop unused/redundant columns
df.drop(columns=["Date_of_journey", "Flight_code", "Arrival"], inplace=True)

# Encode categorical columns
categorical_cols = ["Journey_day", "Airline", "Class", "Source", "Departure", "Total_stops", "Destination"]
label_encoders = {}

for col in categorical_cols:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])
    label_encoders[col] = le

# Features and target
X = df.drop("Fare", axis=1)
y = df["Fare"]

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Random Forest Model
model = RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1)
model.fit(X_train, y_train)

# Predictions
y_pred = model.predict(X_test)

# Evaluation
mae = mean_absolute_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"MAE: ₹{mae:.2f}")
print(f"R² Score: {r2:.4f}")

# Save model and encoders
joblib.dump(model, "fare_model.pkl")
joblib.dump(label_encoders, "encoders.pkl")
