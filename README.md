# BU-Classroom-Reservation-App

A Django web app for Boston University students to browse campus classrooms and reserve them for club meetings, events, and study sessions. Authentication is restricted to `@bu.edu` Google accounts via django-allauth.

**Live demo:** [cs-webapps.bu.edu/nnedi/project/](https://cs-webapps.bu.edu/nnedi/project/)

## Features

- Google OAuth login limited to BU emails (`@bu.edu`)
- Browse buildings with campus side, address, and opening/closing hours
- Browse rooms with capacity, projector availability, and microphone inventory
- Filter rooms by building, minimum mic count, projector, and building hours
- Create reservations (login required) with start and end times
- Booking rules: start before end, within building hours, max 3 hours, no overlapping bookings for the same room
- View upcoming bookings and filter by building, room number, and date

## Tech Stack

- **Backend:** Django, Python
- **Auth:** django-allauth (Google OAuth), custom social-account adapter
- **Database:** SQLite
- **Frontend:** Django templates + CSS

## Getting Started

This app lives inside the `cs412` Django project. From the repository root:

### 1. Install dependencies

```bash
pipenv install
pipenv shell
```

If you are not using Pipenv:

```bash
pip install django django-allauth
```

Google OAuth also needs a Google Cloud OAuth client configured in Django admin (`Social applications`) with authorized redirect URI:

```
http://127.0.0.1:8000/accounts/google/login/callback/
```

### 2. Apply migrations

```bash
python manage.py migrate
```

### 3. Run the development server

```bash
python manage.py runserver
```

Then open [http://127.0.0.1:8000/project/](http://127.0.0.1:8000/project/).

## Project Structure

```
project/
├── models.py          # Building, Room, Microphone, Booking
├── views.py           # Home, lists, filters, create booking
├── urls.py            # App routes
├── forms.py           # Booking form + BU-email signup validation
├── adapters.py        # django-allauth adapter (BU Google accounts only)
├── admin.py           # Django admin registration
├── static/project/    # CSS
└── templates/
    ├── project/       # App pages
    ├── account/       # Login / logout / signup
    └── socialaccount/ # Google OAuth templates
```

## Main Web Routes

| Path | Description |
|------|-------------|
| `/project/` | Home |
| `/project/buildings/` | List buildings |
| `/project/rooms/` | List / filter rooms |
| `/project/bookings/` | List / filter upcoming bookings |
| `/project/reserve/` | Create a reservation (login required) |
| `/accounts/login/` | Google OAuth login (django-allauth) |
| `/accounts/logout/` | Logout |

## Models

- **Building** — abbreviation, address, campus side, room count, opening and closing times
- **Room** — belongs to a building; capacity, room number, projector, mic count, many-to-many microphones
- **Microphone** — type (lavalier / handheld / shotgun), brand, model, wireless, name
- **Booking** — user, room, building, start and end times, with overlap and hour validation on save

## Booking Validation

A booking is rejected if any of these fail:

- End time is not after start time
- Start is before the building opens, or end is after it closes
- Duration is longer than 3 hours
- Another booking already occupies that room for an overlapping interval

## Author

Niyoo Nedi (`nnedi@bu.edu`)
