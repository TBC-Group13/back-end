# Stay Connected 

A platform where developers can ask questions and get clear, helpful answers quickly and easily.

---

## Features
- **JWT Authentication**: Secure endpoints with user authentication.
- **Profile Management**:
  - View user profile details.
  - Upload/update/delete a profile photo.
- **Post questions**
- **Answer questions**
- **Like/Dislike question**
- **Mark answer as correct(only the question author does this)**
- **search question by keyword(words included in title and description), via tags or via both**
---

## Requirements
- Python 3.8+
- Django 4.x
- Django REST Framework (DRF)
- Simple JWT

---

## Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/MariamKhoKh/Stay-Connected.git
cd stayconnected
```

### 2. Install Dependencies
Create a virtual environment and install the required packages:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Apply Migrations
```bash
python manage.py migrate
```

### 5. Run the Development Server
```bash
python manage.py runserver
```

The API will be available at `http://127.0.0.1:8000/`.

---


## API Endpoints
1. User Registration URL:
``` bash
       http://127.0.0.1:8000/api/profile/
```
**Method**: POST

**Payload**:
```
{
    "username": "testuser",
    "email": "testuser@example.com",
    "password": "securepassword123!"
}
```

2. User Login URL: 
``` bash
 http://127.0.0.1:8000/api/login/
 ```
**Method**: POST

**Payload**:
```
{
    "username": "testuser",
    "password": "securepassword123"
}
```
**Response**: A token will be provided upon successful login. 
Use this token (include in the header) for all subsequent requests.

3. Create a Tag URL: 
```bash
http://127.0.0.1:8000/api/tags/
```
**Method**: POST

**Headers**:
```
Authorization: Bearer <Paste access token here without ""-s>
```
**Payload**:
```
{
    "name": "Django"
}
```

4. List Tags URL: 
```bash
http://127.0.0.1:8000/api/tags/
```
**Method**: GET

**Headers**:
```
Authorization: Bearer <Paste access token here without ""-s>
```

5. Create a Question URL:
```bash
http://127.0.0.1:8000/api/questions/
```
**Method**: POST

**Headers**:
```
Authorization: Bearer <Paste access token without ""-s>
```
**Payload**:
```
{
    "title": "How to implement authentication in Django?",
    "content": "What are the best practices for adding authentication in a Django project?",
    "tags": ["Django", "Authentication"]
}
```
6. List Questions URL: 
```
http://127.0.0.1:8000/api/questions/
```
**Method**: GET

**Headers**:
```
Authorization: Bearer <Paste access token without ""-s>
```

7. Answer a Question URL: 
```bash
http://127.0.0.1:8000/api/questions/<QUESTION_ID>/answers/
```
**Method**: POST

**Headers**:
```
Authorization: Bearer <Paste access token without ""-s>
```
**Payload**:
```

{
    "content": "You can use Django Rest Framework's built-in TokenAuthentication or JWT for API authentication."
}

```
8. Like an Answer URL: 
```bash
http://127.0.0.1:8000/api/answers/<ANSWER_ID>/like/
```
**Method**: POST

**Headers**:
```
Authorization: Bearer <Paste access token without ""-s>
```
9. Dislike an Answer URL:
```bash
http://127.0.0.1:8000/api/answers/<ANSWER_ID>/dislike/
```
**Method**: POST

**Headers**:
```
Authorization: Bearer <Paste access token without ""-s>
```

10. Mark an Answer as Correct URL: 
```bash
http://127.0.0.1:8000/api/answers/<ANSWER_ID>/mark-correct/
```
**Method**: POST

**Headers**:
```
Authorization: Bearer <Paste access token without ""-s>
```

11. User reputation URL:
```bash
http://127.0.0.1:8000/api/users/< USER_ID>/reputation/
```

**Method**: GET

**Headers**:
```
Authorization: Bearer <Paste access token without ""-s>
```

12. Search URL:
**example search by key word, tag and both**
```bash
http://127.0.0.1:8000/api/questions/search/?query=python
http://127.0.0.1:8000/api/questions/search/?tag=django
http://127.0.0.1:8000/api/questions/search/?query=python&tag=django
```
**Method**: GET

**Headers**:
```
Authorization: Bearer <Paste access token without ""-s>
```

13. Token Refresh
```bash
http://127.0.0.1:8000/api/token/refresh
```
**Method**: POST

**Purpose**: Provides a new access token using a refresh token.

**Request Body**:
```
{
  "refresh": "<REFRESH_TOKEN>"
}
```

**Response**
```
{
  "access": "<NEW_ACCESS_TOKEN>"
}
```

14. User profile URL:
```bash
http://127.0.0.1:8000/api/profile/
```

**Method**: GET

**Headers**:
```
Authorization: Bearer <Paste access token without ""-s>
```

15. Upload/Update profile photo URL:
```bash
http://127.0.0.1:8000/api/profile/
```

**Method**: POST

**Headers**:
```
Authorization: Bearer <Paste access token without ""-s>
```

**Request Body (form-data):**

**Key**: profile_photo ```(File)```

**Value**: Upload an image file (.jpg, .jpeg, .png).


# General Notes:
**Ensure the server is running and accessible when making requests.**

**JWT tokens must be included in the Authorization header for authenticated endpoints.**

**Media files (e.g., profile photos) are stored under the MEDIA_ROOT directory and served via the /media/ URL.**




