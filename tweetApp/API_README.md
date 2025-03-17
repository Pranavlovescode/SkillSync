# SkillSync API Documentation

This document provides information about the REST API endpoints available in the SkillSync application.

## Authentication

The API uses token-based authentication. To authenticate, you need to obtain a token by sending a POST request to the login endpoint.

### Obtaining a Token

**Endpoint:** `/api/login/`

**Method:** `POST`

**Request Body:**
```json
{
  "username_or_email": "your_username_or_email",
  "password": "your_password"
}
```

**Response:**
```json
{
  "token": "your_auth_token",
  "user": {
    "user_id": "uuid",
    "first_name": "John",
    "last_name": "Doe",
    "email": "john@example.com",
    "username": "johndoe",
    "phone_number": 1234567890,
    "dob": "1990-01-01",
    "profile_photo": "url_to_photo",
    "gender": "M",
    "bio": "About me",
    "createdAt": "2023-01-01T00:00:00Z"
  }
}
```

### Using the Token

Include the token in the Authorization header of your requests:

```
Authorization: Token your_auth_token
```

## User Endpoints

### Register a New User

**Endpoint:** `/api/signup/`

**Method:** `POST`

**Request Body:**
```json
{
  "first_name": "John",
  "last_name": "Doe",
  "email": "john@example.com",
  "username": "johndoe",
  "password": "secure_password"
}
```

### Get Current User Profile

**Endpoint:** `/skill/api/users/me/`

**Method:** `GET`

**Authentication:** Required

### Update Current User Profile

**Endpoint:** `/skill/api/users/update_me/`

**Method:** `PUT` or `PATCH`

**Authentication:** Required

**Request Body:** (include only fields you want to update)
```json
{
  "first_name": "Updated Name",
  "bio": "Updated bio"
}
```

### List All Users

**Endpoint:** `/skill/api/users/`

**Method:** `GET`

**Authentication:** Required

**Query Parameters:**
- `username`: Filter by username

### Get User Details

**Endpoint:** `/skill/api/users/{user_id}/`

**Method:** `GET`

**Authentication:** Required

## Skill Post Endpoints

### List All Posts

**Endpoint:** `/skill/api/posts/`

**Method:** `GET`

**Authentication:** Required

**Query Parameters:**
- `tag`: Filter by tag
- `user_id`: Filter by user ID

### Create a New Post

**Endpoint:** `/skill/api/posts/`

**Method:** `POST`

**Authentication:** Required

**Request Body:**
```json
{
  "post_name": "Post Title",
  "post_description": "Post content",
  "post_tags": "tag1,tag2",
  "post_media": "file_upload"
}
```

### Get Post Details

**Endpoint:** `/skill/api/posts/{post_id}/`

**Method:** `GET`

**Authentication:** Required

### Update a Post

**Endpoint:** `/skill/api/posts/{post_id}/`

**Method:** `PUT` or `PATCH`

**Authentication:** Required (only post owner)

### Delete a Post

**Endpoint:** `/skill/api/posts/{post_id}/`

**Method:** `DELETE`

**Authentication:** Required (only post owner)

### Like a Post

**Endpoint:** `/skill/api/posts/{post_id}/like/`

**Method:** `POST`

**Authentication:** Required

### Get Current User's Posts

**Endpoint:** `/skill/api/posts/my_posts/`

**Method:** `GET`

**Authentication:** Required

## Logout

**Endpoint:** `/api/logout/`

**Method:** `POST`

**Authentication:** Required

## Error Responses

The API returns appropriate HTTP status codes:

- `200 OK`: Request succeeded
- `201 Created`: Resource created successfully
- `400 Bad Request`: Invalid request data
- `401 Unauthorized`: Authentication required or failed
- `403 Forbidden`: Permission denied
- `404 Not Found`: Resource not found
- `500 Internal Server Error`: Server error

Error responses include a JSON object with an error message:

```json
{
  "error": "Error message"
}
``` 