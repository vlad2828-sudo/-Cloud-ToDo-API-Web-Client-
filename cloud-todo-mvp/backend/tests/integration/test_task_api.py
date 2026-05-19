def test_health_returns_ok(client) -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_create_task_returns_201(client, api_headers) -> None:
    response = client.post(
        "/api/tasks",
        headers=api_headers,
        json={"title": "Create MVP", "priority": "HIGH"},
    )

    assert response.status_code == 201
    body = response.json()
    assert body["title"] == "Create MVP"
    assert body["status"] == "NEW"
    assert body["priority"] == "HIGH"


def test_list_tasks_with_filters(client, api_headers) -> None:
    client.post("/api/tasks", headers=api_headers, json={"title": "A task", "priority": "HIGH"})
    client.post("/api/tasks", headers=api_headers, json={"title": "B task", "priority": "LOW"})

    response = client.get("/api/tasks?status=NEW&priority=HIGH&limit=10&offset=0")

    assert response.status_code == 200
    body = response.json()
    assert body["total"] == 1
    assert body["items"][0]["priority"] == "HIGH"


def test_patch_task_changes_status(client, api_headers) -> None:
    created = client.post("/api/tasks", headers=api_headers, json={"title": "Patch status"}).json()

    response = client.patch(
        f"/api/tasks/{created['id']}",
        headers=api_headers,
        json={"status": "DONE"},
    )

    assert response.status_code == 200
    assert response.json()["status"] == "DONE"


def test_delete_task_returns_204(client, api_headers) -> None:
    created = client.post("/api/tasks", headers=api_headers, json={"title": "Remove task"}).json()

    response = client.delete(f"/api/tasks/{created['id']}", headers=api_headers)

    assert response.status_code == 204
    assert client.get(f"/api/tasks/{created['id']}").status_code == 404
