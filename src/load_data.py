import pandas as pd
from sqlalchemy import create_engine


# ====================================
# DATABASE CONNECTION
# ====================================

engine = create_engine(
    "postgresql+psycopg2://postgres:YOUR_PASSWORD@localhost:5432/sales_analysis"
)

# ====================================
# LOAD CSV
# ====================================

df = pd.read_csv("data/input/sales_data.csv")


# ====================================
# LOAD DATA INTO POSTGRESQL
# ====================================

df.to_sql(
    name="sales",
    con=engine,
    if_exists="replace",
    index=False
)

print("Tabela sales carregada com sucesso no PostgreSQL!")
