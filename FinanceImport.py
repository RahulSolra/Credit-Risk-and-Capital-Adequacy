import pandas as pd
from sqlalchemy import create_engine
import urllib.parse
import os

# --- 1. Connection Details ---
user = 'root'
password = urllib.parse.quote_plus("Rahul@321")
host = '127.0.0.1'
database = 'finance'
engine = create_engine(f'mysql+pymysql://{user}:{password}@{host}:3306/{database}')

# --- 2. Multiple File Mapping Configuration ---
# Key: 'File_Name.csv', Value: 'SQL_Table_Name'
files_to_import = {
    'Banking.csv': 'banking',
    'clients.csv': 'clients',
    'customers.csv': 'customers',
    'banking-realtionships.csv': 'banking_relationships', # Spelled exactly like your file
    'gender.csv': 'gender',
    'investment-advisiors.csv': 'investment_advisors'
}

# --- 3. Loop Through All Files ---
for target_file, target_table in files_to_import.items():
    if os.path.exists(target_file):
        print(f"\n⌛ Reading {target_file}...")
        
        # Using header=0 (default) as standard for these files. 
        # Change to header=2 only if your files have 2 blank rows at the top.
        df = pd.read_csv(target_file, header=0)
        
        # --- 4. AUTO-CLEANING ---
        # Clean headers (Space/hyphens -> _, Lowercase)
        df.columns = [
            str(c).strip().replace(' ', '_').replace('-', '_').replace('.', '').replace('/', '_').lower() 
            for c in df.columns
        ]
        
        # # Date columns auto-detection
        # for col in df.columns:
        #     col_lower = col.lower()
        #     if any(key in col_lower for key in ['date', 'time', 'start', 'actual', 'mfg', 'ideal', 'release']):
        #         temp_dt = pd.to_datetime(df[col], errors='coerce')
        #         df[col] = temp_dt.dt.date

        # # Null handling
        # df = df.where(pd.notnull(df), None)

        try:
            # --- 5. DATABASE UPLOAD ---
            print(f"🚀 Uploading {len(df.columns)} columns to '{target_table}' table...")
            
            df.to_sql(target_table, con=engine, if_exists='replace', index=False, chunksize=500)
            
            print(f"✅ Success! '{target_table}' table is ready.")
        except Exception as e:
            print(f"❌ Error while uploading {target_file}: {e}")
    else:
        print(f"❌ Error: {target_file} file folder mein nahi mili! (Skipping...)")

print("\n🎉 Sab file process ho gayi hain, bhai!")