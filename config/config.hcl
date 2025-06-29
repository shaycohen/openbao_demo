storage "raft" {
  path    = "/vault/data"
  node_id = "node1"
}

listener "tcp" {
  address     = "0.0.0.0:8200"
  tls_disable = true  # Use TLS in production!
}

ui = true  # Enables Bao Hi
api_addr = "http://localhost:8200"
cluster_addr = "http://localhost:8201"

