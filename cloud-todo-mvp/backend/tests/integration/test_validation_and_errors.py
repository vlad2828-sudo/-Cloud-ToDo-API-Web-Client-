def test_create_task_without_api_key_returns_401(client) -> None:
    response = client.post("/api/tasks", json={"title": "Secure task"})

    assert response.status_code == 401
    assert response.json()["code"] == "UNAUTHORIZED"


def test_create_task_with_invalid_title_returns_400(client, api_headers) -> None:
    response = client.post("/api/tasks", headers=api_headers, json={"title": "ab"})

    assert response.status_code == 400
    body = response.json()
    assert body["code"] == "VALIDATION_ERROR"
    assert body["details"]


def test_get_missing_task_returns_404(client) -> None:
    response = client.get("/api/tasks/not-found")

    assert response.status_code == 404
    assert response.json()["code"] == "TASK_NOT_FOUND"


def test_patch_without_payload_returns_400(client, api_headers) -> None:
    created = client.post("/api/tasks", headers=api_headers, json={"title": "Patch empty"}).json()

    response = client.patch(f"/api/tasks/{created['id']}", headers=api_headers, json={})

    assert response.status_code == 400
    assert response.json()["code"] == "VALIDATION_ERROR"
