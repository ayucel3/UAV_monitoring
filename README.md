# UAV Application Setup Guide

This guide provides step-by-step instructions to set up and run the backend and frontend components of the UAV application on your local machine.

## Prerequisites

- [Python](https://www.python.org/downloads/) (Python 3.11.4)
- [Node.js](https://nodejs.org/) (version: 20.12.2)
- [Visual Studio Code](https://code.visualstudio.com/) or command line interface

## Backend Setup (Flask)

1. **Navigate to the Backend Folder:**

   ```bash
   cd uav_backend
   ```

2. **Create and Activate a Virtual Environment:**

   - For Windows:
     ```bash
     python -m venv venv
     .\venv\Scripts\Activate
     ```
   - For Unix/Mac:
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```

3. **Install Dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Backend Server:**

   ```bash
   python run.py
   ```

   The backend server should now be running in your local environment.

5. **Run Test Cases (Optional):**
   ```bash
   python tests\test.py
   ```

## Frontend Setup (Vue.js)

1. **Open a New Terminal and Navigate to the Frontend Folder:**

   ```bash
   cd uav_frontend
   ```

2. **Install Dependencies:**

   ```bash
   npm install
   ```

3. **Run the Frontend Development Server:**
   ```bash
   npm run dev
   ```
   You can now access the frontend by visiting the localhost link provided in your terminal.

## Additional Information

- The database has been pre-populated with some data, so you can start interacting with the website immediately after setup.
