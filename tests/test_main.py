from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the Task Management System"}

def test_create_task():
    task_data = {"title": "Test Task", "description": "This is a test task"}
    response = client.post("/tasks/", json=task_data)
    assert response.status_code == 200
    assert response.json()["title"] == "Test Task"
    assert response.json()["description"] == "This is a test task"

def test_read_task():
    # สร้าง task ก่อน
    task_data = {"title": "Test Task", "description": "This is a test task"}
    create_response = client.post("/tasks/", json=task_data)
    task_id = create_response.json()["id"]

    # อ่าน task
    response = client.get(f"/tasks/{task_id}")
    assert response.status_code == 200
    assert response.json()["id"] == task_id
    assert response.json()["title"] == "Test Task"
    assert response.json()["description"] == "This is a test task"