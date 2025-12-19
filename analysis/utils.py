import pandas as pd
import numpy as np
from pathlib import Path

REQUIRED_COLUMNS = [
    'order_date',
    'product_name',
    'category',
    'cost_price',
    'selling_price',
    'quantity',
    'payment_mode',
]

def read_upload_to_df(file_path: str) -> pd.DataFrame:
    p = Path(file_path)
    if p.suffix.lower() == '.csv':
        df = pd.read_csv(p, dtype=str)
    else:
        df = pd.read_excel(p, engine='openpyxl', dtype=str)
    return df

def clean_df(df: pd.DataFrame) -> pd.DataFrame:
    for col in REQUIRED_COLUMNS:
        if col not in df.columns:
            df[col] = np.nan
    df = df[REQUIRED_COLUMNS].copy()
    df['order_date'] = pd.to_datetime(df['order_date'], errors='coerce')
    num_cols = ['cost_price', 'selling_price', 'quantity']
    for col in num_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    df['cost_price'] = df['cost_price'].fillna(0)
    df['selling_price'] = df['selling_price'].fillna(0)
    df['quantity'] = df['quantity'].fillna(0)
    df['product_name'] = df['product_name'].fillna('')
    df['category'] = df['category'].fillna('')
    df['payment_mode'] = df['payment_mode'].fillna('')
    df = df.dropna(subset=['order_date'])
    return df

def add_calculations(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df['total_sales'] = df['selling_price'] * df['quantity']
    df['profit'] = (df['selling_price'] - df['cost_price']) * df['quantity']
    df['profit_margin'] = np.where(
        df['total_sales'] > 0, (df['profit'] / df['total_sales']) * 100, 0
    )
    return df

def compute_analytics(df: pd.DataFrame) -> dict:
    res = {}
    dmf = df.copy()
    dmf['year'] = dmf['order_date'].dt.year
    dmf['month'] = dmf['order_date'].dt.to_period('M').astype(str)
    monthly = (
        dmf.groupby('month', as_index=False)
        .agg(total_sales=('total_sales', 'sum'), profit=('profit', 'sum'))
    )
    monthly['profit_margin'] = np.where(
        monthly['total_sales'] > 0,
        (monthly['profit'] / monthly['total_sales']) * 100,
        0,
    )
    res['monthly'] = monthly.to_dict(orient='records')
    yearly = dmf.groupby('year', as_index=False).agg(total_sales=('total_sales', 'sum'))
    res['yearly_total_sales'] = yearly.to_dict(orient='records')
    if not monthly.empty:
        best = monthly.loc[monthly['total_sales'].idxmax()]
        res['highest_sales_month'] = {'month': best['month'], 'total_sales': float(best['total_sales'])}
    else:
        res['highest_sales_month'] = None
    product_sales = (
        dmf.groupby('product_name', as_index=False)
        .agg(total_sales=('total_sales', 'sum'))
        .sort_values('total_sales', ascending=False)
    )
    res['product_sales'] = product_sales.to_dict(orient='records')
    product_profit = (
        dmf.groupby('product_name', as_index=False)
        .agg(profit=('profit', 'sum'))
        .sort_values('profit', ascending=False)
    )
    res['product_profit'] = product_profit.to_dict(orient='records')
    pmode = dmf['payment_mode'].fillna('').str.strip()
    pmode = pmode.replace({'upi':'UPI','cash':'Cash','card':'Card'})
    distribution = pmode.value_counts().reset_index()
    distribution.columns = ['payment_mode', 'count']
    total = int(distribution['count'].sum()) if not distribution.empty else 0
    distribution['percent'] = np.where(total > 0, (distribution['count'] / total) * 100, 0)
    res['payment_mode_distribution'] = distribution.to_dict(orient='records')
    return res
