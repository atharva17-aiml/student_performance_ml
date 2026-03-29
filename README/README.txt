# Student Performance ML System

## Features

* User authentication (Register / Login / Logout)
* Profile management
* Student performance prediction using ML model
* Input validation for prediction data
* Prediction history tracking
* Dashboard with user statistics
* Admin panel (view users & predictions)
* CSV export for predictions
* Data visualization (analysis page)
* MySQL database integration

---

## Setup

Install dependencies:

```
pip install -r requirements.txt
```

Create `.env` file:

```
DB_HOST=localhost
DB_USER=root
DB_PASS=yourpassword
DB_NAME=yourdatabase
SECRET_KEY=yoursecretkey
```

Initialize database:

```
python database.py
```

Train ML model:

```
python train_model.py
```

Run application:

```
python app.py
```

---

## Usage

1. Register a new user
2. Login to the system
3. Enter student details:

   * Study Time
   * Failures
   * Absences
   * Health
   * G1, G2 marks
4. Click **Predict**
5. View results on dashboard

---

## Prediction Model

* Algorithms used:

  * Linear Regression
  * Random Forest (best model selected automatically)

* Features:

  * studytime
  * failures
  * absences
  * health
  * G1, G2

* Output:

  * Predicted final score (G3)

---

## Input Validation

* Study Time: 1–5
* Failures: 0–3
* Absences: 0–30
* Health: 1–5
* G1, G2: 0–20

---

## Assumptions

* Input values are numeric
* Dataset is available in `/dataset/student_data.csv`
* MySQL server is running
* Environment variables are configured

---

## Notes

* Predictions are stored in database
* Admin can view all users and predictions
* CSV export available for admin
* Sessions expire after a fixed duration

---

## Tech Stack

* Python
* Flask
* MySQL
* Scikit-learn
* Pandas
* NumPy
* Matplotlib / Seaborn
* Gunicorn

---

## Verification

* Dashboard statistics
* Prediction history page
* Admin panel data
* CSV export

---

## Deployment

* Configured for deployment using:

  * Gunicorn
  * Render (via `render.yaml`)

---

## Future Improvements

* Add REST API endpoints
* Improve UI (React / modern frontend)
* Add advanced ML models
* Real-time analytics dashboard
* Role-based access enhancements

---
