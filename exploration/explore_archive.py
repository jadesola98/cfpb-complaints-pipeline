"""This script Profiles one CFPB archive zip: The format, size, columns, missing values,
duplicates, response values and narrative coverage.
"""
 
import sys        # reads the zip path from the command line
import zipfile    # reads files inside a zip without unzipping
import pandas as pd

# --- Helper function -----------------------------------------------------------
def find_col(df, name):
    """Returns the real column name matching 'name', ignoring case and punctuation."""

    def normalise(text):
        # "Complaint ID" and "complaint_id" both become "complaintid"
        return "".join(ch for ch in text.lower() if ch.isalnum())

    for col in df.columns:
        if normalise(col) == normalise(name):
            return col
    return None  # no matching column

# --- Step 1: Read the zip path from the command line -------------------------

zip_path = sys.argv[1]


# --- Step 2: Open the zip and load the data ----------------------------------
# Opens the zip, list its contents, and load the first file into a DataFrame
with zipfile.ZipFile(zip_path) as zf:
    print("Files inside the zip:")
    for info in zf.infolist():
        print(f"  {info.filename}: {info.file_size / 1_000_000:.1f} MB uncompressed")

    first_file = zf.infolist()[0].filename
    with zf.open(first_file) as f:
        # Format unknown yet, so handle CSV or JSON
        if first_file.lower().endswith(".csv"):
            df = pd.read_csv(f, low_memory=False)
        else:
            df = pd.read_json(f)

# --- Step 3: Basic profile ---------------------------------------------------

# Size and structure
print(f"\nRows: {len(df):,}")
print(f"Columns: {len(df.columns)}")
print("\nColumn names and types:")
print(df.dtypes)

# % of empty cells per column, worst first
print("\nMissing values per column (%):")
print((df.isna().mean() * 100).round(1).sort_values(ascending=False))


# --- Step 4: Find the key columns --------------------------------------------

id_col = find_col(df, "Complaint ID")
date_col = find_col(df, "Date received")
response_col = find_col(df, "Company response to consumer")
product_col = find_col(df, "Product")
narrative_col = find_col(df, "Consumer complaint narrative")


# --- Step 5: Detailed checks -------------------------------------------------
# Duplicates mean Spark must deduplicate
if id_col:
    print(f"\nDuplicate complaint IDs: {df[id_col].duplicated().sum():,}")

# Confirm the file covers the period in its name
if date_col:
    print(f"\nDate received range: {df[date_col].min()} to {df[date_col].max()}")

# Look for "In progress": confirms complaints change over time
if response_col:
    print("\nCompany response values:")
    print(df[response_col].value_counts(dropna=False))

# Helps choose the narrative subset for the AI stage
if product_col:
    print("\nTop 10 products:")
    print(df[product_col].value_counts().head(10))

# How much text the AI layer will have, and whether it needs chunking
if narrative_col:
    has_text = df[narrative_col].notna()
    print(f"\nComplaints with a narrative: {has_text.mean() * 100:.1f}%")
    print(f"Average narrative length: {df.loc[has_text, narrative_col].str.len().mean():.0f} characters")