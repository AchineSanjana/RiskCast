import pandas as pd
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.ensemble import RandomForestRegressor
from joblib import dump

from src.features import parse_damage, add_time_features

RAW = Path('data/raw')
csv = next(RAW.glob('StormEvents_details-*.csv'), None)
assert csv is not None, 'Put your StormEvents_details-*.csv into data/raw first.'

print(f'Loading: {csv}')
df = pd.read_csv(csv, low_memory=False)

# Target
df['damage_property_num'] = df['damage_property'].apply(parse_damage)

# Features
df = add_time_features(df)
features = ['event_type','state','month','season','magnitude','magnitude_type','begin_lat','begin_lon']
df = df[features + ['damage_property_num']].copy()

X = df[features]
y = df['damage_property_num']

num = ['month','magnitude','begin_lat','begin_lon']
cat = ['event_type','state','season','magnitude_type']

pre = ColumnTransformer([
    ('num', SimpleImputer(strategy='median'), num),
    ('cat', Pipeline([('imp', SimpleImputer(strategy='most_frequent')),
                      ('oh', OneHotEncoder(handle_unknown='ignore'))]), cat)
])

model = RandomForestRegressor(n_estimators=300, random_state=42, n_jobs=-1)
pipe = Pipeline([('pre', pre), ('model', model)])

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
pipe.fit(X_train, y_train)

pred = pipe.predict(X_test)
rmse = mean_squared_error(y_test, pred, squared=False)
mae  = mean_absolute_error(y_test, pred)
r2   = r2_score(y_test, pred)
print({'RMSE': rmse, 'MAE': mae, 'R2': r2})

Path('models').mkdir(parents=True, exist_ok=True)
dump(pipe, 'models/storm_damage_model.joblib')
print('Saved model -> models/storm_damage_model.joblib')
