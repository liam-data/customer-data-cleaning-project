import pandas as pd
import re

# Load the dataset
df = pd.read_csv("customer_data.csv")

# Remove duplicate rows
df = df.drop_duplicates()

# Clean up whitespace in names
df["name"] = df["name"].astype(str).str.strip()

# Standardize names to title case
df["name"] = df["name"].str.title()

# Standardize emails to lowercase
df["email"] = df["email"].astype(str).str.strip().str.lower()

# Replace blank or invalid emails with a placeholder
df["email"] = df["email"].replace("", pd.NA)
df["email"] = df["email"].apply(
    lambda x: x if pd.notna(x) and "@" in x and "." in x.split("@")[-1] else "missing_or_invalid@email.com"
)

# Standardize city names
df["city"] = df["city"].astype(str).str.strip().str.title()

# Clean phone numbers to format: 555-123-4567
def clean_phone(phone):
    if pd.isna(phone):
        return "Missing"
    digits = re.sub(r"\D", "", str(phone))
    if len(digits) == 10:
        return f"{digits[:3]}-{digits[3:6]}-{digits[6:]}"
    return "Invalid"

df["phone"] = df["phone"].apply(clean_phone)

# Fill missing purchase amounts with 0
df["purchase_amount"] = pd.to_numeric(df["purchase_amount"], errors="coerce")
df["purchase_amount"] = df["purchase_amount"].fillna(0)

# Save cleaned data
df.to_csv("cleaned_customer_data.csv", index=False)

print("Data cleaned successfully.")
print(df)