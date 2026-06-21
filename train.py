import pandas as pd

df = pd.read_csv("data/fertilizer.csv")

print(df.head())
print()
print(df.shape)
print()
print(df.columns)
print(df.info())
print()
print(df.describe())

df = df.drop("Unnamed: 0", axis=1)

X = df.drop("Crop", axis=1)
y = df["Crop"]

print(X.head())
print()
print(y.head())

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

model = RandomForestClassifier(random_state=42)

model.fit(X_train, y_train)

accuracy = model.score(X_test, y_test)

print("\nAccuracy:", accuracy)


import pickle

with open("models/crop_model.pkl", "wb") as f:
    pickle.dump(model, f)

print("Model saved successfully!")