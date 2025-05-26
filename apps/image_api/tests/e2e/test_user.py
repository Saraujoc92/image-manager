def test_create_user(client, admin_headers, new_team):
    team = new_team("Test Team for User Creation")
    team_id = team["id"]
    response = client.post(
        f"/api/v1/team/{team_id}/user",
        json={"email": "user1@test.com", "name": "Test User"},
        headers=admin_headers,
    )
    assert response.status_code == 201
    user = response.json()
    assert "id" in user
    assert "api_key" in user


def test_fail_create_user_duplicate_email(client, admin_headers, new_team):
    team = new_team("Test Team for Duplicate User Creation")
    team_id = team["id"]

    email = "duplicate_mail@test.com"
    # Create the first user
    response = client.post(
        f"/api/v1/team/{team_id}/user",
        json={"email": email, "name": "First User"},
        headers=admin_headers,
    )
    assert response.status_code == 201

    response = client.post(
        f"/api/v1/team/{team_id}/user",
        json={"email": email, "name": "Second User"},
        headers=admin_headers,
    )
    assert response.status_code == 400


def test_fail_bad_request_create_user(client, admin_headers, new_team):
    team = new_team("Test Team for Bad Request User Creation")
    team_id = team["id"]

    # Missing email
    response = client.post(
        f"/api/v1/team/{team_id}/user",
        json={"name": "Test User"},
        headers=admin_headers,
    )
    assert response.status_code == 400

def test_rotate_user_credentials(client, new_team_and_user):
    team, user = new_team_and_user("Test Team for User Credential Rotation")
    team_id = team["id"]
    user_id = user["id"]
    headers = {"X-API-Key": user["api_key"]}
    
    response = client.post(
        f"/api/v1/user/{user_id}/credentials/rotate",
        headers=headers,
    )
    assert response.status_code == 200
    data = response.json()
    assert "api_key" in data
    new_api_key = data["api_key"]
    assert new_api_key != user["api_key"]
    
    # Verify the old API key is no longer valid
    response = client.get(
        f"/api/v1/team/{team_id}/user/all",
        headers=headers,
    )
    assert response.status_code == 403
    
    response = client.get(
        f"/api/v1/team/{team_id}/user/all",
        headers={"X-API-Key": new_api_key},
    )
    assert response.status_code == 200
                 
    