from fastapi import status
from httpx import AsyncClient


async def test_create_post_success(client: AsyncClient, access_token: str):
    # Given
    headers = {"Authorization": f"Bearer {access_token}"}
    data = {
        "title": "Test Post", 
        "content": "This is a test post.", 
        "published_at": "2024-01-01T00:00:00Z", 
        "published": True
    }

    # When
    response = await client.post("/posts/", json=data, headers=headers)

    # Then
    content = response.json()

    assert response.status_code == status.HTTP_201_CREATED
    assert content["id"] is not None


async def test_create_post_invalid_payload_fail(client: AsyncClient, access_token: str):
    # Given
    headers = {"Authorization": f"Bearer {access_token}"}
    data = {
        "content": "This post has no title.",
        "published_at": "2025-03-03T10:00:00Z",
        "published": True
    }

    # When
    response = await client.post("/posts/", json=data, headers=headers)

    # Then
    content = response.json()

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
    assert content["detail"][0]["loc"] == ["body", "title"]


async def test_create_post_not_authenticated_fail(client: AsyncClient):
    # Given
    data = {
        "content": "This post should not be created.",
        "published_at": "2024-05-05T12:00:00Z",
        "published": True
    }

    # When
    response = await client.post("/posts/", json=data)

    # Then
    content = response.json()

    assert response.status_code == status.HTTP_401_UNAUTHORIZED