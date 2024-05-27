from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.debug = True

# Adding configuration for using a SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Creating an SQLAlchemy instance
db = SQLAlchemy(app)

# Settings for migrations
migrate = Migrate(app, db)

# Models
class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20), nullable=False)
    age = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Name: {self.first_name} {self.last_name}, Age: {self.age}"

# Function to render index page
@app.route('/')
def index():
    profiles = Profile.query.all()
    return render_template('index.html', profiles=profiles)

# Function to render add profile page
@app.route('/add_data')
def add_data():
    return render_template('add_profile.html')

# Function to add profiles
@app.route('/add', methods=["POST"])
def profile():
    first_name = request.form.get("first_name")
    last_name = request.form.get("last_name")
    age = request.form.get("age")

    if first_name and last_name and age:
        try:
            age = int(age)
            p = Profile(first_name=first_name, last_name=last_name, age=age)
            db.session.add(p)
            db.session.commit()
            return redirect('/')
        except ValueError:
            # Handle the case where age is not an integer
            app.logger.error(f"Invalid age value: {age}")
            return redirect('/add_data')
        except Exception as e:
            # General exception handling for database errors
            db.session.rollback()
            app.logger.error(f"Error adding profile: {e}")
            return redirect('/add_data')
    else:
        # Handle the case where form data is missing
        app.logger.error("Missing form data")
        return redirect('/add_data')

# Function to delete profiles
@app.route('/delete/<int:id>')
def erase(id):
    data = Profile.query.get(id)
    if data:
        try:
            db.session.delete(data)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            app.logger.error(f"Error deleting profile: {e}")
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
