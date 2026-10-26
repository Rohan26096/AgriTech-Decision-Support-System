
import os
import math
import pickle

import pandas as pd
from flask import Flask, render_template, request


# --------------------------------------------------
# APP AND MODEL SETUP
# --------------------------------------------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "models", "crop_model_v2.pkl")

with open(MODEL_PATH, "rb") as model_file:
    model = pickle.load(model_file)

app = Flask(__name__)

MODEL_FEATURES = [
    "N", "P", "K", "temperature", "humidity", "ph", "rainfall"
]


# --------------------------------------------------
# CROP INFORMATION
# --------------------------------------------------

crop_info = {
    "apple": {
        "season": "Regional / perennial",
        "water": "Moderate; depends on climate and orchard",
        "profit": "Varies by region and market"
    },
    "banana": {
        "season": "Can be grown year-round in suitable climates",
        "water": "High",
        "profit": "Varies by region and market"
    },
    "blackgram": {
        "season": "Kharif or suitable summer season",
        "water": "Low to moderate",
        "profit": "Varies by region and market"
    },
    "chickpea": {
        "season": "Rabi",
        "water": "Low to moderate",
        "profit": "Varies by region and market"
    },
    "coconut": {
        "season": "Perennial",
        "water": "Regular moisture required",
        "profit": "Varies by region and market"
    },
    "coffee": {
        "season": "Perennial",
        "water": "Rainfall and irrigation needs vary by region",
        "profit": "Varies by region and market"
    },
    "cotton": {
        "season": "Usually Kharif",
        "water": "Moderate to high, depending on rainfall",
        "profit": "Varies by region and market"
    },
    "grapes": {
        "season": "Perennial; harvest season varies by region",
        "water": "Carefully managed irrigation",
        "profit": "Varies by region and market"
    },
    "jute": {
        "season": "Kharif",
        "water": "High moisture and rainfall needs",
        "profit": "Varies by region and market"
    },
    "kidneybeans": {
        "season": "Varies by climate and region",
        "water": "Moderate",
        "profit": "Varies by region and market"
    },
    "lentil": {
        "season": "Rabi",
        "water": "Low to moderate",
        "profit": "Varies by region and market"
    },
    "maize": {
        "season": "Kharif and other suitable seasons",
        "water": "Moderate",
        "profit": "Varies by region and market"
    },
    "mango": {
        "season": "Perennial; fruiting is seasonal",
        "water": "Moderate; depends on tree age and climate",
        "profit": "Varies by region and market"
    },
    "mothbeans": {
        "season": "Usually Kharif in dry regions",
        "water": "Low",
        "profit": "Varies by region and market"
    },
    "mungbean": {
        "season": "Kharif, summer, or other suitable seasons",
        "water": "Low to moderate",
        "profit": "Varies by region and market"
    },
    "muskmelon": {
        "season": "Usually warm-season cultivation",
        "water": "Regular moisture; avoid waterlogging",
        "profit": "Varies by region and market"
    },
    "orange": {
        "season": "Perennial; harvest varies by variety and region",
        "water": "Regular, well-managed irrigation",
        "profit": "Varies by region and market"
    },
    "papaya": {
        "season": "Can be planted in suitable warm climates",
        "water": "Regular moisture; avoid waterlogging",
        "profit": "Varies by region and market"
    },
    "pigeonpeas": {
        "season": "Usually Kharif",
        "water": "Low to moderate once established",
        "profit": "Varies by region and market"
    },
    "pomegranate": {
        "season": "Perennial; fruiting depends on management",
        "water": "Carefully managed irrigation",
        "profit": "Varies by region and market"
    },
    "rice": {
        "season": "Often Kharif; other seasons in suitable regions",
        "water": "High in many production systems",
        "profit": "Varies by region and market"
    },
    "watermelon": {
        "season": "Usually warm-season cultivation",
        "water": "Regular moisture; avoid waterlogging",
        "profit": "Varies by region and market"
    }
}


