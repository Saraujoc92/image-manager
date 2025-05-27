def test_upload_image(client, new_team_and_user):
    team, user = new_team_and_user("Test Team for Image Upload")
    team_id = team["id"]
    headers = {"X-API-Key": user["api_key"]}
    image_data = {
        "name": "test_image.jpg",
        "description": "A test image for upload",
        "file": ("test_image.jpg", b"fake_image_data", "image/jpeg"),
    }
    response = client.post(
        f"/api/v1/team/{team_id}/image",
        files=image_data,
        headers=headers,
    )
    assert response.status_code == 200

    response = client.get(
        f"/api/v1/team/{team_id}/image/all",
        headers=headers,
    )
    assert response.status_code == 200
    images = response.json() 
    assert isinstance(images, list)
    assert len(images) == 1
    image = images[0]
    assert "image_path" in image
    assert "uploaded_by" in image
    assert image["uploaded_by"] == user["id"]
    assert "url" in image


def test_image_team_only_access(client, new_team_and_user):
    team, user = new_team_and_user("Test Team for Image Access", "owner@mail.com")
    team_id = team["id"]
    headers = {"X-API-Key": user["api_key"]}
    image_data = {
        "name": "team_image.jpg",
        "description": "A team image for access test",
        "file": ("team_image.jpg", b"fake_image_data", "image/jpeg"),
    }
    response = client.post(
        f"/api/v1/team/{team_id}/image",
        files=image_data,
        headers=headers,
    )
    assert response.status_code == 200

    _, other_user = new_team_and_user(
        "Other Team With no Image Access", "impostor@mail.com"
    )
    other_user_headers = {"X-API-Key": other_user["api_key"]}
    response = client.get(
        f"/api/v1/team/{team_id}/image/all",
        headers=other_user_headers,
    )
    assert response.status_code == 403

    response = client.get(
        f"/api/v1/team/{team_id}/image/all",
        headers=headers,
    )
    assert response.status_code == 200
    images = response.json()
    assert len(images) == 1

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

def test_upload_invalid_image_type(client, new_team_and_user):
    team, user = new_team_and_user("Test Team for Invalid Image Type")
    team_id = team["id"]
    headers = {"X-API-Key": user["api_key"]}
    image_data = {
        "name": "invalid_image.txt",
        "description": "An invalid image type for upload",
        "file": ("invalid_image.txt", b"fake_text_data", "text/plain"),
    }
    response = client.post(
        f"/api/v1/team/{team_id}/image",
        files=image_data,
        headers=headers,
    )
    assert response.status_code == 400
                                   