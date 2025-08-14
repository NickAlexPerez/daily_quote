# Daily Quote App

A simple full-stack app that shows random quotes and lets you add your own.  
Built with Python (Flask) backend and JavaScript frontend.

---

## Technologies Used

- **Backend:**  
  - Python 3  
  - Flask — lightweight web framework  
  - Flask-CORS — enable Cross-Origin Resource Sharing for frontend/backend communication  
  - SQLite — lightweight database to store quotes

- **Frontend:**  
  - HTML, CSS, JavaScript  
  - Fetch API for communicating with the backend

- **Development Environment:**  
  - WSL (Windows Subsystem for Linux)  
  - VS Code for editing  
  - Git for version control

---

## Setup Instructions

### Backend

1. Navigate to the backend folder:

    ```bash
    cd backend
    ```

2. Create and activate a Python virtual environment (recommended):

    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

4. Initialize the database (only needed once):

    ```bash
    python init_db.py
    ```

5. Start the Flask server:

    ```bash
    python app.py
    ```

The backend will run on `http://localhost:5000`.

---

### Frontend

1. Navigate to the frontend folder:

    ```bash
    cd ../frontend
    ```

2. Start a simple HTTP server (Python 3):

    ```bash
    python3 -m http.server 8000
    ```

3. Open your browser and go to:

    ```
    http://localhost:8000/index.html
    ```

---

## Features

- Fetch a random quote from the backend and display it.
- Add a new quote through the frontend form, which stores it in the backend SQLite database.

---

## Notes

- Make sure the backend is running before using the frontend.
- The backend has CORS enabled to allow requests from the frontend.

---

## License

This project is open-source and free to use.