# --------------------------------------------------
# PRICE REFERENCES
#
# Prices are MSP reference benchmarks, not live prices.
# Yield remains None until verified yield data is added.
# Therefore, revenue is not guessed or fabricated.
# --------------------------------------------------

MSP_SOURCE = (
    "https://www.pib.gov.in/"
    "PressReleasePage.aspx?PRID=2260618&lang=2&reg=3"
)

RABI_SOURCE = (
    "https://www.pib.gov.in/"
    "newsite/erelcontent.aspx?lang=2&reg=48&relid=276864"
)

profit_data = {
    "rice": {
        "yield_t_ha": None,
        "price_per_kg": 24.41,
        "price_label": "Paddy MSP (Common), Kharif 2026–27",
        "price_source": "PIB, 13 May 2026",
        "source_url": MSP_SOURCE,
        "price_note": (
            "This is the paddy support price, not a retail "
            "or milled-rice market quote."
        )
    },
    "maize": {
        "yield_t_ha": None,
        "price_per_kg": 24.10,
        "price_label": "Maize MSP, Kharif 2026–27",
        "price_source": "PIB, 13 May 2026",
        "source_url": MSP_SOURCE,
        "price_note": (
            "MSP is a support-price benchmark, not a guaranteed "
            "transaction price."
        )
    },
    "pigeonpeas": {
        "yield_t_ha": None,
        "price_per_kg": 84.50,
        "price_label": "Tur/Arhar MSP, Kharif 2026–27",
        "price_source": "PIB, 13 May 2026",
        "source_url": MSP_SOURCE,
        "price_note": "MSP benchmark for tur/arhar."
    },
    "mungbean": {
        "yield_t_ha": None,
        "price_per_kg": 87.80,
        "price_label": "Moong MSP, Kharif 2026–27",
        "price_source": "PIB, 13 May 2026",
        "source_url": MSP_SOURCE,
        "price_note": "MSP benchmark for moong/green gram."
    },
    "blackgram": {
        "yield_t_ha": None,
        "price_per_kg": 82.00,
        "price_label": "Urad MSP, Kharif 2026–27",
        "price_source": "PIB, 13 May 2026",
        "source_url": MSP_SOURCE,
        "price_note": "MSP benchmark for urad/black gram."
    },
    "cotton": {
        "yield_t_ha": None,
        "price_per_kg": 82.67,
        "price_label": "Cotton MSP, medium staple, Kharif 2026–27",
        "price_source": "PIB, 13 May 2026",
        "source_url": MSP_SOURCE,
        "price_note": (
            "This is for the specified cotton category; "
            "it is not directly comparable with lint or retail prices."
        )
    },
    "chickpea": {
        "yield_t_ha": None,
        "price_per_kg": 58.75,
        "price_label": "Gram MSP, Rabi 2026–27",
        "price_source": "PIB, 1 October 2025",
        "source_url": RABI_SOURCE,
        "price_note": "Government MSP benchmark for gram/chickpea."
    },
    "lentil": {
        "yield_t_ha": None,
        "price_per_kg": 70.00,
        "price_label": "Lentil (Masur) MSP, Rabi 2026–27",
        "price_source": "PIB, 1 October 2025",
        "source_url": RABI_SOURCE,
        "price_note": "Government MSP benchmark for lentil/masur."
    },
    "jute": {
        "yield_t_ha": None,
        "price_per_kg": 56.50,
        "price_label": "Jute MSP, 2025–26",
        "price_source": "PIB, 5 August 2025",
        "source_url": (
            "https://www.pib.gov.in/"
            "PressReleasePage.aspx?PRID=2152556&lang=2&reg=3"
        ),
        "price_note": (
            "This is a 2025–26 MSP benchmark. Verify the current "
            "season before using it."
        )
    }
}


# --------------------------------------------------
# FERTILIZER RECOMMENDATION
# Simple screening only; not a substitute for a soil test.
# --------------------------------------------------


