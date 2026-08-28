import pandas as pd
import joblib


# --------------------------------------------------
# LOAD MODEL
# --------------------------------------------------

saved_model = joblib.load("landslide_final_model.pkl")
model = saved_model["model"]


# --------------------------------------------------
# LOAD DATASET
# --------------------------------------------------

df = pd.read_csv("ner_combined_dataset.csv")

# Remove target column
X = df.drop(columns=["label"])

# Create the same dummy variables used during training
X_encoded = pd.get_dummies(X, drop_first=True)

# Get the exact columns expected by the trained model
expected_features = model.feature_names_in_


# --------------------------------------------------
# PREDICTION FUNCTION
# --------------------------------------------------

def predict_landslide(sample):

    # Convert input into DataFrame
    sample = pd.DataFrame([sample])

    # Convert categorical variables to dummy variables
    sample_encoded = pd.get_dummies(
        sample,
        drop_first=True
    )

    # Make sure columns match the trained model
    sample_encoded = sample_encoded.reindex(
        columns=expected_features,
        fill_value=0
    )

    # Make prediction
    prediction = model.predict(sample_encoded)[0]

    # Get probability
    probability = model.predict_proba(
        sample_encoded
    )[0][1]

    # Convert probability into percentage
    probability_percent = probability * 100

    # Determine risk
    if probability_percent < 20:
        risk = "LOW"

    elif probability_percent < 40:
        risk = "MODERATE"

    elif probability_percent < 60:
        risk = "HIGH"

    else:
        risk = "VERY HIGH"

    return {
        "prediction": int(prediction),
        "probability": round(probability_percent, 2),
        "risk": risk
    }


# --------------------------------------------------
# TEST THE FUNCTION
# --------------------------------------------------

sample = X.iloc[0].to_dict()

result = predict_landslide(sample)


print("\n-----------------------------")
print("LANDSLIDE PREDICTION")
print("-----------------------------")

print("Latitude :", sample["latitude"])
print("Longitude:", sample["longitude"])

print("Prediction :", result["prediction"])

print(
    "Probability :",
    result["probability"],
    "%"
)

print("Risk level  :", result["risk"])