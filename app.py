# ================================
# STORE SALES & PROFIT DASHBOARD
# ================================

import streamlit as st
import pandas as pd
import plotly.express as px

# -------------------------------
# Page Configuration
# -------------------------------
st.set_page_config(
    page_title="Store Sales & Profit Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Store Sales & Profit Analysis Dashboard")
st.markdown("Upload your retail store dataset to analyze sales and profit performance.")

# -------------------------------
# File Upload
# -------------------------------
uploaded_file = st.file_uploader("Upload CSV File", type=["csv"])

if uploaded_file is not None:

    # ------------------------------------------------------------------
    # Load Data with encoding and delimiter detection via csv.Sniffer
    # ------------------------------------------------------------------
    import io, csv

    raw_bytes = uploaded_file.getvalue()
    # decode once with latin1 (safe for any byte values)
    raw_text = raw_bytes.decode('latin1', errors='ignore')
    # display some of the raw lines for debugging
    st.write("Raw file preview:", raw_text.splitlines()[:5])

    # attempt to sniff delimiter from the first few lines
    sample = "\n".join(raw_text.splitlines()[:20])
    sep = None
    try:
        dialect = csv.Sniffer().sniff(sample, delimiters=",;\t|")
        sep = dialect.delimiter
        st.info(f"Detected delimiter: '{sep}'")
    except Exception:
        # fallback to common separators later
        pass

    df = None
    for enc in ('utf-8', 'latin1', 'cp1252'):
        try:
            if sep:
                df = pd.read_csv(io.StringIO(raw_text), encoding=enc, sep=sep)
            else:
                df = pd.read_csv(io.StringIO(raw_text), encoding=enc, sep=None, engine='python')
            if df.shape[1] == 1 and not sep:
                # try other separators explicitly
                for try_sep in (',', ';', '\t', '|'):
                    df2 = pd.read_csv(io.StringIO(raw_text), encoding=enc, sep=try_sep)
                    if df2.shape[1] > 1:
                        df = df2
                        sep = try_sep
                        st.info(f"Switching to separator '{sep}'")
                        break
            break
        except Exception:
            continue

    if df is None:
        st.error("Unable to parse CSV file. Please ensure it is a valid CSV.")
        st.stop()

    # show what pandas produced
    st.write("Parsed columns:", df.columns.tolist())
    st.write("Sample data:", df.head())

    # attempt to detect if the header row is actually in the body
    required_keywords = ['sales', 'profit', 'quantity']
    header_row = None
    for idx in range(min(5, len(df))):
        row_vals = df.iloc[idx].astype(str).str.lower()
        if any(any(kw in v for kw in required_keywords) for v in row_vals):
            header_row = idx
            break
    if header_row is not None and header_row != 0:
        st.warning(f"Header appears on line {header_row+1}; reloading with that row as header.")
        # reload using detected header offset
        df = pd.read_csv(io.StringIO(raw_text), header=header_row, encoding=enc, sep=sep)
        st.write("Re-parsed columns:", df.columns.tolist())
        st.write("Sample data after reload:", df.head())

    if df.shape[1] == 1:
        st.error("Only one column was detected after parsing. Check the file's delimiter or encoding.")
        st.stop()

    # normalize headers: strip BOM/whitespace and make case-insensitive lookups easier
    # clean up headers and build lookup
    df.columns = (
        df.columns
        .astype(str)
        .str.replace('\ufeff', '', regex=False)  # remove BOM
        .str.strip()
    )
    # show what headers we actually saw (helps debug encoding/renaming issues)
    st.write("Detected columns:", df.columns.tolist())

    # create a mapping of lowercase names to actual column names
    col_map = {c.lower(): c for c in df.columns}
    def get_col(name):
        return col_map.get(name.lower())

    # fallback: look for a column containing the keyword as substring
    def find_col_substr(keyword):
        keyword = keyword.lower()
        for c in df.columns:
            if keyword in c.lower():
                return c
        return None

    # try to locate required columns, using substring matching if necessary
    sales_col = get_col('sales') or find_col_substr('sales')
    profit_col = get_col('profit') or find_col_substr('profit')
    quantity_col = get_col('quantity') or find_col_substr('quantity')

    missing = []
    if sales_col is None: missing.append('sales')
    if profit_col is None: missing.append('profit')
    if quantity_col is None: missing.append('quantity')
    if missing:
        st.error(
            "Missing required columns: %s.\n" \
            "Please check your CSV headers or rename the appropriate columns."
            % ', '.join(missing)
        )
        st.stop()

    # -------------------------------
    # Data Cleaning
    # -------------------------------
    df.drop_duplicates(inplace=True)
    df.dropna(inplace=True)

    # figure out normalized column names for later use
    sales_col = get_col('sales')
    profit_col = get_col('profit')
    quantity_col = get_col('quantity')
    date_col = get_col('order date')
    region_col = get_col('region')
    category_col = get_col('category')
    discount_col = get_col('discount')

    # Convert Date Column if present
    if date_col is not None:
        df[date_col] = pd.to_datetime(df[date_col])
        df['Year'] = df[date_col].dt.year
        df['Month'] = df[date_col].dt.to_period('M').astype(str)

    # -------------------------------
    # Sidebar Filters
    # -------------------------------
    st.sidebar.header("🔍 Filter Data")

    if region_col is not None:
        region = st.sidebar.multiselect(
            "Select Region",
            options=df[region_col].unique(),
            default=df[region_col].unique()
        )
        df = df[df[region_col].isin(region)]

    if category_col is not None:
        category = st.sidebar.multiselect(
            "Select Category",
            options=df[category_col].unique(),
            default=df[category_col].unique()
        )
        df = df[df[category_col].isin(category)]

    # -------------------------------
    # KPI Section
    # -------------------------------
    # compute KPIs only if the corresponding columns exist
    total_sales = df[sales_col].sum() if sales_col else 0
    total_profit = df[profit_col].sum() if profit_col else 0
    total_quantity = df[quantity_col].sum() if quantity_col else 0
    profit_ratio = (total_profit / total_sales) * 100 if total_sales != 0 else 0

    st.subheader("📌 Key Performance Indicators")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Sales", f"${total_sales:,.2f}")
    col2.metric("Total Profit", f"${total_profit:,.2f}")
    col3.metric("Total Quantity Sold", f"{int(total_quantity)}")
    col4.metric("Profit Margin", f"{profit_ratio:.2f}%")

    st.markdown("---")

    # -------------------------------
    # Sales by Region
    # -------------------------------
    if region_col is not None:
        st.subheader("🌍 Sales by Region")
        sales_region = df.groupby(region_col)[sales_col].sum().reset_index()
        fig_region = px.bar(
            sales_region,
            x=region_col,
            y=sales_col,
            color=region_col,
            title="Total Sales by Region"
        )
        st.plotly_chart(fig_region, use_container_width=True)

    # -------------------------------
    # Profit by Category
    # -------------------------------
    if category_col is not None:
        st.subheader("📦 Profit by Category")
        profit_category = df.groupby(category_col)[profit_col].sum().reset_index()
        fig_category = px.bar(
            profit_category,
            x=category_col,
            y=profit_col,
            color=category_col,
            title="Total Profit by Category"
        )
        st.plotly_chart(fig_category, use_container_width=True)

    # -------------------------------
    # Monthly Sales Trend
    # -------------------------------
    if 'Month' in df.columns:
        st.subheader("📈 Monthly Sales Trend")
        monthly_sales = df.groupby('Month')[sales_col].sum().reset_index()
        fig_month = px.line(
            monthly_sales,
            x='Month',
            y=sales_col,
            markers=True,
            title="Monthly Sales Trend"
        )
        st.plotly_chart(fig_month, use_container_width=True)

    # -------------------------------
    # Discount vs Profit Analysis
    # -------------------------------
    if discount_col is not None:
        st.subheader("💸 Discount vs Profit Analysis")
        fig_discount = px.scatter(
            df,
            x=discount_col,
            y=profit_col,
            color=category_col if category_col is not None else None,
            title="Impact of Discount on Profit"
        )
        st.plotly_chart(fig_discount, use_container_width=True)

    # -------------------------------
    # Loss Making Products
    # -------------------------------
    if profit_col is not None:
        st.subheader("⚠️ Loss Making Transactions")
        loss_df = df[df[profit_col] < 0]
        st.write(loss_df)

    # -------------------------------
    # Download Filtered Data
    # -------------------------------
    st.download_button(
        label="📥 Download Filtered Data",
        data=df.to_csv(index=False),
        file_name="filtered_store_data.csv",
        mime="text/csv"
    )

else:
    st.info("👆 Please upload a CSV file to begin analysis.")