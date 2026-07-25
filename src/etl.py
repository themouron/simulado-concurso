import pandas as pd


# ====================================
# LOAD DATA
# ====================================

from sqlalchemy import create_engine

engine = create_engine(
    "postgresql+psycopg2://postgres:YOUR_PASSWORD@localhost:5432/sales_analysis"
)

query = """
SELECT *
FROM sales
"""

df = pd.read_sql(query, engine)

# ====================================
# DATA PREPARATION
# ====================================

df["date"] = pd.to_datetime(df["date"])
df["month_number"] = df["date"].dt.month
df["month"] = df["date"].dt.month_name()
df["day_of_week_number"] = df["date"].dt.dayofweek
df["day_of_week"] = df["date"].dt.day_name()
df = df.sort_values("month_number")

# Translate month names to Portuguese.
meses = {
    "January": "Janeiro",
    "February": "Fevereiro",
    "March": "Março",
    "April": "Abril",
    "May": "Maio",
    "June": "Junho",
    "July": "Julho",
    "August": "Agosto",
    "September": "Setembro",
    "October": "Outubro",
    "November": "Novembro",
    "December": "Dezembro"
}

df["month"] = df["month"].map(meses)

# Translate weekday names to Portuguese.
dias_semana = {
    "Monday": "Segunda",
    "Tuesday": "Terça",
    "Wednesday": "Quarta",
    "Thursday": "Quinta",
    "Friday": "Sexta",
    "Saturday": "Sábado",
    "Sunday": "Domingo"
}

# Translate region names to Portuguese.
df["day_of_week"] = df["day_of_week"].map(dias_semana)
region_translation = {
    "East": "Leste",
    "West": "Oeste",
    "North": "Norte",
    "South": "Sul",
    "Central": "Centro"
}

df["region"] = df["region"].map(region_translation)

# Translate product names to Portuguese.
product_translation = {
    "Mouse": "Mouse",
    "Webcam": "Webcam",
    "Keyboard": "Teclado",
    "Headset": "Headset",
    "Router": "Roteador",
    "SSD 1TB": "SSD 1 TB",
    "External HD": "HD Externo",
    "Office Chair": "Cadeira",
    "Monitor": "Monitor",
    "Printer": "Impressora",
    "Desk": "Mesa",
    "Notebook": "Notebook"
}

df["product"] = df["product"].map(product_translation)

# Translate category names to Portuguese.
category_translation = {
    "Computers": "Computadores",
    "Peripherals": "Periféricos",
    "Furniture": "Móveis",
    "Networking": "Redes",
    "Storage": "Armazenamento",
    "Office": "Escritório",
    "Screens": "Monitores"
}

df["category"] = df["category"].map(category_translation)

# ====================================
# DATA VALIDATION
# ====================================

null_values = df.isnull().sum()
duplicate_rows = df.duplicated().sum()

# ====================================
# FEATURE ENGINEERING
# ====================================

df["revenue"] = df["quantity"] * df["unit_price"]

# ====================================
# BUSINESS ANALYSIS
# ====================================

# Total revenue
total_revenue = df["revenue"].sum()

# Revenue by seller
revenue_by_seller = (
    df.groupby("seller")["revenue"]
      .sum()
      .sort_values(ascending=False)
)

# Revenue by product
revenue_by_product = (
    df.groupby("product")["revenue"]
      .sum()
      .sort_values(ascending=False)
)

# Revenue by region
revenue_by_region = (
    df.groupby("region")["revenue"]
      .sum()
      .sort_values(ascending=False)
)

# Revenue by category
revenue_by_category = (
    df.groupby("category")["revenue"]
      .sum()
      .sort_values(ascending=False)
)

# Quantity by product
quantity_by_product = (
    df.groupby("product")["quantity"]
      .sum()
      .sort_values(ascending=False)
)

# Average revenue per sale by seller
average_revenue_by_seller = (
    df.groupby("seller")["revenue"].mean().sort_values(ascending=False)
)

# Number of sales by seller
sales_count_by_seller = (
    df.groupby("seller")["quantity"]
      .count()
      .sort_values(ascending=False)
)

# Unique products sold by seller
products_by_seller = (
    df.groupby("seller")["product"]
    .nunique()
    .sort_values(ascending=False)
)

# Revenue by month
revenue_by_month = (
    df.groupby(["month_number", "month"])["revenue"]
    .sum()
    .sort_index()
)

# Revenue by day_of_week
revenue_by_day_of_week = (
    df.groupby(["day_of_week_number", "day_of_week"])["revenue"]
    .sum()
    .sort_index()
)

# Sales count by month.
sales_count_by_month = (
    df.groupby(["month_number", "month"])["quantity"]
    .count()
)

# ====================================
# LOAD CLEAN DATA INTO POSTGRESQL
# ====================================

df.to_sql(
    name="sales_clean",
    con=engine,
    if_exists="replace",
    index=False
)

print("Tabela sales_clean criada com sucesso no PostgreSQL!")