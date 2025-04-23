
import os
import pandas as pd
from supabase import create_client

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

df = pd.read_csv("output/dn_supabase_ready.csv")
BATCH_SIZE = 100
table_name = "dn"

for start in range(0, len(df), BATCH_SIZE):
    batch = df.iloc[start:start+BATCH_SIZE]
    data = batch.to_dict(orient="records")
    response = supabase.table(table_name).insert(data).execute()
    print(f"✅ Inserido batch {start}–{start+len(batch)-1}")
