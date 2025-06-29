import time
import requests

OPENBAO_ADDR = "http://localhost:8200"
ROOT_TOKEN = "s.OTnbebbRyAZyvJh2Kqqp2T9e"

HEADERS = {"X-Vault-Token": ROOT_TOKEN}

def wait_for_openbao():
    print("Waiting for OpenBao to be ready...")
    for _ in range(30):
        try:
            r = requests.get(f"{OPENBAO_ADDR}/v1/sys/health")
            if r.status_code in (200, 429):
                print("OpenBao is ready.")
                return
        except requests.ConnectionError:
            pass
        time.sleep(1)
    raise RuntimeError("OpenBao did not become ready in time.")

def enable_kv():
    print("Enabling KV secrets engine...")
    r = requests.post(
        f"{OPENBAO_ADDR}/v1/sys/mounts/secret",
        headers=HEADERS,
        json={"type": "kv", "options": {"version": "2"}}
    )
    if r.status_code not in (204, 400):  # 400 means "already enabled"
        r.raise_for_status()
    print("KV secrets engine is enabled.")

def enable_approle():
    print("Enabling AppRole auth method...")
    r = requests.post(
        f"{OPENBAO_ADDR}/v1/sys/auth/approle",
        headers=HEADERS,
        json={"type": "approle"}
    )
    if r.status_code not in (204, 400):  # 400 means "already enabled"
        r.raise_for_status()
    print("AppRole auth method is enabled.")

def create_policy():
    print("Creating policy 'myapp-policy'...")
    policy = """
path "secret/data/myapp/*" {
  capabilities = ["create", "read", "update", "delete", "list"]
}
"""
    r = requests.put(
        f"{OPENBAO_ADDR}/v1/sys/policies/acl/myapp-policy",
        headers=HEADERS,
        json={"policy": policy}
    )
    r.raise_for_status()
    print("Policy 'myapp-policy' created.")

def create_approle():
    print("Creating AppRole 'myapp' with 'myapp-policy'...")
    r = requests.post(
        f"{OPENBAO_ADDR}/v1/auth/approle/role/myapp",
        headers=HEADERS,
        json={
            "secret_id_ttl": "60m",
            "token_ttl": "60m",
            "token_max_ttl": "120m",
            "policies": ["myapp-policy"]
        }
    )
    r.raise_for_status()
    print("AppRole 'myapp' created.")

def get_role_and_secret_id():
    print("Retrieving RoleID and SecretID...")
    r_role = requests.get(
        f"{OPENBAO_ADDR}/v1/auth/approle/role/myapp/role-id",
        headers=HEADERS
    )
    r_role.raise_for_status()
    role_id = r_role.json()["data"]["role_id"]

    r_secret = requests.post(
        f"{OPENBAO_ADDR}/v1/auth/approle/role/myapp/secret-id",
        headers=HEADERS
    )
    r_secret.raise_for_status()
    secret_id = r_secret.json()["data"]["secret_id"]

    print("\n✅ AppRole credentials generated:")
    print(f"ROLE_ID = {role_id}")
    print(f"SECRET_ID = {secret_id}")

if __name__ == "__main__":
    wait_for_openbao()
    enable_kv()
    enable_approle()
    create_policy()
    create_approle()
    get_role_and_secret_id()

