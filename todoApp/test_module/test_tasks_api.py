import requests
import csv
import time

BASE_URL = "http://127.0.0.1:9000"

tests = [
    {
        "name": "Get Task List",
        "method": "GET",
        "url": "/Todo/APIv1/tasks/",
        "payload": None,
        "expected_status": 200
    },
    {
        "name": "Create Task Success",
        "method": "POST",
        "url": "/Todo/APIv1/tasks/",
        "payload": {"title": "Task A", "description": "Test", "due_date": "2025-01-10", "status": "pending"},
        "expected_status": 201
    },
    {
        "name": "Create Task Minimal",
        "method": "POST",
        "url": "/Todo/APIv1/tasks/",
        "payload": {"title": "Only Title"},
        "expected_status": 201
    },
    {
        "name": "Create Task Invalid Missing Title",
        "method": "POST",
        "url": "/Todo/APIv1/tasks/",
        "payload": {"description": "Invalid"},
        "expected_status": 400
    },
    {
        "name": "Create Task Empty Title",
        "method": "POST",
        "url": "/Todo/APIv1/tasks/",
        "payload": {"title": ""},
        "expected_status": 400
    },
    {
        "name": "Create Task Status Invalid Enum",
        "method": "POST",
        "url": "/Todo/APIv1/tasks/",
        "payload": {"title": "Bad", "status": "done"},
        "expected_status": 400
    },
    {
        "name": "Create Task Invalid Date",
        "method": "POST",
        "url": "/Todo/APIv1/tasks/",
        "payload": {"title": "Date Test", "due_date": "2025-99-99"},
        "expected_status": 400
    },
    {
        "name": "Create Task With Null Fields",
        "method": "POST",
        "url": "/Todo/APIv1/tasks/",
        "payload": {"title": "Null Example", "description": None, "due_date": None},
        "expected_status": 201
    },
    {
        "name": "Create Task Huge Description",
        "method": "POST",
        "url": "/Todo/APIv1/tasks/",
        "payload": {"title": "Huge", "description": "x"*5000},
        "expected_status": 201
    },
    {
        "name": "Create Task SQL Injection Attempt",
        "method": "POST",
        "url": "/Todo/APIv1/tasks/",
        "payload": {"title": "1 OR 1=1", "description": "'; DROP TABLE tasks; --"},
        "expected_status": 201
    },
    {
        "name": "Get Valid Task 1",
        "method": "GET",
        "url": "/Todo/APIv1/tasks/1/",
        "payload": None,
        "expected_status": 200
    },
    {
        "name": "Get Task Not Exist",
        "method": "GET",
        "url": "/Todo/APIv1/tasks/999999/",
        "payload": None,
        "expected_status": 404
    },
    {
        "name": "Get Task Negative ID",
        "method": "GET",
        "url": "/Todo/APIv1/tasks/-1/",
        "payload": None,
        "expected_status": 400
    },
    {
        "name": "Update Task Success",
        "method": "POST",
        "url": "/Todo/APIv1/tasks/1/update/",
        "payload": {"title": "Updated Title"},
        "expected_status": 200
    },
    {
        "name": "Update Task Missing Title",
        "method": "POST",
        "url": "/Todo/APIv1/tasks/1/update/",
        "payload": {"description": "Missing title"},
        "expected_status": 400
    },
    {
        "name": "Update Task Empty JSON",
        "method": "POST",
        "url": "/Todo/APIv1/tasks/1/update/",
        "payload": {},
        "expected_status": 400
    },
    {
        "name": "Update Non-Existing Task",
        "method": "POST",
        "url": "/Todo/APIv1/tasks/9999/update/",
        "payload": {"title": "New"},
        "expected_status": 404
    },
    {
        "name": "Update Task Invalid Method",
        "method": "GET",
        "url": "/Todo/APIv1/tasks/1/update/",
        "payload": None,
        "expected_status": 405
    },
    {
        "name": "Delete Existing Task",
        "method": "DELETE",
        "url": "/Todo/APIv1/tasks/1/",
        "payload": None,
        "expected_status": 200
    },
    {
        "name": "Delete Already Deleted Task",
        "method": "DELETE",
        "url": "/Todo/APIv1/tasks/1/",
        "payload": None,
        "expected_status": 500
    },
    {
        "name": "Delete Task Invalid ID",
        "method": "DELETE",
        "url": "/Todo/APIv1/tasks/abc/",
        "payload": None,
        "expected_status": 404
    },
    {
        "name": "Wrong Method On Delete",
        "method": "POST",
        "url": "/Todo/APIv1/tasks/2/",
        "payload": None,
        "expected_status": 405
    },
    {
        "name": "Wrong Method On List",
        "method": "PUT",
        "url": "/Todo/APIv1/tasks/",
        "payload": None,
        "expected_status": 405
    },
    {
        "name": "List Tasks After Operations",
        "method": "GET",
        "url": "/Todo/APIv1/tasks/",
        "payload": None,
        "expected_status": 200
    },
    {
        "name": "Create Task With Long Title",
        "method": "POST",
        "url": "/Todo/APIv1/tasks/",
        "payload": {"title": "T"*300},
        "expected_status": 201
    },
    {
        "name": "Update Task With Long Description",
        "method": "POST",
        "url": "/Todo/APIv1/tasks/2/update/",
        "payload": {"title": "Updated", "description": "Y"*3000},
        "expected_status": 200
    },
    {
        "name": "Get Task Zero ID",
        "method": "GET",
        "url": "/Todo/APIv1/tasks/0/",
        "payload": None,
        "expected_status": 400
    },
    {
        "name": "Update Task Invalid Status Enum",
        "method": "POST",
        "url": "/Todo/APIv1/tasks/2/update/",
        "payload": {"title": "Bad", "status": "unknown"},
        "expected_status": 400
    }
]


results = []

for t in tests:
    url = BASE_URL + t["url"]
    method = t["method"]
    payload = t["payload"]

    try:
        if method == "GET":
            r = requests.get(url)
        elif method == "POST":
            r = requests.post(url, json=payload)
        elif method == "DELETE":
            r = requests.delete(url)
        elif method == "PUT":
            r = requests.put(url)
        else:
            r = None

        status = r.status_code if r else 0
        result = "PASS" if status == t["expected_status"] else "FAIL"

        results.append([t["name"], method, url, status, t["expected_status"], result])

        time.sleep(0.3)

    except Exception as e:
        results.append([t["name"], method, url, str(e), t["expected_status"], "ERROR"])

with open("api_test_results.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["Test Name", "Method", "URL", "Actual Status", "Expected Status", "Result"])
    w.writerows(results)

print("API Test Completed. CSV Generated: api_test_results.csv")
