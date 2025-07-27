# Start containers
docker-compose up -d
# Initialize node1:
docker exec -it openbao1 bao operator init
 >>
        Unseal Key 1: Ppx4aBUfVbjG+W5GQEQ5a33geK0E5RPz4fevEuIj0I7C
        Unseal Key 2: 1N93TsgHC1gmrCSCT9r4NqTTW07ruNkibOwy8age74nd
        Unseal Key 3: IlocT/1K9THxTEVVN5lM1bSoeUOahNWaEP5N2l/K5oby
        Unseal Key 4: U+/okUbTVYpEKOstZl5w3R3FywZM2yyxPC1Tzu6fWAI8
        Unseal Key 5: xONrYjbFO+yT9Gh8ejsOVkDcqXXX4qLv6L9umNK/gq9w

        Initial Root Token: s.J0pe8613F3Q84s8cmKwKQbPs

# Unseal node1 with the unseal key:
docker exec -it openbao1 bao operator unseal <UNSEAL_KEY>

# Join node2 and node3 to the cluster
docker exec -it openbao2 bao operator raft join http://openbao1:8200
docker exec -it openbao3 bao operator raft join http://openbao1:8200

# Unseal node2 and node3 using the same unseal key
docker exec -it openbao2 bao operator unseal <UNSEAL_KEY>
docker exec -it openbao3 bao operator unseal <UNSEAL_KEY>


# Set the root token in the container before running the command "list-peers"
docker exec -e VAULT_TOKEN=s.J0pe8613F3Q84s8cmKwKQbPs -it openbao1 bao operator raft list-peers

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
docker exec -e VAULT_TOKEN=s.J0pe8613F3Q84s8cmKwKQbPs -it openbao2 bao operator raft list-peers

# From leader (openbao2)
docker exec -e VAULT_TOKEN=s.J0pe8613F3Q84s8cmKwKQbPs -it openbao2 bao operator raft remove-peer node1
docker exec -it openbao1 bao operator raft join http://openbao2:8200

docker exec -it openbao1 bao operator raft join http://openbao2:8200
docker exec -it openbao1 bao status
