# Trekking Management Application

## Problem Statement

The Trekking Management Application is a web-based system designed to manage
trekking activities, users, trek staff, bookings, and trek availability.

The application provides separate functionality for Admin, Trek Staff, and
Users. It helps administrators manage treks and users, staff manage assigned
treks and trekkers, and users browse and book available treks.

## Features

### Admin
- Admin dashboard with trek, user, staff, and booking statistics.
- Create and manage treks.
- Assign staff to treks.
- Approve staff registrations.
- Manage users and staff.
- View bookings and trek history.
- Search users, staff, and treks.

### Trek Staff
- Staff dashboard with assigned trek statistics.
- View assigned treks.
- Update available trek slots.
- Update trek status.
- View trekkers registered for a trek.
- Manage staff profile.

### User
- User dashboard with available treks.
- Search and filter treks.
- View trek details.
- Book treks.
- View bookings.
- Manage user profile.

## Technologies Used

- Python
- Flask
- SQLAlchemy
- SQLite
- Jinja2
- Bootstrap 5
- Flask-Login
- HTML5
- CSS3

## Project Structure

```text
trekking-management/
│
├── app.py
├── create_app.py
├── config.py
├── constants.py
├── extensions.py
├── init_db.py
├── create_admin.py
├── requirements.txt
│
├── models/
│
├── routes/
│
├── templates/
│
├── static/
│
├── instance/
│
└── project_report.pdf
