from flask import Flask, jsonify, request
import upload
import os

app = Flask(__name__)

# Configuration
KEYCLOAK_CONFIG = {
    "realm": "agnext",
    "client_id": "qualix",
    "client_name": "qualix",
    "client_uuid": "a4bb4a72-4d47-4613-9b1b-5490633f4fdd",
    "username": "dixha",
    "password": "dixha"
}

@app.route("/")
def index():
    return jsonify({
        "message": "Keycloak Flask Integration API",
        "endpoints": [
            "/token", 
            "/run-operations",
            "/client-roles",
            "/realm-roles",
            "/client-scopes"
        ]
    })

@app.route("/token", methods=["POST"])
def get_token():
    data = request.get_json() or {}
    username = data.get("username", KEYCLOAK_CONFIG["username"])
    password = data.get("password", KEYCLOAK_CONFIG["password"])
    realm = data.get("realm", KEYCLOAK_CONFIG["realm"])
    client_id = data.get("client_id", KEYCLOAK_CONFIG["client_id"])
    
    token = upload.get_token(realm, client_id, username, password)
    if not token:
        return jsonify({"error": "Authentication failed"}), 401
    
    return jsonify({"token": token})

@app.route("/run-operations", methods=["POST"])
def run_operations():
    data = request.get_json() or {}
    token = data.get("token")
    if not token:
        return jsonify({"error": "Token is required"}), 400
        
    realm = data.get("realm", KEYCLOAK_CONFIG["realm"])
    client_name = data.get("client_name", KEYCLOAK_CONFIG["client_name"])
    client_uuid = data.get("client_uuid", KEYCLOAK_CONFIG["client_uuid"])

    client_uuid = upload.get_client_uuid_by_name(token, client_name, realm)
    if not client_uuid:
        return jsonify({"error": "Client UUID not found"}), 404

    client_id = upload.get_client_id_by_name(token, client_name, realm)
    if not client_id:
        return jsonify({"error": "Client ID not found"}), 404

    scope_id = upload.get_scope_id_by_name(token, "qemail", realm)
    if not scope_id:
        return jsonify({"error": "Scope ID not found"}), 404

    upload.assign_scope_to_client(token, client_id, scope_id, realm)
    upload.get_client_role_details(token, client_uuid, realm, "hii")
    upload.create_client_role(token, "hii", "This is a test role", realm, client_uuid)
    upload.create_realm_role(token, "ag-admin", ["read", "write"], realm)
    upload.update_client_role(token, client_uuid, realm, "hii")

    return jsonify({
        "message": "Operations completed successfully",
        "client_uuid": client_uuid,
        "client_id": client_id,
        "scope_id": scope_id
    })

@app.route("/client-roles", methods=["POST"])
def client_roles():
    data = request.get_json() or {}
    token = data.get("token")
    if not token:
        return jsonify({"error": "Token is required"}), 400
        
    realm = data.get("realm", KEYCLOAK_CONFIG["realm"])
    client_uuid = data.get("client_uuid", KEYCLOAK_CONFIG["client_uuid"])
    role_name = data.get("role_name")
    description = data.get("description", "Role created via API")
    
    if not role_name:
        return jsonify({"error": "role_name is required"}), 400
        
    upload.create_client_role(token, role_name, description, realm, client_uuid)
    return jsonify({"message": f"Client role '{role_name}' created"})

@app.route("/realm-roles", methods=["POST"])
def realm_roles():
    data = request.get_json() or {}
    token = data.get("token")
    if not token:
        return jsonify({"error": "Token is required"}), 400
        
    realm = data.get("realm", KEYCLOAK_CONFIG["realm"])
    role_name = data.get("role_name")
    permissions = data.get("permissions", [])
    
    if not role_name:
        return jsonify({"error": "role_name is required"}), 400
        
    upload.create_realm_role(token, role_name, permissions, realm)
    return jsonify({"message": f"Realm role '{role_name}' created"})

@app.route("/client-scopes", methods=["POST"])
def client_scopes():
    data = request.get_json() or {}
    token = data.get("token")
    if not token:
        return jsonify({"error": "Token is required"}), 400
        
    realm = data.get("realm", KEYCLOAK_CONFIG["realm"])
    client_id = data.get("client_id", KEYCLOAK_CONFIG["client_id"])
    scope_name = data.get("scope_name")
    
    if not scope_name:
        return jsonify({"error": "scope_name is required"}), 400
        
    scope_id = upload.get_scope_id_by_name(token, scope_name, realm)
    if not scope_id:
        return jsonify({"error": f"Scope with name '{scope_name}' not found"}), 404
        
    upload.assign_scope_to_client(token, client_id, scope_id, realm)
    return jsonify({"message": f"Scope '{scope_name}' assigned to client"})

if __name__ == "__main__":
    app.run(debug=True, port=5001)