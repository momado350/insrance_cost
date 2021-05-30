from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
#import model
def analyze_smoker(smoker_status):
    if smoker_status == 1:
        return ("To lower your cost, you should consider quitting smoking.")
    else:
        return ("Smoking is not an issue for you.")
        

    
#define analyze_bmi function
def analyze_bmi(bmi_value):
    if bmi_value > 30:
        return ("Your BMI is in the obese range. To lower your cost, you should significantly lower your BMI.")
    elif bmi_value >= 25 and bmi_value <= 30:
        return ("Your BMI is in the overweight range. To lower your cost, you should lower your BMI.")
    elif bmi_value >= 18.5 and bmi_value < 25:
        return ("Your BMI is in a healthy range.")
    else:
        return ("Your BMI is in the underweight range. Increasing your BMI will not help lower your cost, but it will help improve your health.")
    
 #define a Function to estimate insurance cost:
def estimate_insurance_cost(name, age, sex, bmi, num_of_children, smoker):
    estimated_cost = 250*age - 128*sex + 370*bmi + 425*num_of_children + 24000*smoker - 12500
    return (name + "'s Estimated Insurance Cost is: " + str(estimated_cost) + " dollars." + analyze_bmi(bmi) + analyze_smoker(smoker))
    
    return estimated_cost
   
app = Flask(__name__)

ENV = 'dev'

if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost/insurance'
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = ''

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Estimate(db.Model):
    __tablename__ = 'estimator1'
    id = db.Column(db.Integer, primary_key=True)
    name_input = db.Column(db.String(200), unique=True)
    sex_input = db.Column(db.Integer)
    age_input = db.Column(db.Integer)
    bmi_input = db.Column(db.Float)
    children_input = db.Column(db.Integer)
    smoker_input = db.Column(db.Integer)
    

    def __init__(self, name_input, sex_input, age_input, bmi_input, children_input, smoker_input):
        self.name_input = name_input
        self.sex_input = sex_input
        self.age_input = age_input
        self.bmi_input = bmi_input
        self.children_input = children_input
        self.smoker_input = smoker_input
        


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        name_input = request.form['name_input']
        sex_input = int(request.form['sex_input'])
        age_input =  int(request.form['age_input'])
        bmi_input = float(request.form['bmi_input'])
        children_input = int(request.form['children_input'])
        smoker_input = int(request.form['smoker_input'])
        user_insurance_cost = estimate_insurance_cost(name= name_input, age = int(age_input), sex = int(sex_input), bmi = float(bmi_input), num_of_children = int(children_input), smoker = int(smoker_input))
        
        if name_input == '' or sex_input == None or  age_input == None or  bmi_input == None or children_input == None or  smoker_input == None:
            return render_template('index.html', message='Please enter required fields')
        if db.session.query(Estimate).filter(Estimate.name_input == name_input).count() == 0:
            data = Estimate(name_input, sex_input, age_input, bmi_input, children_input, smoker_input)
            db.session.add(data)
            db.session.commit()
            return render_template('success.html', user_insurance_cost=user_insurance_cost)
        return render_template('index.html', message='You have already estimated your insurance cost. Check your Email or use a different name if you considring another cost estimate!')

        
        
        
    #return render_template('index.html', name_input=name_input, sex_input=sex_input, age_input=age_input, bmi_input=bmi_input, children_input=children_input, smoker_input=smoker_input, user_insurance_cost=user_insurance_cost) 
   
if __name__ == '__main__':
    
    app.run()

        
        




