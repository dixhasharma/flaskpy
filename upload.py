import pandas as pd
import requests
import json
KEYCLOAK_URL = "http://localhost:8080"
ADMIN_USERNAME = "dixha"
ADMIN_PASSWORD = "dixha"
CLIENT_ID = "qualix"
#  Get Admin Access Token
def get_token(realm, client_id, username, password):
    url = f"{KEYCLOAK_URL}/realms/{realm}/protocol/openid-connect/token"
    payload = {
        "client_id": client_id,
        "username": username,
        "password": password,
        "grant_type": "password",
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    response = requests.post(url, data=payload, headers=headers)
    return response.json().get("access_token")
def get_client_uuid_by_name(token, client_name, realm):
    url = f"{KEYCLOAK_URL}/admin/realms/{realm}/clients"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        clients = response.json()
        for client in clients:
            if client['clientId'] == client_name:
                return client['id']
        print(f"Client '{client_name}' not found.")
        return None
    else:
        print(f"Failed to fetch clients: {response.status_code} - {response.text}")
        return None
def get_client_id_by_name(token, client_name, realm):
    url = f"{KEYCLOAK_URL}/admin/realms/{realm}/clients"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        clients = response.json()
        for client in clients:
            if client['clientId'] == client_name:
                return client['id']
        print(f"Client with name '{client_name}' not found.")
        return None
    else:
        print(f"Failed to fetch clients: {response.status_code} - {response.text}")
        return None
def get_all_realms(token):
    url = f"{KEYCLOAK_URL}/admin/realms"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        realms = response.json()
        realm_names = [realm['realm'] for realm in realms]
        return realm_names
    else:
        print(f"Failed to fetch realms: {response.status_code} - {response.text}")
        return []       
# Update Client Role
def update_client_role(token, CLIENT_UUID, realm, role_name):
    # Step 1: Get role by name
    url_get = f"{KEYCLOAK_URL}/admin/realms/{realm}/clients/{CLIENT_UUID}/roles/{role_name}"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    get_response = requests.get(url_get, headers=headers)
    if get_response.status_code != 200:
        print(f"Failed to fetch role: {get_response.status_code} - {get_response.text}")
        return

    role_data = get_response.json()
    role_id = role_data['id']

    # Step 2: Update role by ID
    url_put = f"{KEYCLOAK_URL}/admin/realms/{realm}/roles-by-id/{role_id}"
    payload = {
        "id": role_id,
        "name": role_name,
        "description": "this is a",
        "attributes": {
            "permissions": ["dixha"],
            "access_scope": ["full"]
        }
    }

    put_response = requests.put(url_put, headers=headers, json=payload)
    if put_response.status_code == 204:
        print("Client role updated successfully.")
    else:
        print(f"Failed to update client role ({put_response.status_code}): {put_response.text}")
# Create Realm Role with Permission Attributes
def create_realm_role(token, role_name, permissions, realm):
    url = f"{KEYCLOAK_URL}/admin/realms/{realm}/roles"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    payload = {
        "name": role_name,
        "attributes": {
            "permissions": permissions
        }
    }
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 201:
        print(f" Created realm role: {role_name}")
    elif response.status_code == 409:
        print(f" Role '{role_name}' already exists.")
    else:
        print(f"Failed to create role '{role_name}': {response.text}")
# Create Client Role
def create_client_role(token, role_name, description, realm, CLIENT_UUID):
    url = f"{KEYCLOAK_URL}/admin/realms/{realm}/clients/{CLIENT_UUID}/roles"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    payload = {
        "name": role_name,
        "description": description
    }
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 201:
        print(f" Client role '{role_name}' created.")
    elif response.status_code == 409:
        print(f" Client role '{role_name}' already exists.")
    else:
        print(f" Failed to create client role '{role_name}': {response.status_code} - {response.text}")
# Fetch Client Role Details
def get_client_role_details(token, CLIENT_UUID, realm, role_name="admin"):
    url = f"{KEYCLOAK_URL}/admin/realms/{realm}/clients/{CLIENT_UUID}/roles/{role_name}"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        print(" Client role details:")
        print(json.dumps(response.json(), indent=4))
    else:
        print(f" Failed to get role details: {response.status_code} - {response.text}")
# get scope id
def get_scope_id_by_name(token, scope_name, realm):
    url = f"{KEYCLOAK_URL}/admin/realms/{realm}/client-scopes"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        scopes = response.json()
        for scope in scopes:
            if scope['name'] == scope_name: 
                return scope['id']
        print(f"Scope with name '{scope_name}' not found.")
        return None
    else:
        print(f"Failed to fetch client scopes: {response.status_code} - {response.text}")
        return None
#assign scope to client
def assign_scope_to_client(token, client_id, scope_id, realm):
    url = f"{KEYCLOAK_URL}/admin/realms/{realm}/clients/{client_id}/default-client-scopes/{scope_id}"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.put(url, headers=headers)
    if response.status_code == 204:
        print(" Scope assigned to client.")
    elif response.status_code == 409:
        print(" Scope already assigned.")
    else:
        print(" Error assigning scope:", response.text)
        # Get roles (Mock or real - for /roles endpoint)
def get_roles():
    # Either fetch from Keycloak or return mock data
    return {
        "roles": ["admin", "user", "viewer"],
        "message": "Roles fetched successfully"
    }

