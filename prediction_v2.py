import pandas as pd
import joblib


# ============================================================
# LOAD V2 EARLY WARNING MODEL
# ============================================================

MODEL_PATH = "landslide_early_warning_model.pkl"

model = joblib.load(MODEL_PATH)

print("V2 Early Warning Model loaded successfully.")


# ============================================================
# PREDICTION FUNCTION
# ============================================================

def predict_landslide_v2(sample):

    # Convert dictionary into DataFrame
    sample_df = pd.DataFrame([sample])

    # Make prediction
    prediction = int(
        model.predict(sample_df)[0]
    )

    # Get probability of landslide
    probability = float(
        model.predict_proba(sample_df)[0][1]
    )

    probability_percent = round(
        probability * 100,
        2
    )


    # ========================================================
    # RISK CLASSIFICATION
    # ========================================================

    if probability >= 0.75:

        risk = "VERY HIGH"

    elif probability >= 0.50:

        risk = "HIGH"

    elif probability >= 0.25:

        risk = "MODERATE"

    else:

        risk = "LOW"


    # ========================================================
    # RETURN RESULT
    # ========================================================

    return {
        "prediction": prediction,
        "probability": probability_percent,
        "risk": risk
    }