def test_no_api_key(client):
    response = client.get("/api/v1/users/all")
    assert response.status_code == 403
    assert response.json() == {"detail": "Unauthorized"}


def test_invalid_api_key(client):
    headers = {"X-API-Key": "invalid_key"}
    response = client.get("/api/v1/users/all", headers=headers)
    assert response.status_code == 403
    assert response.json() == {"detail": "Unauthorized"}


def test_valid_admin_api_key(client, admin_headers):
    response = client.get("/api/v1/users/all", headers=admin_headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)  # Assuming the response is a list of users


def test_team_only_access(client, new_team_and_user, admin_headers):
    team1, user1 = new_team_and_user("Test Team 1", "user1@test.com")
    team2, _ = new_team_and_user("Test Team 2", "user2@test.com")
    headers = {"X-API-Key": user1["api_key"]}
    response = client.get(f"/api/v1/users/{team1['id']}/all", headers=headers)
    assert response.status_code == 200
    denied_response = client.get(f"/api/v1/users/{team2['id']}/all", headers=headers)
    assert denied_response.status_code == 403
