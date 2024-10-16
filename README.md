# Meal Management and Student Recognition System

## Project Overview

This is a Django-based backend system designed for managing meals, student records, and their meal entries with integrated phone verification and face recognition functionalities. The system provides several endpoints to handle CRUD operations for students, meals, and menus, along with recording student meal entries based on meal times.

## Key Features:

 - **Student Management:** CRUD operations for student records including photo upload and phone number validation.
 - **Meal and Menu Management:** Create and manage meals, organize them into menus for different days and meal times.
 - **Meal Entry Tracking:** Track meal entries for students based on meal times (breakfast, lunch, dinner).
 - **Phone Verification:** Send and verify user phone numbers using external services.
 - **Face Recognition:** Face recognition API to verify students.
 - **API Integration:** REST API endpoints for managing the system's features.


## Models

1. Student - This model represents a student in the system.
2. Meal - This model represents a meal.
3. Menu - This model represents the weekly meal plan for different times of the day (Breakfast, Lunch, Dinner).
4. MealEntry - This model represents a record of students consuming a meal at a particular time on a specific date.


## API Endpoints

### Student Endpoints
 - ```GET /students/:``` Get all students.
 - ```POST /students/:``` Create a new student.
 - ```PUT /students/<id>/:``` Update a student.
 - ```DELETE /students/<id>/:``` Delete a student.

### Meal Endpoints
 - ```GET /meals/:``` Get all meals.
 - ```POST /meals/:``` Create a new meal.
 - ```PUT /meals/<id>/:``` Update a meal.
 - ```DELETE /meals/<id>/:``` Delete a meal.

### Menu Endpoints
 - ```GET /menu/:``` Get the weekly menu.
 - ```POST /menu/:``` Create a new menu.
 - ```PUT /menu/<id>/:``` Update a menu.
 - ```DELETE /menu/<id>/:``` Delete a menu.

### Meal Entry Endpoints
 - ```GET /meal-entries/:``` Get all meal entries.
 - ```POST /meal-entries/:``` Create a new meal entry.
 - ```GET /meal-counts/:``` Get the total meal counts for each student.

### Phone Verification Endpoints
 - ```POST /send_phone/:``` Send a verification code to the user’s phone number.
 - ```POST /verify_phone/:``` Verify the sent code for a phone number.

### Face Recognition Endpoints
 - ```POST /check_user/:``` Verify a user’s identity using face recognition.


## Dependencies
 - **Django:** Web framework
 - **phonenumber_field:** For phone number validation
 - **Pillow:** For image handling (student and meal photos)
 - **Django REST Framework:** For building the RESTful APIs
 - **External API Integration:** (For phone verification and face recognition)


## Installation

1. Clone the repository:
    ```sh
    git https://github.com/Fakhrillo/PDP-Kitchen.git
    cd PDP-Kitchen
    ```

2. Create a virtual environment and install dependencies:
    ```sh
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```

3. Apply migrations:
    ```sh
    python manage.py migrate
    ```

4. Run the development server:
    ```sh
    python manage.py runserver
    ```


## Configuration

Make sure to configure your settings in ```settings.py```:

 - Set up your **database** (default is SQLite, but you can use PostgreSQL or MySQL).
 - Set up **MEDIA_URL** and **MEDIA_ROOT** for handling image uploads.
 - Set up the **phone verification API** and **face recognition API** in your environment.


## License
This project is licensed under the MIT License. See the LICENSE file for more details.