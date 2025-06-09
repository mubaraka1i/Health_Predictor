import pandas as pd
import joblib
import os
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler



csv_path = 'data/bodyms.csv'

df = pd.read_csv(csv_path)


df.columns = [col.strip().replace(' ', '') for col in df.columns]
df.rename(columns={
    'Waist': 'Waistin',
    'TotalHeight': 'Heightin',
    'Gender': 'GenderBinary'
}, inplace=True)



required_columns = ['GenderBinary', 'Age', 'Heightin', 'Waistin', 'Weightlbs']


df.dropna(subset=required_columns, inplace=True)


df['GenderBinary'] = df['GenderBinary'].apply(lambda x: 1 if x == 1 else 0)


df = df[(df['Waistin'] > 20) & (df['Waistin'] < 60)]
df = df[(df['Heightin'] > 48) & (df['Heightin'] < 84)]



df['PantsWaistInches'] = (df['Waistin'] - 2).clip(lower=20)



features = ['Heightin', 'Weightlbs', 'Age', 'GenderBinary']



X = df[features]
y = df['PantsWaistInches']


scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)


model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_scaled, y)


os.makedirs('model', exist_ok=True)
joblib.dump(model, 'model/pants_model.pkl')
joblib.dump(scaler, 'model/pants_scaler.pkl')


importances = pd.Series(model.feature_importances_, index=features).sort_values(ascending=False)
print("Top Feature Importances:\n", importances)
