import pandas as pd
import joblib


# ==========================================
# LOAD DATASET
# ==========================================

df = pd.read_csv("ner_combined_dataset.csv")

print("Dataset loaded.")
print("Dataset shape:", df.shape)


# ==========================================
# LOAD V2 MODEL
# ==========================================

model = joblib.load(
    "landslide_early_warning_model.pkl"
)

print("V2 model loaded successfully.")


# ==========================================
# SELECT ONE REAL DATASET ROW
# ==========================================

sample = df.drop(
    columns=[
        "label",
        "event_date",
        "landslide_trigger",
        "landslide_size"
    ]
).iloc[0:1]


# ==========================================
# PREDICTION
# ==========================================

prediction = model.predict(sample)[0]

probability = model.predict_proba(
    sample
)[0][1]


# ==========================================
# RISK LEVEL
# ==========================================

if probability >= 0.75:
    risk = "VERY HIGH"

elif probability >= 0.50:
    risk = "HIGH"

elif probability >= 0.25:
    risk = "MODERATE"

else:
    risk = "LOW"


# ==========================================
# DISPLAY RESULT
# ==========================================

print("\n===================================")
print("V2 EARLY WARNING PREDICTION")
print("===================================")

print(
    "Latitude :",
    sample["latitude"].iloc[0]
)

print(
    "Longitude:",
    sample["longitude"].iloc[0]
)

print(
    "State    :",
    sample["state"].iloc[0]
)

print(
    "District :",
    sample["district"].iloc[0]
)

print(
    "Prediction:",
    prediction
)

print(
    "Probability:",
    round(probability * 100, 2),
    "%"
)

print(
    "Risk level:",
    risk
)