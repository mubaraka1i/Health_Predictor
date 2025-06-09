import pandas as pd
import joblib
import os
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler


df = pd.read_csv('data/bodyms.csv')
df.columns = [col.strip().replace(' ', '') for col in df.columns]
df.rename(columns={
    'Waist': 'Waistin',
    'TotalHeight': 'Heightin',
    'Gender': 'GenderBinary'
}, inplace=True)


df.dropna(subset=['GenderBinary', 'Age', 'Heightin', 'Waistin', 'Weightlbs'], inplace=True)
df['GenderBinary'] = df['GenderBinary'].apply(lambda x: 1 if x == 1 else 0)
df = df[(df['Waistin'] > 20) & (df['Waistin'] < 60)]
df = df[(df['Heightin'] > 48) & (df['Heightin'] < 84)]


features = ['Heightin', 'Weightlbs', 'Age', 'GenderBinary']
X = df[features]
y = df['Waistin']


scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
model = LinearRegression()
model.fit(X_scaled, y)


os.makedirs('model', exist_ok=True)
joblib.dump(model, 'model/waist_model.pkl')
joblib.dump(scaler, 'model/waist_scaler.pkl')


