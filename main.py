import pandas as pd

customers = pd.read_csv("data/olist_customers_dataset.csv")
orders = pd.read_csv("data/olist_orders_dataset.csv")
items = pd.read_csv("data/olist_order_items_dataset.csv")
payments = pd.read_csv("data/olist_order_payments_dataset.csv")
products = pd.read_csv("data/olist_products_dataset.csv")

print("Customers:", customers.shape)
print("Orders:", orders.shape)
print("Items:", items.shape)
print("Payments:", payments.shape)
print("Products:", products.shape)

print("\nMissing Values")

print(customers.isnull().sum())
print(products.isnull().sum())
print("\nDuplicates")

print("Customers:", customers.duplicated().sum())
print("Orders:", orders.duplicated().sum())
print("Items:", items.duplicated().sum())
print("Payments:", payments.duplicated().sum())
print("Products:", products.duplicated().sum())
print("\nMerging Tables...")

merged = orders.merge(
    customers,
    on="customer_id",
    how="inner"
)

merged = merged.merge(
    items,
    on="order_id",
    how="inner"
)

merged = merged.merge(
    payments,
    on="order_id",
    how="inner"
)

merged = merged.merge(
    products,
    on="product_id",
    how="inner"
)

print("Merged Dataset Shape:", merged.shape)

print("\nMerged Dataset Sample:")
print(merged.head())
print("\nBusiness Insights")

total_orders = merged["order_id"].nunique()
total_revenue = merged["payment_value"].sum()
total_customers = merged["customer_unique_id"].nunique()

print("Total Orders:", total_orders)
print("Total Revenue:", round(total_revenue, 2))
print("Total Customers:", total_customers)

print("\nTop 10 States")

top_states = merged.groupby(
    "customer_state"
)["order_id"].count().sort_values(
    ascending=False
)

print(top_states.head(10))

merged["order_purchase_timestamp"] = pd.to_datetime(
    merged["order_purchase_timestamp"]
)

merged["month"] = merged[
    "order_purchase_timestamp"
].dt.month

monthly_sales = merged.groupby(
    "month"
)["payment_value"].sum().sort_index()

print("\nMonthly Sales Trend")
print(monthly_sales)

merged.to_csv(
    "output/final_dataset.csv",
    index=False
)

print("\nFinal Dataset Saved Successfully!")