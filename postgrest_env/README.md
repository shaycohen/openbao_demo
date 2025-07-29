# Remove all data first
docker-compose down -v
rm -rf ./data ./certs ./postgres/postgres-data ./postgres/certs

# create certificates
bash scripts/generate_certs.sh

# upload db
docker-compose up -d postgres

# start leader
docker-compose up -d openbao1

docker exec -it openbao1 bao operator init -key-shares=1 -key-threshold=1
docker exec -it openbao1 bao operator unseal <Unseal_Key>

# start peers
docker-compose up -d openbao2 openbao3

docker exec -it openbao2 bao operator unseal <Unseal_Key>
docker exec -it openbao3 bao operator unseal <Unseal_Key>

# see if peers added
docker exec -e VAULT_TOKEN= <TOKEN> -it openbao1 bao operator members
Active Node = true → This is the leader node

# test HA
docker stop openbao1
docker exec -e VAULT_TOKEN= <TOKEN> -it openbao2 bao operator members
