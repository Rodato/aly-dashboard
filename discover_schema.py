"""Run this once to see all tables and columns available in Supabase.

Usage:
    python3 discover_schema.py
"""
from utils.db import get_schema_info

df = get_schema_info()
if "error" in df.columns:
    print("Error:", df["error"].iloc[0])
else:
    print(df.to_string(index=False))
