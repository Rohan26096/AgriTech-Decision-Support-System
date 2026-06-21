import pickle
from flask import Flask, render_template, request
import pandas as pd

with open("models/crop_model.pkl", "rb") as f:
    model = pickle.load(f)

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html", prediction=None)

@app.route("/predict", methods=["POST"])
def predict():

    N = int(request.form["N"])
    P = int(request.form["P"])
    K = int(request.form["K"])
    ph = float(request.form["ph"])
    soil_moisture = int(request.form["soil_moisture"])


    input_data = pd.DataFrame({
        "N": [N],
        "P": [P],
        "K": [K],
        "pH": [ph],
        "soil_moisture": [soil_moisture]
    })

    prediction = model.predict(input_data)

    return render_template(
        "index.html",
        prediction=prediction[0]
    )

if __name__ == "__main__":
    app.run(debug=False, use_reloader=False, port=5001)