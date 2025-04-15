import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import statsmodels.api as sm
from scipy import stats
import streamlit as st
from fpdf import FPDF

# Load the dataset
df = pd.read_csv('data/ad_data.csv')

# Perform necessary calculations
df['CTR'] = df['clicks'] / df['impressions']
df['conversion_rate'] = df['conversions'] / df['clicks']
df['CPC'] = df['spend'] / df['clicks']
df['CPA'] = df['spend'] / df['conversions']

# Split by platform for A/B testing
facebook = df[df['platform'] == 'Facebook']
google = df[df['platform'] == 'Google']

# A/B Test - T-test for conversion rates
t_stat, p_val = stats.ttest_ind(
    facebook['conversion_rate'].dropna(),
    google['conversion_rate'].dropna()
)

# Streamlit UI
st.title("A/B Testing Dashboard")
st.write("A/B Test Results:")
st.write(f"T-Statistic: {t_stat:.4f}, P-Value: {p_val:.4f}")

if p_val < 0.05:
    st.success("✅ Significant difference in conversion rates between platforms.")
else:
    st.warning("❌ No significant difference found.")

# Visualizations
fig, ax = plt.subplots()
sns.boxplot(data=[facebook['conversion_rate'], google['conversion_rate']], ax=ax)
ax.set_xticklabels(['Facebook', 'Google'])
ax.set_title('Conversion Rate Comparison')
st.pyplot(fig)

# Regression Analysis
# One-hot encode categorical variables
df_encoded = pd.get_dummies(df, columns=['gender', 'platform'], drop_first=True)

# Select features and target
features = ['spend', 'age', 'gender_M', 'platform_Google']
for col in features:
    if col not in df_encoded.columns:
        df_encoded[col] = 0  # Add missing columns if necessary

X = df_encoded[features].apply(pd.to_numeric, errors='coerce')
y = pd.to_numeric(df_encoded['conversions'], errors='coerce')

# Drop rows with any NaNs in X or y
mask = X.notnull().all(axis=1) & y.notnull()
X_clean = X[mask]
y_clean = y[mask]

# Check if X_clean and y_clean are still valid numeric data
if X_clean.isnull().sum().any() or y_clean.isnull().sum() > 0:
    st.error("There are still missing values in the data after cleaning. Please check the dataset.")
else:
    # Add a constant (intercept) to the features
    X_sm_clean = sm.add_constant(X_clean)

    # Ensure all data is float64
    X_sm_clean = X_sm_clean.astype(float)
    y_clean = y_clean.astype(float)

    # Fit the OLS regression model
    model = sm.OLS(y_clean, X_sm_clean).fit()

    # Display the model summary
    st.subheader("Regression Analysis Summary")
    st.text(model.summary())

    # Auto-generate PDF report
    def create_pdf():
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="A/B Testing Report", ln=True, align="C")
        pdf.ln(10)
        pdf.cell(200, 10, txt=f"T-Statistic: {t_stat:.4f}", ln=True)
        pdf.cell(200, 10, txt=f"P-Value: {p_val:.4f}", ln=True)
        pdf.ln(10)
        pdf.set_font("Courier", size=8)
        for line in model.summary().as_text().split('\n'):
            pdf.cell(0, 5, txt=line, ln=True)
        pdf.output("ab_testing_report.pdf")

    # Button to generate the report
    if st.button("Generate PDF Report"):
        create_pdf()
        st.success("✅ Report generated successfully! Download it below.")
        with open("ab_testing_report.pdf", "rb") as f:
            st.download_button("Download PDF", f, file_name="ab_testing_report.pdf")

    # Optionally, you can also create an HTML report:
    def create_html_report():
        html_content = f"""
        <html>
        <head><title>A/B Testing Report</title></head>
        <body>
        <h1>A/B Testing Report</h1>
        <p><strong>T-Statistic:</strong> {t_stat:.4f}</p>
        <p><strong>P-Value:</strong> {p_val:.4f}</p>
        <h2>Regression Analysis Summary</h2>
        <pre>{model.summary()}</pre>
        </body>
        </html>
        """
        with open("ab_testing_report.html", "w") as file:
            file.write(html_content)

    # Button to generate the HTML report
    if st.button("Generate HTML Report"):
        create_html_report()
        st.success("✅ HTML report generated successfully! Download it below.")
        with open("ab_testing_report.html", "rb") as f:
            st.download_button("Download HTML", f, file_name="ab_testing_report.html")
