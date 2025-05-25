def test_upload_image(client, new_team_and_user):
    team, user = new_team_and_user("Test Team for Image Upload", "user@test.com")
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
    assert response.status_code == 201

    response = client.get(
        f"/api/v1/team/{team_id}/image/all",
        headers=headers,
    )
    assert response.status_code == 200
    all_images = response.json()
    assert "images" in all_images
    images = all_images.get("images")
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
    assert response.status_code == 201

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
    response_data = response.json()
    assert "images" in response_data
    assert len(response_data["images"]) == 1
