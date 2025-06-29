import requests

OPENBAO_ADDR = "http://localhost:8200"
ROLE_ID = "a9df48e5-075b-ec2c-d741-b4cec0724c5f"
SECRET_ID = "4a77f601-7f64-d31b-cff5-813ef88d05b9"
#SECRET_ID = "f5b2cf8f-cb47-df93-f95e-bbf26933f0d3"


def login_with_approle(role_id, secret_id):
    r = requests.post(f"{OPENBAO_ADDR}/v1/auth/approle/login", json={
        "role_id": role_id,
        "secret_id": secret_id
    })
    r.raise_for_status()
    return r.json()["auth"]["client_token"]

def read_secret(token):
    headers = {"X-Vault-Token": token}
    r = requests.get(f"{OPENBAO_ADDR}/v1/secret/data/myapp/config", headers=headers)
    r.raise_for_status()
    return r.json()["data"]["data"]

if __name__ == "__main__":
    token = login_with_approle(ROLE_ID, SECRET_ID)
    print("Token:", token, flush=True)
    secret = read_secret(token)
    print("Secret:", secret, flush=True)

