# 📝 Django To-Do List Application

A simple **Task Management Web Application** built using **Django**.  
The project provides **RESTful APIs** for CRUD operations on tasks, along with **HTML templates** for displaying and creating tasks.

---

## 🚀 Features

### ✅ RESTful Task API
- Create a new task  
- Retrieve all tasks  
- Retrieve a single task  
- Update an existing task  
- Delete a task  
- API accepts and returns **JSON**

### 🖥️ Web Interface (Templates)
- View all tasks  
- Add a new task using a form  
- UI communicates with backend API routes

### 🗄️ Database
- Uses **SQLite**
- Task model includes:
  - `title`
  - `description`
  - `due_date`
  - `status` (Pending/Completed)

### 🧪 Testing
- Automated tests for all CRUD API endpoints  
- Using Django Test Framework / Pytest

### 🔐 Logging & Error Handling
- Logging added using Django’s logging system  
- Clean exception handling

## ⚙️ Installation & Setup

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/harshsoni21/ToDO.git
cd ToDO
pip install -r requirements.txt
python manage.py runserver
``` 

## We Can Add JWT based Authentication in Future if Need Required.




