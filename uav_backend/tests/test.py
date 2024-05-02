import sys
import os
import unittest
from flask import json
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db
from app.models import Drone, Task, Image
from app.utils import generate_noisy_image



class UAVBackendTestCase(unittest.TestCase):

    def setUp(self):
        """Set up test variables and initialize app."""
        from config import TestConfig
        self.app = create_app(TestConfig)
        self.client = self.app.test_client()
        self.ctx = self.app.app_context()
        self.ctx.push() 
        db.create_all()

    def tearDown(self):
        """Tear down all initialized variables."""
        db.session.remove()
        db.drop_all()
        self.ctx.pop()  

    def test_get_drones(self):
        """Test API can get a list of drones (GET request)."""
        drone = Drone(name='Test Drone')
        db.session.add(drone)
        db.session.commit()

        res = self.client.get('/api/drones')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['name'], 'Test Drone')

    def test_create_task(self):
        """Test API can create a task (POST request)."""
        drone = Drone(name='Task Drone')
        db.session.add(drone)
        db.session.commit()

        db.session.refresh(drone)

        res = self.client.post('/api/tasks', json={
            'name': 'New Task',
            'description': 'Test Description',
            'drone_id': drone.id
        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 201)
        self.assertEqual(data['name'], 'New Task')

    def test_get_task(self):
        """Test API can get details of a specific task (GET request)."""
        with self.app.app_context():  
            drone = Drone(name='Task Drone')
            db.session.add(drone)
            db.session.commit()  

            task = Task(name='Specific Task', description='Detailed Description', drone_id=drone.id)
            db.session.add(task)
            db.session.commit()  

            res = self.client.get(f'/api/tasks/{task.id}')
            data = json.loads(res.data)
            self.assertEqual(res.status_code, 200)
            self.assertEqual(data['name'], 'Specific Task')
            self.assertEqual(data['description'], 'Detailed Description')
            self.assertEqual(data['drone_id'], drone.id)

    def test_execute_task(self):
        """Test API can execute a task and capture images (POST request)."""
        from config import TestConfig
        self.app = create_app(TestConfig)
        self.client = self.app.test_client()
        with self.app.app_context():
            drone = Drone(name='Task Drone')
            db.session.add(drone)
            db.session.commit() 

            task = Task(name='Executable Task', description='Execute Description', drone_id=drone.id)
            db.session.add(task)
            db.session.commit()

            res = self.client.post(f'/api/tasks/{task.id}/execute')
            data = json.loads(res.data)
            self.assertEqual(res.status_code, 201)
            self.assertEqual(data['message'], 'Task executed and images captured')

            images = Image.query.filter_by(task_id=task.id).all()
            self.assertEqual(len(images), 5)  

    def test_get_images(self):
        """Test API can get images for a specific task (GET request)."""
        with self.app.app_context():
            drone = Drone(name='Task Drone')
            db.session.add(drone)
            db.session.commit() 

            task = Task(name='Image Task', description='Task with Images', drone_id=drone.id)
            db.session.add(task)
            db.session.commit()  

            images_data = [generate_noisy_image() for _ in range(3)]
            for img_data in images_data:
                image = Image(task_id=task.id, image_data=img_data)
                db.session.add(image)
            db.session.commit()  

            res = self.client.get(f'/api/tasks/{task.id}/images')
            data = json.loads(res.data)
            self.assertEqual(res.status_code, 200)
            self.assertEqual(len(data['images']), 3)  

if __name__ == '__main__':
    unittest.main()