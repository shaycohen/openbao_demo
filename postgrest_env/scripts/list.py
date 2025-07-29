import requests

api_url = "http://localhost:8200"

role_id = input('role_id: ')
secret_id = input('secret_id: ')
env = input('env: ')
app = input('app: ')

def login_with_approle(role_id, secret_id):
    response = requests.post(
        f"{api_url}/v1/auth/approle/login",
        json={
            "role_id": role_id,
            "secret_id": secret_id
        }
    )
    response.raise_for_status()
    token = response.json()["auth"]["client_token"]
    return token

if __name__ == "__main__":
    token = login_with_approle(role_id, secret_id)
    print(f"Token: {token}")
    headers = {"X-Vault-Token": token}
    resp = requests.request(
        method="LIST",
        url=f"{api_url}/v1/{env}/{app}",
        headers=headers
    )
    print(resp.text)

