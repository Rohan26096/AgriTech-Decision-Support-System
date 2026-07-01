import pickle
from flask import Flask, render_template, request
import pandas as pd

with open("models/crop_model.pkl", "rb") as f:
    model = pickle.load(f)

app = Flask(__name__)


def fertilizer_recommendation(N, P, K):
    recommendations = []

    if N < 50:
        recommendations.append("Apply Urea (Nitrogen deficiency)")

    if P < 40:
        recommendations.append("Apply DAP (Phosphorus deficiency)")

    if K < 40:
        recommendations.append("Apply MOP (Potassium deficiency)")

    if not recommendations:
        recommendations.append("Soil nutrients are balanced")

    return recommendations


def soil_health_score(N, P, K, ph):
    score = 100

    if N < 50:
        score -= 15

    if P < 40:
        score -= 15

    if K < 40:
        score -= 15

    if ph < 5.5 or ph > 8:
        score -= 20

    return max(score, 0)

def irrigation_advice(moisture):
    if moisture < 30:
        return "High irrigation required"
    elif moisture < 60:
        return "Moderate irrigation required"
    else:
        return "No irrigation required currently"

def soil_status(score):
    if score >= 80:
        return "Excellent 🟢"
    elif score >= 60:
        return "Good 🟡"
    elif score >= 40:
        return "Moderate 🟠"
    else:
        return "Poor 🔴"

def nutrient_status(value):
    if value < 40:
        return "Deficient 🔴"
    elif value < 80:
        return "Moderate 🟡"
    else:
        return "Healthy 🟢"

def profit_estimation(crop):

    crop = crop.lower()

    if crop not in profit_data:
        return {
            "yield": 0,
            "price": 0,
            "revenue": 0
        }

    expected_yield = profit_data[crop]["yield"]
    market_price = profit_data[crop]["price"]

    revenue = expected_yield * 1000 * market_price

    return {
        "yield": expected_yield,
        "price": market_price,
        "revenue": revenue
    }
def disease_risk(ph, moisture, N):

    if moisture > 80:
        return {
            "risk": "High 🔴",
            "disease": "Fungal Infection",
            "advice": "Reduce irrigation and apply fungicide."
        }

    elif moisture > 60:
        return {
            "risk": "Medium 🟡",
            "disease": "Leaf Spot",
            "advice": "Monitor crop regularly."
        }

    elif N < 30:
        return {
            "risk": "Medium 🟡",
            "disease": "Weak Plant Growth",
            "advice": "Increase nitrogen fertilizer."
        }

    else:
        return {
            "risk": "Low 🟢",
            "disease": "Healthy Crop",
            "advice": "No immediate action required."
        }
crop_info = {
    "banana": {
        "season": "All Season",
        "water": "High",
        "profit": "High"
    },
    "rice": {
        "season": "Kharif",
        "water": "Very High",
        "profit": "Medium"
    },
    "maize": {
        "season": "Kharif",
        "water": "Moderate",
        "profit": "High"
    },
    "cotton": {
        "season": "Kharif",
        "water": "Moderate",
        "profit": "High"
    },
    "mango": {
        "season": "Summer",
        "water": "Moderate",
        "profit": "High"
    }
}
profit_data = {
    "banana": {
        "yield": 35,
        "price": 20
    },
    "rice": {
        "yield": 4.5,
        "price": 25
    },
    "maize": {
        "yield": 6,
        "price": 22
    },
    "cotton": {
        "yield": 2.5,
        "price": 65
    },
    "mango": {
        "yield": 12,
        "price": 40
    }
}
@app.route("/")
def home():
    return render_template(
        "index.html",
        prediction=None,
        fertilizers=None,
        health_score=None,
        irrigation=None,
        status=None,
        crop_details=None,
        n_status=None,
        p_status=None,
        k_status=None,
        N=None,
        P=None,
        K=None,
        profit=None,
        disease=None,
    )


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

    fertilizers = fertilizer_recommendation(N, P, K)

    health_score = soil_health_score(
        N, P, K, ph
    )
    irrigation = irrigation_advice(soil_moisture)

    status = soil_status(health_score)
    n_status = nutrient_status(N)
    p_status = nutrient_status(P)
    k_status = nutrient_status(K)

    crop_name = prediction[0].lower()

    crop_details = crop_info.get(
        crop_name,
        {
            "season": "Not Available",
            "water": "Not Available",
            "profit": "Not Available"
        }
    )
    profit = profit_estimation(crop_name)
    disease = disease_risk(ph, soil_moisture, N)

    return render_template(
        "index.html",
        prediction=prediction[0],
        fertilizers=fertilizers,
        health_score=health_score,
        irrigation=irrigation,
        status=status,
        crop_details=crop_details,
        n_status=n_status,
        p_status=p_status,
        k_status=k_status,
        N=N,
        P=P,
        K=K,
        ph=ph,
        soil_moisture=soil_moisture,
        profit=profit,
        disease=disease
    )


if __name__ == "__main__":
    app.run(debug=False, use_reloader=False, port=5001)