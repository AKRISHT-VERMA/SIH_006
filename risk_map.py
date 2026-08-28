import pandas as pd

from prediction_v2 import predict_landslide_v2


# ============================================================
# LOAD DATASET
# ============================================================

df = pd.read_csv("ner_combined_dataset.csv")


# ============================================================
# GENERATE RISK MAP DATA
# ============================================================

def generate_risk_map():

    results = []

    # Remove columns that cannot be used for prediction
    prediction_df = df.drop(
        columns=[
            "label",
            "event_date",
            "landslide_trigger",
            "landslide_size"
        ]
    )

    # Predict every location
    predictions = model_predict(prediction_df)

    for i in range(len(df)):

        probability = predictions[i]["probability"]

        risk = predictions[i]["risk"]

        results.append({

            "latitude": float(
                df.iloc[i]["latitude"]
            ),

            "longitude": float(
                df.iloc[i]["longitude"]
            ),

            "state": df.iloc[i]["state"],

            "district": df.iloc[i]["district"],

            "probability": probability,

            "risk": risk
        })

    return results


# ============================================================
# MODEL PREDICTION
# ============================================================

def model_predict(data):

    predictions = []

    for i in range(len(data)):

        sample = data.iloc[i].to_dict()

        result = predict_landslide_v2(sample)

        predictions.append(result)

    return predictions