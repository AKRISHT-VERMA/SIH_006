import pandas as pd

df = pd.read_csv("ner_combined_dataset.csv")

print("\n==============================")
print("EARLY WARNING DATA CHECK")
print("==============================")

print("\nDataset shape:")
print(df.shape)

print("\nLabel distribution:")
print(df["label"].value_counts())

print("\n------------------------------")
print("EVENT COLUMN INFORMATION")
print("------------------------------")

for column in [
    "event_date",
    "landslide_trigger",
    "landslide_size"
]:
    print("\nColumn:", column)

    print("Missing values:",
          df[column].isna().sum())

    print("Non-missing values:",
          df[column].notna().sum())

    print("Unique values:")
    print(df[column].dropna().unique()[:20])


print("\n------------------------------")
print("FEATURE COLUMNS")
print("------------------------------")

for column in df.columns:
    print(
        column,
        "-> missing:",
        df[column].isna().sum()
    )