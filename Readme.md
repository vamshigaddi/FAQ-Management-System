## FAQ Management System
A Django-based application to manage frequently asked questions (FAQs) with multi-language support and API endpoints for easy retrieval and creation of FAQs.

### Table of Contents

#### 1. Project Overview
#### 2. Features
#### 3. TechStack
#### 4. Installation 
#### 5. Usage
#### 6. API Endpoints
#### 7. Testing

## Project Overview
This project allows users to manage FAQs with support for multiple languages (Hindi, Bengali, etc.). FAQs can be retrieved via API, with fallback support for missing translations, and caching for performance.
## Features
- **Multilingual FAQ Management:** Store and retrieve FAQs in multiple languages with automated translations.
- **WYSIWYG Editor Integration:** Format FAQ answers with django-ckeditor.
- **REST API**: Efficiently manage FAQs with support for language-specific queries.
- **Caching:** Boost performance with Redis-based caching for translations.
- **Admin Interface:** User-friendly admin panel for managing FAQs.
- **Unit Testing:** Comprehensive tests to ensure reliability.

## Tech Stack
- **Backend:** Django, Django Rest Framework
- **Database:** PostgreSQL
- **Cache:** Redis
- **Translation:** googletrans Library
- **Editor:** django-ckeditor

## Installation
To get started with the project, follow the steps below:
- **Download Docker Desktop**
- **Redis**
### 1. Clone the repository:
```
git clone https://github.com/vamshigaddi/FAQ-Management-System.git
cd FAQ-Management-System.git
```
### 2. Create ```.env``` file
Inside the project directory, create a .env file with credentials or simply you can use existing one
```
POSTGRES_DB=faq_db
POSTGRES_USER=faq_user
POSTGRES_PASSWORD=faq_password
POSTGRES_HOST=db
POSTGRES_PORT=5432
```
### 3. Start the Docker Containers
Run the following command to build and start the application
```
docker-compose up --build
```
- For Running Migrations inside a Container
- Open other terminal while docker compose is running and execute the following command
```
docker-compose exec web python manage.py migrate
 ```
### 4. Create the Django superuser:
While the containers are up and running, open the other terminal and create a superuser to access the Django admin interface:
```
docker-compose exec web python manage.py createsuperuser
```
- It will open shell in the terminal and ask for username and password. Enter the password carefully, it doesnot shows password.
### 5. Access the Admin Interface:
Go to ``` http://127.0.0.1:8000/admin``` and log in with the superuser credentials.
### 6. Access the API:
The API is available at ``` http://127.0.0.1:8000/api/faqs/ ```
## Usage
The application allows CRUD operations on FAQs. Use the admin interface or the provided API to manage FAQ entries.

## API Endpoints
- The FAQ API allows you to create and retrieve FAQs.
#### Create FAQ
- Endpoint: POST: ```http://127.0.0.1:8000/api/faqs/```
#### Request Body:
```
{
  "question": "What is mango?",
  "answer": "<p>Mango is a fruit</p>",
  "question_hi": "आम क्या है?",
  "question_bn": "আম কি?"
}
```
#### Response:
```
{
    "id": 7,
    "question": "What is mango?",
    "translated_question": "What is mango?",
    "answer": "<p>Mango is a fruit</p>"
}
```
#### Retrieve FAQ
- **Endpoint:** GET /api/faqs/?lang=<language_code
- **Example:**  GET : ```http://127.0.0.1:8000/api/faqs/?lang=hi``` For Hindi Language, change `hi` to `bn` for Bengali Language
#### Response:
```
    {
        "id": 1,
        "question": "What is the capital of India?",
        "translated_question": "भारत की राजधानी क्या है?",
        "answer": "<p>New Delhi.</p>"
    },
```
#### Update FAQ
- **Endpoint:** PUT ``` http://127.0.0.1:8000/api/faqs/id/ ```
- **Example:** PUT ```http://127.0.0.1:8000/api/faqs/2/```
#### Request Body:
````
{
  "question": "What is the capital of India?",
  "answer": "<p>Delhi India.</p>",
  "question_hi": "भारत की राजधानी क्या है?",
  "question_bn": "ভারতের রাজধানী কি?"
}
````
#### Response Body:
```
{
    "id": 2,
    "question": "What is the capital of India?",
    "translated_question": "What is the capital of India?",
    "answer": "<p>Delhi India.</p>"
}
```
#### Delete FAQ
- **Endpoint:** DELETE ``` http://127.0.0.1:8000/api/faqs/id/ ```
- **Example:** DELETE ```http://127.0.0.1:8000/api/faqs/2/```

## Unit Testing
- To run the tests,first you have to run this command in terminal
- ```set DJANGO_SETTINGS_MODULE=faq_project.settings```

- **API TESTING**
- Run this command for testing the API's
- ```   pytest faqs/tests/test_api.py  ```
- **MODEL TESTING**
- Run this command for testing model methods
- ```  pytest faqs/tests/test_models.py  ```
