# Mkulima Chapchap - React + Flask Full Stack App

Mkulima Chapchap is a simple veterinary farm health management app. It helps a farmer register, log in, add animals, track animal weights, record vaccination/deworming/medical/breeding records, record costs and sale price, and view upcoming health reminders.

This project is intentionally simple and bootcamp-friendly, but it is fully functional and meets the listed React + Flask full-stack requirements.

---

## 1. Project Features

### Authentication

- Register a new user/farmer
- Login using email and password
- Logout from the frontend and backend
- JWT authentication using `Flask-JWT-Extended`
- Protected backend routes using `@jwt_required()`
- Protected frontend pages using React Router

### Farm Records

- Add animals
- View all animals belonging to the logged-in user
- View one animal with its records
- Update animal details
- Delete animal records
- Record animal weight history
- Record vaccination dates
- Record deworming schedules
- Record medical costs
- Record breeding costs
- Record sale price when an animal is sold
- View upcoming health reminders due in the next 30 days
- Favorite animals to demonstrate a many-to-many relationship

---

## 2. Requirements Checklist

### Frontend Requirements

| Requirement                 | Implemented? | Where                                 |
| --------------------------- | -----------: | ------------------------------------- |
| React functional components |          Yes | All components/pages use functions    |
| React Hooks                 |          Yes | `useState`, `useEffect`, `useContext` |
| React Router                |          Yes | `src/App.jsx`                         |
| Consume Flask backend       |          Yes | `src/services/api.js` uses `fetch`    |
| Clean responsive UI         |          Yes | `src/styles.css`                      |
| Home page                   |          Yes | `src/pages/Home.jsx`                  |
| Login/Register page         |          Yes | `src/pages/LoginRegister.jsx`         |
| Dashboard/main page         |          Yes | `src/pages/Dashboard.jsx`             |
| Protected routes            |          Yes | `src/components/ProtectedRoute.jsx`   |
| Context/state management    |          Yes | `src/context/AuthContext.jsx`         |
| Components folder           |          Yes | `src/components`                      |
| Pages folder                |          Yes | `src/pages`                           |
| Services/API folder         |          Yes | `src/services`                        |

### Backend Requirements

| Requirement           | Implemented? | Where                                                     |
| --------------------- | -----------: | --------------------------------------------------------- |
| Flask                 |          Yes | `backend/app.py`                                          |
| Flask SQLAlchemy      |          Yes | `backend/extensions.py`, `backend/models`                 |
| REST API principles   |          Yes | `/api/...` endpoints                                      |
| SQLite or PostgreSQL  |          Yes | SQLite by default; PostgreSQL supported by `DATABASE_URL` |
| Proper models         |          Yes | `backend/models/__init__.py`                              |
| Routes/Blueprints     |          Yes | `backend/routes`                                          |
| Serializers           |          Yes | `to_dict()` methods in models                             |
| CRUD operations       |          Yes | Animals, weights, health records                          |
| Environment variables |          Yes | `.env.example`, `config.py`                               |
| JWT authentication    |          Yes | `auth_routes.py`                                          |
| Seed file             |          Yes | `backend/seed.py`                                         |

---

## 3. Database Relationships

### One-to-Many Relationship

One user can have many animals.

```python
User.animals -> Animal.owner
```

Also, one animal can have many weight records and many health records.

```python
Animal.weights -> WeightRecord.animal
Animal.health_records -> HealthRecord.animal
```

### Many-to-Many Relationship

Many users can favorite many animals.

```python
User.favorite_animals <-> Animal.favorited_by
```

This is implemented using the `favorites` association table.

---

## 4. Protected Backend Routes

The project has more than 10 protected routes. These routes require a valid JWT token in the `Authorization` header.

| No. | Method | Route                              | Purpose                 |
| --: | ------ | ---------------------------------- | ----------------------- |
|   1 | POST   | `/api/auth/logout`                 | Logout confirmation     |
|   2 | GET    | `/api/auth/me`                     | Get logged-in user      |
|   3 | GET    | `/api/animals`                     | List user animals       |
|   4 | POST   | `/api/animals`                     | Add animal              |
|   5 | GET    | `/api/animals/<id>`                | View one animal         |
|   6 | PUT    | `/api/animals/<id>`                | Update animal           |
|   7 | DELETE | `/api/animals/<id>`                | Delete animal           |
|   8 | POST   | `/api/animals/<id>/favorite`       | Favorite animal         |
|   9 | DELETE | `/api/animals/<id>/favorite`       | Unfavorite animal       |
|  10 | GET    | `/api/animals/<id>/weights`        | List weights            |
|  11 | POST   | `/api/animals/<id>/weights`        | Add weight              |
|  12 | DELETE | `/api/weights/<id>`                | Delete weight           |
|  13 | GET    | `/api/animals/<id>/health-records` | List health records     |
|  14 | POST   | `/api/animals/<id>/health-records` | Add health record       |
|  15 | PUT    | `/api/health-records/<id>`         | Update health record    |
|  16 | DELETE | `/api/health-records/<id>`         | Delete health record    |
|  17 | GET    | `/api/reminders`                   | View upcoming reminders |

