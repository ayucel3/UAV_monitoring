from . import db

class Drone(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255))
    drone_id = db.Column(db.Integer, db.ForeignKey('drone.id'), nullable=False)
    drone = db.relationship('Drone', backref=db.backref('tasks', lazy=True))

class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey('task.id'), nullable=False)
    image_data = db.Column(db.LargeBinary, nullable=False)
    task = db.relationship('Task', backref=db.backref('images', lazy=True))
