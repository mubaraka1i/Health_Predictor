Health Predictor

This project is a full-stack web application that calculates BMI and estimates body fat percentage using multiple variables to improve accuracy beyond traditional BMI formulas. The calculator takes into account gender, waist size, hip size, region (socioeconomic), height/weight data, and muscle mass status to generate customized results. In addition, it uses regression models trained on previous data to predict estimated pants width based on the user’s measurements.

Features:

- Web-based BMI & Body Fat Calculator
- More accurate estimations using regression models trained on real anthropometric datasets
- User selects their region for more customized results
- Dynamic, interactive front-end using HTML, CSS, and JavaScript
- Backend API powered by Flask and Python
- CSV-based dataset filtering for advanced BMI calculation

Technologies Used:

- Python
- Flask
- HTML / CSS / JavaScript
- Pandas
- Scikit-learn
- CSV datasets

Setup Instructions

1.Clone this repository:
   
   git clone https://github.com/mubaraka1i/BMI_Calculator.git
   
2.Navigate into the project folder:

   cd BMI_Calculator

3.Create a virtual environment:

   python3 -m venv venv         <----
   
   source venv/bin/activate    (For Mac/Linux)
   venv\Scripts\activate       (For Windows)


4.Install packages:

   pip install -r requirements.txt

5.Run app:

   python app.py

