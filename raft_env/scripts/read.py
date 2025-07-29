import requests

api_url = "http://localhost:8200"
role_id = input('role_id: ')
secret_id = input('secret_id: ')
env = input('env: ')
app = input('app: ')

def login_with_approle(role_id, secret_id):
    r = requests.post(f"{api_url}/v1/auth/approle/login", json={
        "role_id": role_id,
        "secret_id": secret_id
    })
    r.raise_for_status()
    return r.json()["auth"]["client_token"]

def read_secret(token):
    headers = {"X-Vault-Token": token}
    r = requests.get(f"{api_url}/v1/{env}/{app}/secret_ini", headers=headers)
    r.raise_for_status()
    return r.json()

if __name__ == "__main__":
    token = login_with_approle(role_id, secret_id)
    print("Token:", token, flush=True)
    secret = read_secret(token)
    print("Secret:", secret, flush=True)

