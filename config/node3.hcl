storage "raft" {
  path    = "/vault/data"
  node_id = "node3"
}

listener "tcp" {
  address     = "0.0.0.0:8200"
  tls_disable = true
}

ui = true
api_addr     = "http://openbao3:8200"
cluster_addr = "http://openbao3:8201"