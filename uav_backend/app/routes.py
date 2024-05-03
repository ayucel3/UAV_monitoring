from flask import Blueprint, request, jsonify, abort
from .models import db, Drone, Task, Image
from .utils import generate_noisy_image
import base64

api_blueprint = Blueprint('api', __name__)

@api_blueprint.route('/drones', methods=['GET'])
def get_drones():
    try:
        drones = Drone.query.all()
        return jsonify([{'id': drone.id, 'name': drone.name} for drone in drones])
    except Exception as e:
        abort(500, description=f"Internal Server Error: {str(e)}")

@api_blueprint.route('/tasks', methods=['POST'])
def create_task():
    try:
        data = request.json
        if not data or 'name' not in data or 'drone_id' not in data:
            abort(400, description="Missing required fields: 'name' and 'drone_id' must be provided.")

        task = Task(name=data['name'], description=data.get('description', ''), drone_id=data['drone_id'])
        db.session.add(task)
        db.session.commit()
        return jsonify({'id': task.id, 'name': task.name, 'description': task.description, 'drone_id': task.drone_id}), 201
    except Exception as e:
        db.session.rollback()
        abort(500, description=f"Internal Server Error: {str(e)}")

@api_blueprint.route('/tasks', methods=['GET'])
def get_tasks():
    try:
        tasks = Task.query.filter(Task.is_deleted == False).all()  # Only fetch tasks that are not deleted
        return jsonify([{'id': task.id, 'name': task.name, 'description': task.description, 'drone_id': task.drone_id, 'is_executed' : task.is_executed } for task in tasks])
    except Exception as e:
        abort(500, description=f"Internal Server Error: {str(e)}")


@api_blueprint.route('/tasks/<int:id>', methods=['GET'])
def get_task(id):
    try:
        task = Task.query.filter_by(id=id, is_deleted=False).first_or_404()  # Ensure the task is not deleted
        return jsonify({'id': task.id, 'name': task.name, 'description': task.description, 'drone_id': task.drone_id , 'is_executed' : task.is_executed})
    except Exception as e:
        abort(500, description=f"Internal Server Error: {str(e)}")


@api_blueprint.route('/tasks/<int:id>/execute', methods=['POST'])
def execute_task(id):
    try:
        task = Task.query.get_or_404(id)
        task.is_executed = True
        images = [generate_noisy_image() for _ in range(5)]
        for img in images:
            image = Image(task_id=task.id, image_data=img)
            db.session.add(image)
        db.session.commit()
        return jsonify({'message': 'Task executed and images captured'}), 201
    except Exception as e:
        db.session.rollback()
        abort(500, description=f"Internal Server Error: {str(e)}")

@api_blueprint.route('/tasks/<int:id>/images', methods=['GET'])
def get_images(id):
    try:
        images = Image.query.filter_by(task_id=id).all()
        images_base64 = [base64.b64encode(image.image_data).decode('utf-8') for image in images]
        return jsonify({'images': images_base64})
    except Exception as e:
        abort(500, description=f"Internal Server Error: {str(e)}")

@api_blueprint.route('/images', methods=['GET'])
def get_all_images():
    try:
        images = Image.query.all()
        images_base64 = [base64.b64encode(image.image_data).decode('utf-8') for image in images]
        return jsonify({'images': images_base64})
    except Exception as e:
        abort(500, description=f"Internal Server Error: {str(e)}")

@api_blueprint.route('/tasks/<int:id>', methods=['DELETE'])
def delete_task(id):
    try:
        task = Task.query.get_or_404(id)
        task.is_deleted = True  
        db.session.commit()
        return jsonify({'message': 'Task deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        abort(500, description=f"Internal Server Error: {str(e)}")
