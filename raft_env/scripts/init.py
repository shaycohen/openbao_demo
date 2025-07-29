import time
import requests

api_url = "http://localhost:8200"
root_token = input('root token: ')
headers = {"X-Vault-Token": root_token}

def wait_for_openbao():
    for _ in range(30):
        try:
            r = requests.get(f"{api_url}/v1/sys/health")
            if r.status_code in (200, 429):  # 429 = unsealed and standby
                return
        except requests.ConnectionError as e:
            print('error', str(e))
            pass
        time.sleep(1)
    raise RuntimeError("OpenBao not ready.")

wait_for_openbao()

requests.post(f"{api_url}/v1/sys/auth/approle", headers=headers, json={"type": "approle"})

envs = ['dev', 'tst', 'prd']
app = input('app: ')
apps = [app]
for env in envs: 
    requests.post(f"{api_url}/v1/sys/mounts/{env}", headers=headers, json={"type": "kv"})

    for app in apps: 
        policy = f"""
        path "{env}/{app}/*" {{
          capabilities = ["read", "list"]
        }}
        """

        r = requests.put(
            f"{api_url}/v1/sys/policies/acl/{env}_{app}-policy",
            headers=headers,
            json={"policy": policy}
        )
        r.raise_for_status()

        requests.post(f"{api_url}/v1/auth/approle/role/{app}_{env}", headers=headers, json={
            "secret_id_ttl": "60m",
            "token_ttl": "60m",
            "token_max_ttl": "120m",
            "policies": [f"{env}_{app}-policy"]
        })
        role_id = requests.get(f"{api_url}/v1/auth/approle/role/{app}_{env}/role-id", headers=headers).json()["data"]["role_id"]
        secret_id = requests.post(f"{api_url}/v1/auth/approle/role/{app}_{env}/secret-id", headers=headers).json()["data"]["secret_id"]
        print(env, app, role_id, secret_id)
        requests.post(f"{api_url}/v1/{env}/{app}/secret_ini", headers=headers, json={
            f"data_{env}_{app}": {
                "username": "prod_user",
                "password": "s3cr3t_prod_pw"
            }
        })