def fertilizer_recommendation(N, P, K):
    """
    Basic screening based on entered values.
    These values are not enough to calculate fertilizer dosage.
    """

    recommendations = []

    if N < 40:
        recommendations.append(
            "Nitrogen input is relatively low. Verify soil nitrogen "
            "through a soil test before deciding on fertilizer."
        )

    if P < 40:
        recommendations.append(
            "Phosphorus input is relatively low. Confirm available "
            "soil phosphorus through a soil test."
        )

    if K < 40:
        recommendations.append(
            "Potassium input is relatively low. Confirm available "
            "soil potassium through a soil test."
        )

    if not recommendations:
        recommendations.append(
            "The entered NPK values do not trigger this basic screening. "
            "This does not confirm that the soil has sufficient nutrients."
        )

    return recommendations



# --------------------------------------------------
# SOIL HEALTH
# --------------------------------------------------

def soil_health_score(N, P, K, ph):
    score = 100

    if N < 40:
        score -= 15

    if P < 40:
        score -= 15

    if K < 40:
        score -= 15

    if ph < 5.5 or ph > 8:
        score -= 20

    return max(score, 0)


def soil_status(score):
    if score >= 80:
        return "Excellent 🟢"
    elif score >= 60:
        return "Good 🟡"
    elif score >= 40:
        return "Moderate 🟠"
    return "Poor 🔴"


def nutrient_status(value):
    if value < 40:
        return "Low ⚠️"
    elif value < 80:
        return "Moderate 🟡"
    return "High 🟢"


# --------------------------------------------------
# IRRIGATION
# --------------------------------------------------


def irrigation_advice(moisture):
    if moisture < 30:
        return (
            "Low entered moisture reading. Check the sensor and "
            "crop-specific irrigation requirements."
        )

    elif moisture < 60:
        return (
            "Moderate entered moisture reading. Check soil conditions "
            "and crop requirements before irrigating."
        )

    return (
        "Higher entered moisture reading. Check the root-zone moisture "
        "and drainage before deciding whether to irrigate."
    )


# --------------------------------------------------
# REVENUE ESTIMATION
# --------------------------------------------------

def profit_estimation(crop):
    """Return a sourced price reference and revenue only if yield is known."""

    crop = str(crop).lower()
    data = profit_data.get(crop)

    if not data:
        return {
            "yield_t_ha": None,
            "price_per_kg": None,
            "price_label": "No directly comparable MSP reference found",
            "price_source": None,
            "source_url": "https://agmarknet.gov.in/",
            "price_note": (
                "Check AGMARKNET modal prices for the relevant crop, "
                "variety, and market."
            ),
            "gross_revenue": None
        }

    yield_t_ha = data.get("yield_t_ha")
    price_per_kg = data.get("price_per_kg")
    gross_revenue = None

    if yield_t_ha is not None and price_per_kg is not None:
        if yield_t_ha >= 0 and price_per_kg >= 0:
            gross_revenue = yield_t_ha * 1000 * price_per_kg

    return {
        **data,
        "gross_revenue": gross_revenue
    }


# --------------------------------------------------
# CROP RISK SCREENING
# This heuristic is not a disease diagnosis.
# --------------------------------------------------


def disease_risk(ph, moisture, N):
    """
    General monitoring guidance only.
    This is not a validated crop disease prediction model.
    """

    observations = []

    if moisture > 80:
        observations.append(
            "The entered moisture value is high. Check drainage and "
            "inspect plants for disease symptoms."
        )

    if ph < 5.5 or ph > 8.0:
        observations.append(
            "The entered pH is outside this application's broad "
            "screening range. Verify it with a soil test."
        )

    if N < 30:
        observations.append(
            "The entered nitrogen value is low relative to this "
            "screening threshold. Check crop growth and soil-test results."
        )

    if observations:
        return {
            "risk": "Needs Monitoring",
            "disease": "One or more input values need attention",
            "advice": " ".join(observations)
        }

    return {
        "risk": "Routine Monitoring",
        "disease": "No warning triggered by these simple checks",
        "advice": (
            "Continue regular crop inspections. These checks cannot "
            "rule out pests, diseases, or nutrient deficiencies."
        )
    }


