import pandas as pd
import os

# ===========================
# Create folder paths
# ===========================

RAW = "data/raw"
PROCESSED = "data/processed"

os.makedirs(PROCESSED, exist_ok=True)

# ===========================
# 1. NAV HISTORY
# ===========================

nav = pd.read_csv(f"{RAW}/02_nav_history.csv")

nav["date"] = pd.to_datetime(
    nav["date"],
    errors="coerce"
)

nav = nav.sort_values(["amfi_code", "date"])

nav["nav"] = nav.groupby("amfi_code")["nav"].ffill()

nav = nav.drop_duplicates()

nav = nav[nav["nav"] > 0]

nav.to_csv(
    f"{PROCESSED}/02_nav_history_clean.csv",
    index=False
)

print("NAV history cleaned successfully.")

# ===========================
# 2. SCHEME PERFORMANCE
# ===========================

perf = pd.read_csv(f"{RAW}/07_scheme_performance.csv")

returns = [
    "return_1yr_pct",
    "return_3yr_pct",
    "return_5yr_pct"
]

for col in returns:
    perf[col] = pd.to_numeric(
        perf[col],
        errors="coerce"
    )

perf["expense_ratio_pct"] = pd.to_numeric(
    perf["expense_ratio_pct"],
    errors="coerce"
)

perf.to_csv(
    f"{PROCESSED}/07_scheme_performance_clean.csv",
    index=False
)

print("Scheme performance cleaned successfully.")

# ===========================
# 3. FUND MASTER
# ===========================

fund = pd.read_csv(f"{RAW}/01_fund_master.csv")

fund = fund.drop_duplicates()

fund["launch_date"] = pd.to_datetime(
    fund["launch_date"],
    errors="coerce"
)

fund.to_csv(
    f"{PROCESSED}/01_fund_master_clean.csv",
    index=False
)

print("Fund master cleaned successfully.")

print("All cleaning completed successfully!")