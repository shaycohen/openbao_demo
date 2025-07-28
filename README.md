# remove all env and data
docker-compose down -v 
rm -rf ./certs ./data

# Crete Certs
bash scripts/generate_certs.sh

# Start container
docker-compose up -d openbao1

# Initialize node1:  
docker exec -it openbao1 bao operator init -key-shares=1 -key-threshold=1
 >>
        Unseal Key 1: x
        Initial Root Token: s.x

# Check if openbao1 is seald:
docker exec -it openbao1 bao status
docker exec -it openbao1 bao operator unseal <UNSEAL_KEY>

# Start the other containers
docker-compose up -d openbao2 openbao3
docker exec -it openbao2 bao operator raft join https://openbao1:8200
docker exec -it openbao3 bao operator raft join https://openbao1:8200


# Unseal node1 with the unseal key:
docker exec -it openbao2 bao operator unseal <<UNSEAL_KEY> 
docker exec -it openbao3 bao operator unseal <<UNSEAL_KEY> 

# Set the root token in the container before running the command "list-peers"
docker exec -e VAULT_TOKEN= <TOKEN> -it openbao1 bao operator raft list-peers

# unseal node 2 and 3 
docker exec -it openbao2 bao operator unseal <<UNSEAL_KEY> 
docker exec -it openbao3 bao operator unseal <<UNSEAL_KEY> 

## Log in the ui ##
openbao1
https://localhost:8200
openbao2
https://localhost:8202
openbao3
https://localhost:8204