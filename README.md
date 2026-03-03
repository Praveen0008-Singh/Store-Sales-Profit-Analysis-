# Store-Sales-Profit-Analysis

# 📊 Store Sales & Profit Analysis Dashboard

A fully interactive **Sales and Profit Analysis Web Application** built using **Python, Pandas, Plotly, and Streamlit**.

This project helps businesses analyze retail performance, identify profitable segments, detect loss-making products, and make data-driven decisions.

---

## 🚀 Live Features

* 📌 Key Performance Indicators (KPIs)

  * Total Sales
  * Total Profit
  * Quantity Sold
  * Profit Margin %

* 🌍 Sales by Region (Interactive Bar Chart)

* 📦 Profit by Category

* 📈 Monthly Sales Trend

* 💸 Discount vs Profit Analysis

* ⚠️ Loss-Making Transactions Table

* 🔍 Sidebar Filters (Region & Category)

* 📥 Download Filtered Data

---

## 🛠️ Tech Stack

* **Python**
* **Pandas** – Data cleaning & manipulation
* **Plotly Express** – Interactive visualizations
* **Streamlit** – Web app framework

---

## 📂 Project Structure

```
Store-Sales-Analysis/
│
├── app.py
├── README.md
├── requirements.txt
└── sample_data.csv (optional)
```

---

## 📦 Installation & Setup

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/yourusername/store-sales-analysis.git
cd store-sales-analysis
```

### 2️⃣ Create Virtual Environment (Optional but Recommended)

```bash
python -m venv venv
venv\Scripts\activate   # Windows
source venv/bin/activate  # Mac/Linux
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

If you don't have `requirements.txt`, install manually:

```bash
pip install streamlit pandas plotly
```

---

## ▶️ Run the Application

```bash
streamlit run app.py
```

The app will open automatically in your browser at:

```
http://localhost:8501
```

---

## 📊 Dataset Requirements

Your CSV file should contain the following columns:

* `Order Date`
* `Region`
* `Category`
* `Sales`
* `Profit`
* `Quantity`
* `Discount` (optional but recommended)

---

## 🧠 Business Insights You Can Generate

* Which region generates the highest revenue?
* Which category is most profitable?
* Are discounts negatively affecting profit?
* What are the peak sales months?
* Which transactions are loss-making?

---

## 🌐 Deployment (Streamlit Cloud)

1. Push project to GitHub
2. Visit [https://streamlit.io/cloud](https://streamlit.io/cloud)
3. Connect your GitHub repository
4. Select `app.py`
5. Deploy

---

## 📌 Future Enhancements

* 🔮 Sales Forecasting (ARIMA / Prophet)
* 🤖 Profit Prediction using Machine Learning
* 📊 Customer Segmentation
* 📍 Geo-based Sales Mapping
* 🐳 Docker Deployment
* ☁️ AWS / Azure Hosting

---

