#رفع الداتا لسيكول


import pandas as pd
import mysql.connector

df = pd.read_csv(r"C:\ProgramData\MySQL\MySQL Server 9.2\Uploads\excel_task_cleaned.csv")
df = df[~df['START_DATE'].str.contains("Totals", na=False)]

df['START_DATE'] = pd.to_datetime(df['START_DATE'], format='%m/%d/%Y %H:%M', errors='coerce')
df['END_DATE'] = pd.to_datetime(df['END_DATE'], format='%m/%d/%Y %H:%M', errors='coerce')

df['START_DATE'] = df['START_DATE'].dt.strftime('%Y-%m-%d %H:%M:%S')
df['END_DATE'] = df['END_DATE'].dt.strftime('%Y-%m-%d %H:%M:%S')
df = df.dropna(subset=['START_DATE', 'END_DATE'])
df = df.fillna("NULL")

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="OKASHA3210",
    database="excel_task_cleaned"
)

cursor = conn.cursor()

for _, row in df.iterrows():
    cursor.execute("""
        INSERT INTO uber_data (START_DATE, END_DATE, CATEGORY, START, STOP, MILES, PURPOSE) 
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, tuple(row))
conn.commit()
cursor.close()
conn.close()

print("عاش يعكش")



#تنبؤ بالداتا وتصفية الداتا من القيم الغير معروفة

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.neighbors import KNeighborsClassifier

file_path = "Excel_task_cleaned.csv"
df = pd.read_csv(file_path)

most_common_category = df["CATEGORY"].mode()[0]
df.loc[df["CATEGORY"] == "Unknown", "CATEGORY"] = most_common_category

most_common_start = df[df["START"] != "Unknown"]["START"].mode()[0]
most_common_stop = df[df["STOP"] != "Unknown"]["STOP"].mode()[0]
df.loc[df["START"] == "Unknown", "START"] = most_common_start
df.loc[df["STOP"] == "Unknown", "STOP"] = most_common_stop


most_common_start_location = df[df["START"] != "Unknown Location"]["START"].mode()[0]
most_common_stop_location = df[df["STOP"] != "Unknown Location"]["STOP"].mode()[0]
df.loc[df["START"] == "Unknown Location", "START"] = most_common_start_location
df.loc[df["STOP"] == "Unknown Location", "STOP"] = most_common_stop_location

final_file_path = "Excel_task_final_cleaned.csv"
df.to_csv(final_file_path, index=False)

print(f" تم تنظيف البيانات بنجاح: {final_file_path}")
