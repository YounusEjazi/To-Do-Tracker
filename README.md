
# 📝 To-Do Tracker

A full-stack task tracking application built with **Vue.js** (frontend) and **Django REST Framework** (backend). This project helps users manage tasks with support for priorities, deadlines, tags, and more. It uses JWT-based authentication to secure API endpoints and provides a clean, responsive UI.

---

## 🚀 Features

- ✅ User Authentication with JWT
- 🗂️ Create, update, delete tasks
- 📌 Prioritize tasks (Low, Medium, High)
- 🕒 Set due dates and mark overdue tasks
- 🏷️ Add tags and descriptions
- 📎 File attachments
- 📋 Subtasks support (coming soon!)
- 🎨 Responsive and styled UI with Bootstrap 5

---


## 🧰 Getting Started

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/your-username/to-do-tracker.git
cd to-do-tracker
```

### 2️⃣ Backend Setup (Django)

```bash
cd backend
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

### 3️⃣ Frontend Setup (Vue)

```bash
cd todo-frontend
npm install
npm run serve
```

### 4️⃣ Visit the App

Frontend: http://localhost:3000  
Backend API: http://localhost:8000/api/

---

## 📃 License

MIT License – do whatever you want, but give credit 😄
