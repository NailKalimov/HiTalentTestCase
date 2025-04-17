def test_create_table(client):
    response = client.post("/tables/", json={
        "name": "Test Table",
        "seats": 2,
        "location": "Test Area"
    })
    assert response.status_code == 200
    assert response.json()["name"] == "Test Table"


def test_get_tables(client):
    response = client.get("/tables/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_delete_table(client):
    create_resp = client.post("/tables/", json={
        "name": "To Delete",
        "seats": 4,
        "location": "Somewhere"
    })
    table_id = create_resp.json()["id"]

    delete_resp = client.delete(f"/tables/{table_id}")
    assert delete_resp.status_code == 200
