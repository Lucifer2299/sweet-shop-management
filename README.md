🍬 Sweet Shop Management System

A full-stack Sweet Shop Management System built with FastAPI (Backend) and React + Vite (Frontend).
The application supports user authentication, role-based access control, and sweet inventory management with a clean, modern UI.

🚀 Features
🔐 Authentication & Authorization

User registration & login

JWT-based authentication

Role support: admin, staff, customer

Secure password hashing

🍭 Sweet Management

View all sweets

Add new sweets (admin/staff)

Search sweets by:

Name

Category

Price range

🖥 Frontend

Built using React + Vite

Clean UI with plain HTML/CSS

Login & Sweets dashboard

Responsive layout

🗄 Database

SQLite for simplicity

SQLAlchemy ORM

Auto table creation

🧱 Tech Stack
Backend

FastAPI

SQLAlchemy

SQLite

JWT (python-jose)

Passlib (bcrypt)

Frontend

React

Vite

HTML / CSS

Fetch API

📁 Project Structure
sweet-shop-management/
│
├── backend/
│   ├── app/
│   │   ├── api/          # API routes (auth, users, sweets)
│   │   ├── core/         # Security & config
│   │   ├── db/           # Database session
│   │   ├── models/       # SQLAlchemy models
│   │   ├── schemas/      # Pydantic schemas
│   │   ├── services/     # Business logic
│   │   └── main.py       # FastAPI app entry
│   ├── test.db           # SQLite DB
│   └── requirements.txt
│
├── frontend/
│   └── sweet-shop-frontend/
│       ├── src/
│       │   ├── pages/
│       │   ├── context/
│       │   ├── App.jsx
│       │   └── main.jsx
│       └── package.json
│
└── README.md

⚙️ Backend Setup
1️⃣ Create Virtual Environment
cd backend
python3 -m venv venv
source venv/bin/activate

2️⃣ Install Dependencies
pip install -r requirements.txt

3️⃣ Run Backend Server
uvicorn app.main:app --reload


📍 Backend runs at:
http://127.0.0.1:8000

📄 API Docs:

Swagger UI → http://127.0.0.1:8000/docs

OpenAPI → http://127.0.0.1:8000/openapi.json

🎨 Frontend Setup
1️⃣ Install Dependencies
cd frontend/sweet-shop-frontend
npm install

2️⃣ Run Frontend
npm run dev


📍 Frontend runs at:
http://localhost:5173

🔑 API Endpoints
Auth
Method	Endpoint	Description
POST	/api/auth/register	Register user
POST	/api/auth/login	Login user
POST	/api/auth/refresh	Refresh token
Sweets
Method	Endpoint	Description
GET	/api/sweets	List sweets
POST	/api/sweets	Add sweet
GET	/api/sweets/search	Search sweets
🧪 Testing
pytest


All core features are tested including:

Authentication

RBAC

Sweet creation & listing

Search functionality

🔐 Default Roles

New users → customer

Admin role can be assigned directly in DB for testing

📌 Notes

CORS enabled for frontend communication

Admin restriction can be relaxed for demo purposes

Designed for rapid development & learning

👨‍💻 Author

Atharva Durge
GitHub: https://github.com/Lucifer2299

📜 License

This project is for educational and learning purposes.
