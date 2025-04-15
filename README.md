# A/B Testing Dashboard

A Streamlit web app for analyzing and visualizing A/B test results from advertising data. The dashboard provides statistical comparison (t-test), regression analysis, and auto-generated PDF/HTML reports for marketing teams.

---

## Features

- **A/B Test Analysis:** Compares conversion rates between Facebook and Google ad platforms using a t-test.
- **Interactive Visualizations:** Boxplot comparison of conversion rates by platform.
- **Regression Analysis:** OLS regression to understand factors influencing conversions.
- **Automated Reporting:** Generate and download PDF or HTML reports with results and model summaries.
- **User-friendly UI:** Built with Streamlit for easy interaction.

---

## Demo

https://ab-tester.streamlit.app/

---

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/srishtayal/AB-testing.git
cd ab-testing
```

### 2. Prepare Your Data

- Place your ad data CSV file at `data/ad_data.csv`.
- The CSV should include at least these columns:  
  `impressions`, `clicks`, `conversions`, `spend`, `age`, `gender`, `platform`

### 3. Install Dependencies

Create a virtual environment (optional but recommended):

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

Install required packages:

```bash
pip install -r requirements.txt
```

### 4. Run the App

```bash
streamlit run main.py
```

---

## File Structure

```
.
├── main.py
├── requirements.txt
├── README.md
└── data/
    └── ad_data.csv
```

---

## requirements.txt Example

```
streamlit
pandas
numpy
matplotlib
seaborn
scipy
statsmodels
scikit-learn
fpdf
```

---

## Usage

- **A/B Test Results:** See t-test statistics and significance.
- **Boxplot:** Visualize conversion rate distributions for each platform.
- **Regression Analysis:** View OLS regression summary.
- **Download Reports:** Click buttons to generate and download PDF/HTML reports.

---