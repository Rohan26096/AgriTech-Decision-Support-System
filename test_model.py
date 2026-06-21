import pickle

with open("models/crop_model.pkl", "rb") as f:
    model = pickle.load(f)

prediction = model.predict([[80, 40, 40, 5.5, 30]])

print("Predicted Crop:", prediction[0])