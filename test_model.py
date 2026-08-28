import joblib

model = joblib.load("landslide_final_model.pkl")

print("Model loaded successfully!")
print(model.keys())