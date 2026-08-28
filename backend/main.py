from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from weather import get_weather
from weather import get_rainfall_forecast
from warning_engine import calculate_warning

import sys
import os


# ============================================================
# FIND PROJECT ROOT
# ============================================================

PROJECT_ROOT = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

FRONTEND_PATH = os.path.join(
    PROJECT_ROOT,
    "frontend"
)

sys.path.append(PROJECT_ROOT)


# ============================================================
# IMPORT V2 MODEL
# ============================================================

from prediction_v2 import predict_landslide_v2


# ============================================================
# CREATE FASTAPI APP
# ============================================================

app = FastAPI(
    title="Northeast India Landslide Early Warning API",
    description="ML-based pre-event landslide risk prediction system",
    version="2.0"
)
app.mount(
    "/static",
    StaticFiles(
        directory=FRONTEND_PATH
    ),
    name="static"
)

@app.get("/app")
def frontend():

    return FileResponse(
        os.path.join(
            FRONTEND_PATH,
            "index.html"
        )
    )




# ============================================================
# HOME ENDPOINT
# ============================================================

@app.get("/")
def home():

    return {
        "message": "Northeast India Landslide Early Warning API is running!",
        "model": "V2 Early Warning Model"
    }


# ============================================================
# INPUT DATA MODEL
# ============================================================

class LocationData(BaseModel):

    latitude: float
    longitude: float

    state: str
    district: str

    elevation_m: float
    slope_deg: float
    aspect_deg: float

    plan_curvature: float
    profile_curvature: float
    tri: float

    annual_rainfall_mm: float
    monsoon_rainfall_mm: float
    max_daily_rainfall_mm: float

    soil_clay_pct: float
    soil_sand_pct: float
    soil_silt_pct: float

    soil_organic_carbon_pct: float
    soil_bulk_density: float
    soil_moisture_pct: float

    land_cover: str
    ndvi: float

    distance_to_road_km: float
    road_density_km_per_km2: float

    distance_to_river_km: float
    distance_to_fault_km: float

    seismic_zone: str

    population_density_per_km2: float

    historical_landslides_5km_10yr: int


# ============================================================
# V2 PREDICTION ENDPOINT
# ============================================================

@app.post("/predict")
def predict(data: LocationData):

    # Convert API input to dictionary

    input_data = data.model_dump()

    # Run V2 ML model

    result = predict_landslide_v2(
        input_data
    )

    # Add location information

    result["latitude"] = data.latitude
    result["longitude"] = data.longitude

    result["state"] = data.state
    result["district"] = data.district

    return result

from risk_map import generate_risk_map


@app.get("/risk-map")
def risk_map():

    locations = generate_risk_map()

    return {
        "count": len(locations),
        "locations": locations
    }

@app.get("/weather")
def weather(latitude: float, longitude: float):

    current = get_weather(
        latitude,
        longitude
    )

    forecast = get_rainfall_forecast(
        latitude,
        longitude
    )

    return {
        "latitude": latitude,
        "longitude": longitude,

        "temperature":
            current["current"]["temperature_2m"],

        "humidity":
            current["current"]["relative_humidity_2m"],

        "current_rain":
            current["current"]["rain"],

        "current_precipitation":
            current["current"]["precipitation"],

        "rainfall_next_24h":
            forecast["rainfall_next_24h"],

        "max_rain_probability":
            forecast["max_rain_probability"]
    }

@app.get("/early-warning")
def early_warning(
    latitude: float,
    longitude: float,
    ml_probability: float
):

    # Get live weather

    current = get_weather(
        latitude,
        longitude
    )

    forecast = get_rainfall_forecast(
        latitude,
        longitude
    )


    # Get rainfall values

    rainfall = forecast[
        "rainfall_next_24h"
    ]

    rain_probability = forecast[
        "max_rain_probability"
    ]


    # Calculate hybrid warning

    warning = calculate_warning(
        ml_probability=ml_probability,
        rainfall_next_24h=rainfall,
        rain_probability=rain_probability
    )


    return {

        "latitude": latitude,

        "longitude": longitude,

        "ml_probability":
            ml_probability,

        "rainfall_next_24h":
            rainfall,

        "rain_probability":
            rain_probability,

        "warning_score":
            warning["score"],

        "warning":
            warning["warning"]

    }