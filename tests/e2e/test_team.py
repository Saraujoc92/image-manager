def test_delete_team(client, admin_headers, new_team_and_user):
    team, user = new_team_and_user("Test Team for Deletion")
    team_id = team["id"]
    # Test the api key of the user
    assert "api_key" in user
    team_users = client.get(
        f"/api/v1/team/{team_id}/user/all", headers={"X-API-Key": user["api_key"]}
    )
    assert team_users.status_code == 200

    # Delete the team
    response = client.delete(f"/api/v1/team/{team_id}", headers=admin_headers)
    assert response.status_code == 204

    # Verify the team is deleted
    response = client.get(f"/api/v1/team/{team_id}/user/all", headers=admin_headers)
    assert response.status_code == 404

    # Verify the user is deactivated
    user_response = client.get(
        f"/api/v1/team/{team_id}/user/all", headers={"X-API-Key": user["api_key"]}
    )
    assert (
        user_response.status_code == 403
    )  # User should not be able to access after deletion
