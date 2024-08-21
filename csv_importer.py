import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from app.model import Shipping_data

DATABASE_URL = 'sqlite:///instance/database.db'
engine = create_engine(DATABASE_URL, echo=True)
Session = sessionmaker(bind=engine)
session = Session()

csv_file_path = 'data.csv'
df = pd.read_csv(csv_file_path)

# ensure that the necessary columns are present and correctly named
if 'user_id' not in df.columns:
    df['user_id'] = 1 # default to admin user ID
    
# convert date columns and handle errors
date_columns = ['CY_Open', 'SI_Cut_Off', 'CY_CY_CLS', 'ETD', 'ETA', 'Date_Valid']
for col in date_columns:
    df[col] = pd.to_datetime(df[col], errors='coerce')

# fill NaN values with appropriate default values
df.fillna({
    'cost': 0,
    'CS': '',
    'week': 0,
    'carrier': '',
    'service': '',
    'MV': '',
    'SO': '',
    'size': '',
    'POL': '',
    'POD': '',
    'Final_Destination': '',
    'routing': '',
    'CY_Open': pd.Timestamp('1970-01-01'),
    'SI_Cut_Off': pd.Timestamp('1970-01-01'),
    'CY_CY_CLS': pd.Timestamp('1970-01-01'),
    'ETD': pd.Timestamp('1970-01-01'),
    'ETA': pd.Timestamp('1970-01-01'),
    'Contract_or_Coloader': '',
    'shipper': '',
    'consignee': '',
    'term': '',
    'salesman': '',
    'Date_Valid': pd.Timestamp('1970-01-01'),
    'SR': '',
    'remark': '',
    'user_id': 1  # default to admin user ID
}, inplace=True)

# verify that there are no NaN values in critical columns
if df['user_id'].isnull().any():
    print("Warning: 'user_id' column contains NaN values.")

# Insert data into the database
for index, row in df.iterrows():
    new_data = Shipping_data(
        date_created=datetime.utcnow(),
        CS=row['CS'],
        week=row['week'],
        carrier=row['carrier'],
        service=row['service'],
        MV=row['MV'],
        SO=row['SO'],
        size=row['size'],
        POL=row['POL'],
        POD=row['POD'],
        Final_Destination=row['Final_Destination'],
        routing=row['routing'],
        CY_Open=row['CY_Open'],
        SI_Cut_Off=row['SI_Cut_Off'],
        CY_CY_CLS=row['CY_CY_CLS'],
        ETD=row['ETD'],
        ETA=row['ETA'],
        Contract_or_Coloader=row['Contract_or_Coloader'],
        shipper=row['shipper'],
        consignee=row['consignee'],
        term=row['term'],
        salesman=row['salesman'],
        cost=row['cost'],
        Date_Valid=row['Date_Valid'],
        SR=row['SR'],
        remark=row['remark'],
        user_id=row['user_id']
    )
    try:
        session.add(new_data)
    except Exception as e:
        print(f"Error inserting row {index}: {e}")

try:
    session.commit()
except Exception as e:
    session.rollback()
    print(f"An error occurred during commit: {e}")

session.close()
