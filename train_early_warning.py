import pandas as pd
import numpy as np
import joblib

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.ensemble import GradientBoostingClassifier

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix,
    classification_report
)


# ============================================================
# 1. LOAD DATASET
# ============================================================

print("\n========================================")
print("LANDSLIDE EARLY WARNING MODEL - V2")
print("========================================")

df = pd.read_csv("ner_combined_dataset.csv")

print("\nDataset shape:", df.shape)


# ============================================================
# 2. REMOVE POST-EVENT / LEAKAGE FEATURES
# ============================================================

removed_columns = [
    "label",
    "event_date",
    "landslide_trigger",
    "landslide_size"
]

print("\nRemoving columns:")
for column in removed_columns:
    print(" -", column)


# ============================================================
# 3. CREATE X AND y
# ============================================================

X = df.drop(columns=removed_columns)

y = df["label"]


print("\nInput features:", X.shape[1])
print("Target samples:", len(y))


# ============================================================
# 4. IDENTIFY NUMERICAL AND CATEGORICAL FEATURES
# ============================================================

categorical_features = X.select_dtypes(
    include=["object"]
).columns.tolist()

numerical_features = X.select_dtypes(
    exclude=["object"]
).columns.tolist()


print("\nNumerical features:")
print(numerical_features)

print("\nCategorical features:")
print(categorical_features)


# ============================================================
# 5. TRAIN / TEST SPLIT
# ============================================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)


print("\nTraining samples:", len(X_train))
print("Testing samples :", len(X_test))


# ============================================================
# 6. NUMERICAL PREPROCESSING
# ============================================================

numeric_pipeline = Pipeline(
    steps=[
        (
            "imputer",
            SimpleImputer(strategy="median")
        )
    ]
)


# ============================================================
# 7. CATEGORICAL PREPROCESSING
# ============================================================

categorical_pipeline = Pipeline(
    steps=[
        (
            "imputer",
            SimpleImputer(strategy="most_frequent")
        ),
        (
            "onehot",
            OneHotEncoder(
                handle_unknown="ignore",
                sparse_output=False
            )
        )
    ]
)


# ============================================================
# 8. COMBINE PREPROCESSING
# ============================================================

preprocessor = ColumnTransformer(
    transformers=[
        (
            "numeric",
            numeric_pipeline,
            numerical_features
        ),
        (
            "categorical",
            categorical_pipeline,
            categorical_features
        )
    ]
)


# ============================================================
# 9. CREATE GRADIENT BOOSTING MODEL
# ============================================================

model = GradientBoostingClassifier(
    n_estimators=200,
    learning_rate=0.05,
    max_depth=3,
    random_state=42
)


# ============================================================
# 10. CREATE COMPLETE PIPELINE
# ============================================================

pipeline = Pipeline(
    steps=[
        (
            "preprocessor",
            preprocessor
        ),
        (
            "model",
            model
        )
    ]
)


# ============================================================
# 11. TRAIN MODEL
# ============================================================

print("\n========================================")
print("TRAINING MODEL...")
print("========================================")

pipeline.fit(X_train, y_train)

print("Training completed successfully!")


# ============================================================
# 12. PREDICTIONS
# ============================================================

y_pred = pipeline.predict(X_test)

y_probability = pipeline.predict_proba(
    X_test
)[:, 1]


# ============================================================
# 13. EVALUATION
# ============================================================

accuracy = accuracy_score(
    y_test,
    y_pred
)

precision = precision_score(
    y_test,
    y_pred
)

recall = recall_score(
    y_test,
    y_pred
)

f1 = f1_score(
    y_test,
    y_pred
)

roc_auc = roc_auc_score(
    y_test,
    y_probability
)


print("\n========================================")
print("MODEL PERFORMANCE")
print("========================================")

print(
    f"Accuracy  : {accuracy * 100:.2f}%"
)

print(
    f"Precision : {precision * 100:.2f}%"
)

print(
    f"Recall    : {recall * 100:.2f}%"
)

print(
    f"F1 Score  : {f1 * 100:.2f}%"
)

print(
    f"ROC-AUC   : {roc_auc:.4f}"
)


# ============================================================
# 14. CONFUSION MATRIX
# ============================================================

cm = confusion_matrix(
    y_test,
    y_pred
)


print("\n========================================")
print("CONFUSION MATRIX")
print("========================================")

print(cm)


# ============================================================
# 15. CLASSIFICATION REPORT
# ============================================================

print("\n========================================")
print("CLASSIFICATION REPORT")
print("========================================")

print(
    classification_report(
        y_test,
        y_pred,
        target_names=[
            "No Landslide",
            "Landslide"
        ]
    )
)


# ============================================================
# 16. SAVE MODEL
# ============================================================

model_filename = (
    "landslide_early_warning_model.pkl"
)

joblib.dump(
    pipeline,
    model_filename
)


print("\n========================================")
print("MODEL SAVED")
print("========================================")

print(
    "Saved as:",
    model_filename
)

print("\nV2 EARLY WARNING MODEL COMPLETE!")