# --------------------------------------------------
# DEFAULT TEMPLATE CONTEXT
# --------------------------------------------------

def empty_template_context():
    return {
        "prediction": None,
        "fertilizers": [],
        "health_score": None,
        "irrigation": None,
        "status": None,
        "crop_details": None,
        "n_status": None,
        "p_status": None,
        "k_status": None,
        "N": None,
        "P": None,
        "K": None,
        "ph": None,
        "soil_moisture": None,
        "temperature": None,
        "humidity": None,
        "rainfall": None,
        "profit": None,
        "disease": None,
        "error": None
    }


# --------------------------------------------------
# HOME PAGE
# --------------------------------------------------

@app.route("/")
def home():
    return render_template(
        "index.html",
        **empty_template_context()
    )


# --------------------------------------------------
# CROP PREDICTION
# --------------------------------------------------

@app.route("/predict", methods=["POST"])
def predict():
    try:
        N = float(request.form["N"])
        P = float(request.form["P"])
        K = float(request.form["K"])
        ph = float(request.form["ph"])
        soil_moisture = float(request.form["soil_moisture"])
        temperature = float(request.form["temperature"])
        humidity = float(request.form["humidity"])
        rainfall = float(request.form["rainfall"])

    except (KeyError, TypeError, ValueError):
        context = empty_template_context()
        context["error"] = (
            "Please enter valid numbers in every field."
        )
        return render_template("index.html", **context), 400

    values = [
        N, P, K, ph, soil_moisture,
        temperature, humidity, rainfall
    ]

    if not all(math.isfinite(value) for value in values):
        context = empty_template_context()
        context["error"] = "Inputs must be finite numbers."
        return render_template("index.html", **context), 400

    if (
        min(N, P, K, rainfall) < 0
        or not 0 <= ph <= 14
        or not 0 <= soil_moisture <= 100
        or not 0 <= humidity <= 100
        or not -10 <= temperature <= 60
    ):
        context = empty_template_context()
        context.update({
            "N": N,
            "P": P,
            "K": K,
            "ph": ph,
            "soil_moisture": soil_moisture,
            "temperature": temperature,
            "humidity": humidity,
            "rainfall": rainfall,
            "error": (
                "One or more values are outside the accepted input range."
            )
        })
        return render_template("index.html", **context), 400

    # The trained model uses these seven features.
    # Soil moisture is used only by the dashboard heuristics.
    input_data = pd.DataFrame(
        [{
            "N": N,
            "P": P,
            "K": K,
            "temperature": temperature,
            "humidity": humidity,
            "ph": ph,
            "rainfall": rainfall
        }],
        columns=MODEL_FEATURES
    )

    try:
        prediction = model.predict(input_data)[0]

    except Exception:
        app.logger.exception("Crop prediction failed")
        context = empty_template_context()
        context["error"] = (
            "Prediction failed. Check that crop_model_v2.pkl was trained "
            "with the seven expected features."
        )
        return render_template("index.html", **context), 500

    crop_name = str(prediction).lower()

    crop_details = crop_info.get(
        crop_name,
        {
            "season": "Not configured",
            "water": "Not configured",
            "profit": "Not configured"
        }
    )

    health_score = soil_health_score(N, P, K, ph)

    context = {
        "prediction": prediction,
        "fertilizers": fertilizer_recommendation(N, P, K),
        "health_score": health_score,
        "irrigation": irrigation_advice(soil_moisture),
        "status": soil_status(health_score),
        "crop_details": crop_details,
        "n_status": nutrient_status(N),
        "p_status": nutrient_status(P),
        "k_status": nutrient_status(K),
        "N": N,
        "P": P,
        "K": K,
        "ph": ph,
        "soil_moisture": soil_moisture,
        "temperature": temperature,
        "humidity": humidity,
        "rainfall": rainfall,
        "profit": profit_estimation(crop_name),
        "disease": disease_risk(ph, soil_moisture, N),
        "error": None
    }

    return render_template("index.html", **context)


if __name__ == "__main__":
    app.run(
        debug=False,
        use_reloader=False,
        port=5001
    )
