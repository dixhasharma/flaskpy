# Keycloak Flask API

A Python Flask API for interacting with Keycloak authentication server. This API is specifically designed to be used with Postman or other API clients.

## Prerequisites

- Python 3.6+
- Flask
- Keycloak server running on http://localhost:8080

## Setup

1. Clone this repository
2. Run the Flask application:

```
python main.py
```

The API will be available at: http://localhost:5000

## API Endpoints

### Get a Token

```
POST /token
```

**Request Body:**
```json
{
  "username": "dixha",
  "password": "dixha",
  "realm": "agnext",
  "client_id": "qualix"
}
```

**Response:**
```json
{
  "token": "eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiw..."
}
```

### Run Operations

```
POST /run-operations
```

**Request Body:**
```json
{
  "token": "YOUR_TOKEN_HERE",
  "realm": "agnext",
  "client_name": "qualix"
}
```

### Create Client Role

```
POST /client-roles
```

**Request Body:**
```json
{
  "token": "YOUR_TOKEN_HERE",
  "role_name": "custom-role",
  "description": "Custom role description",
  "realm": "agnext",
  "client_uuid": "a4bb4a72-4d47-4613-9b1b-5490633f4fdd"
}
```

### Create Realm Role

```
POST /realm-roles
```

**Request Body:**
```json
{
  "token": "YOUR_TOKEN_HERE",
  "role_name": "custom-realm-role",
  "permissions": ["read", "write", "delete"],
  "realm": "agnext"
}
```

### Assign Client Scope

```
POST /client-scopes
```

**Request Body:**
```json
{
  "token": "YOUR_TOKEN_HERE",
  "scope_name": "qemail",
  "realm": "agnext",
  "client_id": "qualix"
}
```

## Default Configuration

The API uses the following default configuration if not specified in the requests:

```
{
  "realm": "agnext",
  "client_id": "qualix",
  "client_name": "qualix",
  "client_uuid": "a4bb4a72-4d47-4613-9b1b-5490633f4fdd",
  "username": "dixha",
  "password": "dixha"
}
```

## Postman Collection

You can import the Postman collection JSON file to easily test all endpoints. 