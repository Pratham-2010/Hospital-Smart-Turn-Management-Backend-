from flask import Flask
import os
from extension import db
from dotenv import load_dotenv
load_dotenv()


# import models
from models.patient import Patient
from models.department import Department
from models.token_model import Token

# import blueprints
from routes.department_routes import department_bp
from routes.patient_routes import patient_bp
from routes.token_routes import token_bp

app = Flask(__name__)
app.secret_key = "hackathon-secret-key"

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(
    BASE_DIR, "instance", "hospital.db"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

# register blueprints
app.register_blueprint(department_bp)
app.register_blueprint(patient_bp)
app.register_blueprint(token_bp)

@app.route("/")
def home():
    return "Hospital Smart Turn Management System"
if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    print(app.url_map)   # 👈 ADD THIS LINE

    app.run(debug=True)