---

## 5. Project Structure

```txt
mkulima-chapchap/
├── README.md
├── backend/
│   ├── .env.example
│   ├── .gitignore
│   ├── app.py
│   ├── config.py
│   ├── extensions.py
│   ├── requirements.txt
│   ├── seed.py
│   ├── models/
│   │   └── __init__.py
│   └── routes/
│       ├── __init__.py
│       ├── animal_routes.py
│       ├── auth_routes.py
│       ├── record_routes.py
│       └── reminder_routes.py
└── frontend/
    ├── .env.example
    ├── .gitignore
    ├── index.html
    ├── package.json
    └── src/
        ├── App.jsx
        ├── main.jsx
        ├── styles.css
        ├── components/
        │   ├── AnimalCard.jsx
        │   ├── Navbar.jsx
        │   └── ProtectedRoute.jsx
        ├── context/
        │   └── AuthContext.jsx
        ├── pages/
        │   ├── AnimalDetails.jsx
        │   ├── Dashboard.jsx
        │   ├── Home.jsx
        │   ├── LoginRegister.jsx
        │   └── NotFound.jsx
        └── services/
            └── api.js
```

---

## 6. Backend Setup

Open a terminal in the `backend` folder.

```bash
cd backend
```

Create and activate a virtual environment.

### Windows PowerShell

```bash
python -m venv venv
venv\Scripts\activate
```

### macOS/Linux/WSL

```bash
python3 -m venv venv
source venv/bin/activate
```

Install dependencies.

```bash
pip install -r requirements.txt
```

Create your environment file.

```bash
cp .env.example .env
```

For a simple student project, the default SQLite database is enough:

```env
DATABASE_URL=sqlite:///mkulima_chapchap.db
```

Create and seed the database.

```bash
python seed.py
```

Start the Flask backend.

```bash
python app.py
```

The backend should run on:

```txt
http://localhost:5000
```

Test the API in your browser:

```txt
http://localhost:5000/
```

You should see:

```json
{ "message": "Mkulima Chapchap Flask API is running." }
```

---

## 7. Frontend Setup

Open a second terminal in the `frontend` folder.

```bash
cd frontend
```

Install dependencies.

```bash
npm install
```

Create your frontend environment file.

```bash
cp .env.example .env
```

Start React.

```bash
npm run dev
```

The frontend should run on:

```txt
http://localhost:5173
```

---

## 8. Demo Login

After running `python seed.py`, use:

```txt
Email: farmer@example.com
Password: password123
```

---

## 9. How the App Works

1. A user registers or logs in.
2. The backend returns a JWT access token.
3. The frontend saves the token in `localStorage`.
4. When the frontend calls protected routes, it sends the token in this format:

```txt
Authorization: Bearer <token>
```

5. Flask checks the token using `@jwt_required()`.
6. If the token is valid, the user can access animal records, weights, health records, and reminders.

---

## 10. Suggested Student Presentation Script

You can present the project like this:

> My project is called Mkulima Chapchap. It is a simple veterinary farm health management app. Farmers can register, log in, add animals, record weights, record vaccination and deworming schedules, add medical and breeding costs, and see upcoming reminders. The backend is built with Flask, Flask SQLAlchemy, and JWT authentication. The frontend is built with React functional components, React Router, hooks, and Context API. The database has one-to-many relationships between users and animals, and animals and records. It also has a many-to-many relationship where users can favorite many animals.

---

## 11. Notes for Marking

This app is deliberately simple. It avoids unnecessary complexity and focuses on meeting the bootcamp requirements clearly:

- Simple authentication
- Simple CRUD
- Clear protected routes
- Clear model relationships
- Clear project folders
- Clear README
- Commented code

---

## 12. Common Troubleshooting

### Backend says `ModuleNotFoundError`

Make sure your virtual environment is active and you installed requirements:

```bash
pip install -r requirements.txt
```

### Frontend cannot connect to backend

Confirm Flask is running on port `5000` and the frontend `.env` contains:

```env
VITE_API_URL=http://localhost:5000/api
```

### Login fails

Run the seed script again:

```bash
python seed.py
```

Then use:

```txt
farmer@example.com / password123
```

### Database issues

Delete the SQLite database file if needed, then run:

```bash
python seed.py
```

---

## 13. Optional PostgreSQL Setup

SQLite is easiest for bootcamp testing. If your assessor requires PostgreSQL, create a PostgreSQL database and update `backend/.env`:

```env
DATABASE_URL=postgresql://username:password@localhost:5432/mkulima_chapchap
```

Then run:

```bash
python seed.py
```
