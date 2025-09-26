import pandas as pd
import numpy as np
import re

def parse_damage(value: str) -> float:
    """Convert NOAA damage strings like '10.00K', '2.5M', '1.2B' to float dollars."""
    if value is None or (isinstance(value, float) and np.isnan(value)):
        return 0.0
    s = str(value).strip()
    if s == '' or s == '0.00K':
        return 0.0
    m = re.match(r'^(?P<num>[0-9.]+)\s*(?P<suf>[KMB])$', s, re.IGNORECASE)
    if not m:
        return np.nan
    num = float(m.group('num'))
    suf = m.group('suf').upper()
    mult = {'K':1e3, 'M':1e6, 'B':1e9}[suf]
    return num * mult

def add_time_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df['begin_date_time'] = pd.to_datetime(df['begin_date_time'], errors='coerce')
    df['year'] = df['begin_date_time'].dt.year
    df['month'] = df['begin_date_time'].dt.month
    # Seasons: DJF, MAM, JJA, SON
    bins = [0,2,5,8,11,12]
    labels = ['DJF','MAM','JJA','SON','DJF']
    df['season'] = pd.Categorical(pd.cut(df['month'], bins=bins, labels=labels, include_lowest=True))
    return df
