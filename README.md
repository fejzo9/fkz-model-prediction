# ⚽ Football Match Outcome & Score Prediction  
## FK Željezničar & Bosnian Premier League (WWIN Liga BiH)

This project focuses on building **machine learning models for predicting football match outcomes and scores**, with a primary emphasis on **FK Željezničar Sarajevo** and the **Bosnian Premier League**.

The goal is not to “guess” match results, but to **model probabilities, expected goals, and match dynamics** using statistically and mathematically sound approaches such as **regression models** and **convolutional neural networks (CNNs)**.

---

## 🎯 Project Objectives

- Predict:
  - Match outcomes (**Win / Draw / Loss**)
  - Expected number of goals
  - Probabilities of each outcome
- Focus on:
  - FK Željezničar Sarajevo
  - Key rivals:
    - FK Sarajevo
    - FK Zrinjski
    - FK Borac
- Extend the model to the **entire Bosnian Premier League**

---

## 🧠 Modeling Approach

This project combines **classical statistical modeling** with **modern deep learning techniques**.

### 1️⃣ Regression-Based Models
Used for:
- Expected goals prediction
- Probabilistic outcome estimation

Planned techniques:
- Poisson regression (goal modeling)
- Logistic regression (W/D/L probabilities)
- Bayesian extensions (optional)

These models provide:
- Interpretable parameters
- Probabilistic outputs
- A strong baseline used in professional football analytics

---

### 2️⃣ Convolutional Neural Networks (CNNs)
CNNs will be used to capture **patterns in match sequences and team form**.

Possible representations:
- Time-series encoded as matrices (recent matches, form windows)
- Team performance heatmaps
- Feature interaction maps

CNNs are **not used on images**, but on **structured numerical data transformed into spatial representations**.

---

## 📊 Dataset Construction

The dataset will be **built manually and incrementally**.

### Data Scope
- Last **5 seasons** of matches
- Competitions:
  - Bosnian Premier League (WWIN Liga BiH)
- Teams:
  - FK Željezničar
  - FK Sarajevo
  - FK Zrinjski
  - FK Borac
  - Other league teams (later phase)

### Planned Features
- Match date
- Home / away indicator
- Goals scored & conceded
- Recent form (last N matches)
- Head-to-head statistics
- League position
- Goal difference
- Points per match
- Home advantage indicators

---

## 🛠️ Tech Stack

- **Language**: Python
- **Environment**: Google Colab
- **Libraries**:
  - NumPy
  - Pandas
  - scikit-learn
  - statsmodels
  - PyTorch / TensorFlow (for CNNs)
  - Matplotlib / Seaborn

> All experiments are developed in **Google Colab**, then **exported and committed** to this repository as notebooks.

---

## 📁 Repository Structure (Planned)

```text
├── data/
│   ├── raw/
│   ├── processed/
│   └── features/
├── notebooks/
│   ├── 01_data_collection.ipynb
│   ├── 02_feature_engineering.ipynb
│   ├── 03_poisson_regression.ipynb
│   ├── 04_outcome_probabilities.ipynb
│   ├── 05_cnn_experiments.ipynb
│   └── 06_evaluation.ipynb
├── models/
├── results/
├── README.md
└── requirements.txt
```
---

## 📈 Evaluation Strategy

Models will be evaluated using:
- Log-loss (probabilistic accuracy)
- Accuracy (W/D/L classification)
- Brier score
- Calibration curves
- Confusion matrices

Emphasis is placed on:
- Probability quality, not just raw accuracy
- Generalization, not overfitting historical data

---

## ⚠️ Important Disclaimer

Football is a **low-scoring, high-variance sport**.

This project:
- ❌ Does NOT claim perfect prediction
- ❌ Is NOT a betting system
- ✅ IS a data science & machine learning research project

Expected realistic performance:
- **Outcome prediction accuracy**: ~55–60%
- **Score prediction**: probabilistic, not exact

--- 

## 🚀 Project Status

Current stage:
- Repository setup
- Dataset design
- Data collection for FK Željezničar (last 5 seasons)

---

## 👤 Author

**Fejzullah Zdralović**

Software Engineer | Machine Learning & Data Science

Focus: Sports Analytics, AI, Statistical Modeling

---
📜 License

This project is released for **educational and research purposes**.