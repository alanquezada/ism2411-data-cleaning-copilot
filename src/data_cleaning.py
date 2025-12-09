# Project: ism2411-data-cleaning-copilot
# The purpose of this code is to organize the files that is imported by handling the missing values, organzing columns and removing valid entries.
# Then it saves the new corrrected data in a new file

import pandas as pd


#Function 1: load_data
#The first part is downloading the file
def load_data(file_path: str) -> pd.DataFrame:
    """Loads the raw sales data from a CSV file into a pandas DataFrame."""
    try:
        df = pd.read_csv(file_path)
        return df
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        return pd.DataFrame()

#Function 2 clean_column_names with the suggestions of the copilot
# I used copilot to give me sugggestions
#I need a function that standarizes all the columns from the uploaded file and converts them to lowercase and replaces them with underscores
#for it to make consisten column names and prevent less errors when im working with the data
# suggestion : def standardize_columns(df: pd.DataFrame) -> pd.DataFrame:
def clean_column_names(df: pd.DataFrame) -> pd.DataFrame:
    #The copilot assisted me with this function but im adding a modification to include .str.strip() to handle leading/trailing
    #This is for it to handle the white space in column names before lowercasing and replacing.
    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
    return df 

#Function 3: handle_missing_values with the assistence of copiloy 
#Step 3 is handeling missing values and clean up text.
#This part of the function will work with the quantity and price columns by putting 0 in stead of missing values.
#This is for it to be able to have more accurate calculations 
def handle_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    #The copilot suggested me to put in 0 value for the missing values, I took the suggestion for I can be consistent.
    #To make sure I have a standarized number in the quantity and price columns to avoid errors.
    
    # 1. Fill missing values with 0
    df['price'] = df['price'].fillna(0)
    df['qty'] = df['qty'].fillna(0)

   
    df['price'] = pd.to_numeric(df['price'], errors='coerce').fillna(0)
    df['qty'] = pd.to_numeric(df['qty'], errors='coerce').fillna(0)

    return df

#Function 4: remove_invalid_rows

#This will remove any type of columns in price or quantity that are negative because all the value need to be positive,
# It will also help in getting rid of any invalid entries
# Because any negative prices or quantites is invalid and will cause issues in calculations for the data analysis.
def remove_invalid_rows(df: pd.DataFrame) -> pd.DataFrame:
    # this part removes the rows with the negative values in price and quantity columns
    df_filtered = df[(df['price'] >= 0) & (df['qty'] >= 0)].copy()

    # I strip white spaces from product names and categories
    df_filtered['prodname'] = df_filtered['prodname'].str.strip()
    df_filtered['category'] = df_filtered['category'].str.strip()

    return df_filtered

# This is the part that I copy pasted from the assignment as required by instructor 
if __name__ == "__main__":
    raw_path = "data/raw/sales_data_raw.csv"
    cleaned_path = "data/processed/sales_data_clean.csv"

    df_raw = load_data(raw_path)

    # ensures that the data was loaded succedfully 
    if df_raw.empty:
        print("Cleaning script stopped due to file loading error.")
    else:
        df_clean = clean_column_names(df_raw)
        df_clean = handle_missing_values(df_clean)
        df_clean = remove_invalid_rows(df_clean)
        df_clean.to_csv(cleaned_path, index=False)
        print("Cleaning complete. First few rows:")
        print(df_clean.head())