import time
import requests

OPENBAO_ADDR = "http://localhost:8200"
ROOT_TOKEN = "s.OTnbebbRyAZyvJh2Kqqp2T9e"
headers = {"X-Vault-Token": ROOT_TOKEN}

def wait_for_openbao():
    for _ in range(30):
        try:
            r = requests.get(f"{OPENBAO_ADDR}/v1/sys/health")
            if r.status_code in (200, 429):  # 429 = unsealed and standby
                return
        except requests.ConnectionError as e:
            print('error', str(e))
            pass
        time.sleep(1)
    raise RuntimeError("OpenBao not ready.")

wait_for_openbao()

# Step 1: Initialize and unseal (only required once, use CLI or automate if needed)
# Step 2: Login with root token (already known for bootstrap)
# Step 3: Enable KV and AppRole auth
requests.post(f"{OPENBAO_ADDR}/v1/sys/mounts/secret", headers=headers, json={"type": "kv"})
requests.post(f"{OPENBAO_ADDR}/v1/sys/auth/approle", headers=headers, json={"type": "approle"})

# Step 4: Create AppRole
requests.post(f"{OPENBAO_ADDR}/v1/auth/approle/role/myapp", headers=headers, json={
    "secret_id_ttl": "60m",
    "token_ttl": "60m",
    "token_max_ttl": "120m",
    "policies": ["default"]
})

# Step 5: Get RoleID and SecretID
role_id = requests.get(f"{OPENBAO_ADDR}/v1/auth/approle/role/myapp/role-id", headers=headers).json()["data"]["role_id"]
secret_id = requests.post(f"{OPENBAO_ADDR}/v1/auth/approle/role/myapp/secret-id", headers=headers).json()["data"]["secret_id"]

print("ROLE_ID =", role_id)
print("SECRET_ID =", secret_id)

# Step 6: Store a secret
requests.post(f"{OPENBAO_ADDR}/v1/secret/data/myapp/config", headers=headers, json={
    "data": {
        "username": "prod_user",
        "password": "s3cr3t_prod_pw"
    }
})

