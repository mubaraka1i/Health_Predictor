from flask import Flask, render_template, request
import joblib
import pandas as pd
from region_mapper import map_country_to_macroregion

REGION_BMI_MULTIPLIERS = {
   "North & Australasia": 1.00,
   "Central & South America": 0.92,
   "Middle East & North Africa": 0.92,
   "Sub-Saharan Africa": 0.79,
   "South Asia": 0.75,
   "East Asia": 0.75,
   "Southeast Asia": 0.75,
   "South Pacific": 1.04,
   "Other": 1.00
}

app = Flask(__name__)

waist_model = joblib.load('model/waist_model.pkl')

pants_model = joblib.load('model/pants_model.pkl')
pants_scaler = joblib.load('model/pants_scaler.pkl')
waist_scaler = joblib.load('model/waist_scaler.pkl')

region_df = pd.read_csv('data/region_averages.csv')

def gender_to_binary(g):
    return 1 if g == 'male' else 0

def get_region_defaults(region_input, gender):
    region_input = region_input.lower()
    gb = 1 if gender == 'male' else 0

    for r in region_df['SubjectsBirthLocation'].unique():
        if region_input.strip().lower() == str(r).strip().lower():
            row = region_df[(region_df['SubjectsBirthLocation'] == r) & (region_df['GenderBinary'] == gb)]
            if not row.empty:
                return {
                    'height': float(row['Heightin']),
                    'weight': float(row['Weightlbs']),
                    'waist': float(row['waistcircumference'])
                }

    regional_fallbacks = {
        'north america': {1: 40.5, 0: 38.7},
        'sub-saharan africa': {1: 37.2, 0: 35.8},
        'east asia': {1: 34.0, 0: 31.5},
        'south asia': {1: 35.1, 0: 33.2},
        'europe': {1: 39.8, 0: 37.9},
        'middle east & north africa': {1: 39.0, 0: 36.5},
        'central & south america': {1: 38.2, 0: 36.9},
        'southeast asia': {1: 33.5, 0: 31.1},
        'south pacific': {1: 41.3, 0: 39.0},
        'other': {1: 38.0, 0: 36.0}
    }

    macro = map_country_to_macroregion(region_input)
    waist = regional_fallbacks.get(macro.lower(), regional_fallbacks['other'])[gb]

    return {
        'height': 69.0 if gb == 1 else 63.5,
        'weight': 199.8 if gb == 1 else 170.8,
        'waist': waist
    }

@app.route('/')
def home():
    return render_template('bmi_form.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    gender = request.form['gender'].lower()
    region = request.form['region']
    age = int(request.form['age'])
    weight = float(request.form['weight'])
    feet = int(request.form['feet'])
    inches = int(request.form['inches'])
    height = feet * 12 + inches
    muscle_level = request.form['muscle'].lower()

    muscle_factor = {
        'low': -2,
        'average': 0,
        'high': 3,
        'elite': 7.5
    }.get(muscle_level, 1)

    try:
        waist = float(request.form['waist'])
    except:
        waist = None

    region_defaults = get_region_defaults(region, gender)
    if not waist or waist <= 0:
        waist_features = [[height, weight, age, gender_to_binary(gender)]]
        waist_scaled = waist_scaler.transform(waist_features)
        waist = waist_model.predict(waist_scaled)[0]
        waist = max(6, min(80, waist))

    macroregion = map_country_to_macroregion(region)
    region_multiplier = REGION_BMI_MULTIPLIERS.get(macroregion, 1.00)

    bmi = (weight / (height ** 2)) * 703 * region_multiplier
    bmi_raw = (weight / (height ** 2)) * 703

    is_outlier = height < 60 or height > 75
    if is_outlier:
        bmi *= 0.8

    gender_binary = 1 if gender == 'male' else 0
    pants_features = [[gender_binary, weight, height, age]]
    pants_scaled = pants_scaler.transform(pants_features)
    pants_size = pants_model.predict(pants_scaled)[0]
    pants_size = max(20, min(60, pants_size))

    bodyfat_pred = (
        (1.20 * bmi_raw) +
        (0.23 * age) -
        (10.8 * gender_binary) -
        muscle_factor - 5.4
    )
    bodyfat_pred = max(3, min(50, bodyfat_pred))
    bodyfat = f"{bodyfat_pred:.2f}%"

    bmi_val = bmi_raw
    bf_val = bodyfat_pred

    if bmi_val < 18.5 and bf_val < 20:
        advice = "You're on the leaner side. Focus on nourishing meals and resistance training to build strength and stay energized!"
    elif bmi_val < 18.5 and bf_val >= 20:
        advice = "Even with a lower weight, body fat is a bit high. Consider incorporating strength training to improve tone and metabolism."
    elif 18.5 <= bmi_val < 25 and bf_val < 20:
        advice = "Great job! You're in a healthy BMI and body fat range. Keep up your routine and stay consistent!"
    elif 18.5 <= bmi_val < 25 and bf_val >= 20:
        advice = "Weight is healthy, but body fat could be lower. Try adding strength-focused workouts to improve your composition!"
    elif 25 <= bmi_val < 32 and bf_val < 20:
        advice = "You might have more muscle mass, which can affect body composition. You're likely doing well, so keep training smart!"
    elif 25 <= bmi_val < 32 and bf_val >= 20:
        advice = "There’s room to improve. Start with small, sustainable changes to your diet and add more daily movement."
    elif bmi_val >= 32 and bf_val < 20:
        advice = "High BMI but low body fat usually means strong muscle mass. Keep it up! Stay consistent and monitor energy and joint health."
    else:
        advice = "You're taking the first step by learning your numbers. Begin with gentle activity and nourishing meals. Progress is built one habit at a time!"


    return render_template('bmi_result.html',
                           bmi=f"{bmi:.2f}",
                           bodyfat_known=bodyfat,
                           calculation_method="",
                           gender=gender,
                           waist=f"{waist:.1f}" if waist else "N/A",
                           age=age,
                           region=region,
                           pants_width=f"{pants_size:.1f}",
                           advice=advice)



if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)
