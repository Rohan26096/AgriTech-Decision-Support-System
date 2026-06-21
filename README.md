# 🌱 Crop Recommendation System

Crop Recommendation System is a Machine Learning-powered web application that helps farmers and agricultural enthusiasts identify the most suitable crop based on soil characteristics and environmental conditions. The system uses a trained Random Forest model to provide accurate crop recommendations from user-provided inputs.

## 🚀 Features

### Smart Crop Prediction

* Predicts the most suitable crop based on soil parameters
* Considers Nitrogen (N), Phosphorus (P), Potassium (K), pH, and Soil Moisture
* Uses a Random Forest Classifier for accurate recommendations
* Provides real-time predictions through an interactive web interface

## 🛠️ Technology Stack

* **Backend:** Flask (Python)
* **Machine Learning:** Scikit-learn (Random Forest Classifier)
* **Frontend:** HTML5, CSS3
* **Data Processing:** Pandas, NumPy

## Screenshots

### Home Page

![Home Page](screenshots/home.png)

### Prediction Result

![Prediction Result](screenshots/prediction.png)


## 📋 Installation

1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/Crop-Recommendation-System.git
cd Crop-Recommendation-System
```

2. Create a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies

```bash
pip install -r requirements.txt
```

4. Run the application

```bash
python3 app.py
```

5. Open your browser and visit:

```text
http://127.0.0.1:5001
```

## 📁 Project Structure

```text
Crop-Recommendation/
├── data/
│   └── fertilizer.csv
├── models/
│   └── crop_model.pkl
├── static/
│   └── style.css
├── templates/
│   └── index.html
├── app.py
├── train.py
├── requirements.txt
└── README.md
```

## 🤖 Machine Learning Model

### Crop Prediction Model

* **Algorithm:** Random Forest Classifier
* **Input Features:**

  * Nitrogen (N)
  * Phosphorus (P)
  * Potassium (K)
  * pH
  * Soil Moisture
* **Output:** Recommended Crop

## 🌾 Supported Crops

The model can recommend various crops including:

* Rice
* Maize
* Chickpea
* Kidneybeans
* Pigeonpeas
* Mothbeans
* Mungbean
* Blackgram
* Lentil
* Pomegranate
* Banana
* Mango
* Grapes
* Watermelon
* Muskmelon
* Coconut
* Cotton
* Jute
* Coffee

## 🎯 Future Improvements

* Fertilizer Recommendation System
* Weather API Integration
* Enhanced UI/UX
* Cloud Deployment
* Mobile Responsive Design

## 👨‍💻 Author

**Rohan**

Artificial Intelligence | Machine Learning Enthusiast

---

🌱 Leveraging Machine Learning for Smarter Agricultural Decisions 🌱
