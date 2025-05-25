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

def test_upload_empty_file(client, admin_headers, new_team):
    team = new_team("Test Team for Empty File Upload")
    team_id = team["id"]

    response = client.post(
        f"/api/v1/team/{team_id}/user",
        headers=admin_headers,
    )
    assert response.status_code == 400
    
    response = client.post(
        f"/api/v1/team/{team_id}/image",
        files={"file": ("empty_file.jpg", b"", "image/jpeg")},
        headers=admin_headers,
    )
    assert response.status_code == 400
    