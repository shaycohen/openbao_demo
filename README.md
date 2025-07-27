# Start containers
docker-compose up -d
# Initialize node1:
docker exec -it openbao1 bao operator init
 >>
        Unseal Key 1: x
        Unseal Key 2: x
        Unseal Key 3: IlocT/x/K5oby
        Unseal Key 4: U+/x
        Unseal Key 5: x+/gq9w

        Initial Root Token: s.x

# Unseal node1 with the unseal key:
docker exec -it openbao1 bao operator unseal <UNSEAL_KEY>

# Join node2 and node3 to the cluster
docker exec -it openbao2 bao operator raft join http://openbao1:8200
docker exec -it openbao3 bao operator raft join http://openbao1:8200

# Unseal node2 and node3 using the same unseal key
docker exec -it openbao2 bao operator unseal <UNSEAL_KEY>
docker exec -it openbao3 bao operator unseal <UNSEAL_KEY>


# Set the root token in the container before running the command "list-peers"
docker exec -e VAULT_TOKEN= <TOKEN> -it openbao1 bao operator raft list-peers

# unseal node 2 and 3 
docker exec -it openbao2 bao operator unseal <<UNSEAL_KEY> #run 3 times with 3 diffrent key
docker exec -it openbao3 bao operator unseal <<UNSEAL_KEY> #run 3 times with 3 diffrent key

## Log in the ui ##
openbao1
http://localhost:8200
openbao2
http://localhost:8202
openbao3
http://localhost:8204


# ha testing -
docker stop openbao1

# Re-join peer to cluster
docker restart openbao1
docker exec -it openbao1 bao operator unseal <<UNSEAL_KEY>  # X3 times
docker exec -e VAULT_TOKEN=<TOKEN> -it openbao2 bao operator raft list-peers

# From leader (openbao2)
docker exec -e VAULT_TOKEN=<TOKEN> -it openbao2 bao operator raft remove-peer node1
docker exec -it openbao1 bao operator raft join http://openbao2:8200

docker exec -it openbao1 bao operator raft join http://openbao2:8200
docker exec -it openbao1 bao status
