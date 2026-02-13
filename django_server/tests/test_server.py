from django.urls import reverse

HEALTHZ_URL = reverse('healthz')
ROOT_URL = reverse('admin-root-redirect')

def test_server_health_check(client):
    response = client.get(HEALTHZ_URL)

    assert response.status_code == 200, (
        f"{HEALTHZ_URL} check failed: {response.status_code}"
    )
    assert response.json() == {"status": "ok"}, (
        f"Unexpected {HEALTHZ_URL} response: {response.json()}"
    )

def test_root_admin_route(client):
    response = client.get(ROOT_URL)

    assert response.status_code == 302, (
        f"{ROOT_URL} check failed: {response.status_code}"
    )
    assert response.url == "/admin/", (
        f"{ROOT_URL} redirected to unexpected URL: {response.url}"
    )
