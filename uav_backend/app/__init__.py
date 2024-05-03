from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config  
from flask_cors import CORS

db = SQLAlchemy()

def seed_database():
    from .models import Drone, Task

    # Clear existing data
    db.session.query(Task).delete()
    db.session.query(Drone).delete()
    db.session.commit()

    # Adding new drones
    drones = [
        Drone(name='Drone 1'),
        Drone(name='Drone 2'),
        Drone(name='Drone 3')
    ]
    db.session.bulk_save_objects(drones)
    db.session.commit()  # Make sure drones are committed to get their IDs

    drones = Drone.query.all()
    # Adding new tasks
    tasks = [
        Task(name='Photography', description='Aerial photography task', drone_id=drones[0].id),
        Task(name='Surveillance', description='Area surveillance task', drone_id=drones[1].id),
        Task(name='Delivery', description='Package delivery task', drone_id=drones[2].id),
        Task(name='Support', description='Support task', drone_id=drones[2].id)

    ]
    db.session.bulk_save_objects(tasks)
    db.session.commit()



def create_app(config_class=Config):
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(config_class)  

    db.init_app(app)

    with app.app_context():
        from .routes import api_blueprint
        app.register_blueprint(api_blueprint, url_prefix='/api')

        db.create_all()  
        seed_database()
    return app
