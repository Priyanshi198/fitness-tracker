from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

# Initialize Flask App
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///fitness.db'
app.config['SECRET_KEY'] = 'b891ae14748f0f74c2e409010488f3455d93f4e1bffbefa3'
db = SQLAlchemy(app)

# Fitness Data Model
class FitnessData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    exercise = db.Column(db.String(100), nullable=False)
    duration = db.Column(db.Float, nullable=False)
    calories = db.Column(db.Float, nullable=False)
    water_intake = db.Column(db.Float, nullable=False)

# Goals Model
class Goal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    calorie_goal = db.Column(db.Float, nullable=False)
    water_goal = db.Column(db.Float, nullable=False)

# Home Route
@app.route('/')
def index():
    return render_template('index.html')

# Add Fitness Data
@app.route('/add', methods=['GET', 'POST'])
def add_data():
    if request.method == 'POST':
        try:
            exercise = request.form['exercise']
            duration = float(request.form['duration'])
            calories = float(request.form['calories'])
            water_intake = float(request.form['water_intake'])

            new_data = FitnessData(exercise=exercise, duration=duration, calories=calories, water_intake=water_intake)
            db.session.add(new_data)
            db.session.commit()

            flash('Fitness data added successfully!', 'success')
        except Exception as e:
            flash(f"Error: {str(e)}", 'danger')
        return redirect('/view')

    return render_template('add.html')

# Generate Exercise Recommendations
def generate_recommendations(data):
    if not data:
        return {"No Data": ["Add some fitness data to get recommendations!"]}

    total_calories = sum(item.calories for item in data)
    total_duration = sum(item.duration for item in data)

    # Recommendations based on Calories Burned and Exercise Duration
    recommendations = {
        "Fat Loss": [
            "Try High-Intensity Interval Training (HIIT) for fat burning.",
            "Add running or cycling for better cardiovascular health.",
            "Incorporate strength training to build lean muscle."
        ],
        "Muscle Gain": [
            "Focus on resistance training like weightlifting.",
            "Try compound movements like squats, deadlifts, and bench presses.",
            "Increase your protein intake and ensure proper rest."
        ],
        "Flexibility & Recovery": [
            "Incorporate yoga or Pilates for better flexibility.",
            "Try foam rolling and stretching exercises.",
            "Prioritize rest days and active recovery."
        ],
        "Overall Fitness": [
            "Mix cardio, strength, and flexibility exercises.",
            "Join fitness classes or try group training for motivation.",
            "Track progress to stay consistent."
        ]
    }

    # Adjust Recommendations Based on Activity
    if total_calories > 2000 or total_duration > 300:
        return {"Muscle Gain": recommendations["Muscle Gain"]}
    elif total_calories > 1000:
        return {"Fat Loss": recommendations["Fat Loss"]}
    else:
        return {"Overall Fitness": recommendations["Overall Fitness"]}

# View Fitness Data
@app.route('/view')
def view_data():
    data = FitnessData.query.all()
    recommendations = generate_recommendations(data)
    return render_template('view.html', data=data, recommendations=recommendations)

# Set Goal
@app.route('/set-goal', methods=['POST'])
def set_goal():
    try:
        calorie_goal = float(request.form.get('calorie_goal'))
        water_goal = float(request.form.get('water_goal'))
        
        goal = Goal.query.first()
        if not goal:
            goal = Goal(calorie_goal=calorie_goal, water_goal=water_goal)
            db.session.add(goal)
        else:
            goal.calorie_goal = calorie_goal
            goal.water_goal = water_goal
        db.session.commit()
        flash('Goals updated successfully!', 'success')
    except Exception as e:
        flash(f"Error: {str(e)}", 'danger')
    return redirect('/view')

# Create Database if it Doesn't Exist
with app.app_context():
    db.create_all()

# Run the App
if __name__ == '__main__':
    app.run(debug=True)
