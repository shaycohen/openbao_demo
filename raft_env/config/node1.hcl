storage "raft" {
  path    = "/vault/data"
  node_id = "openbao1"
}

listener "tcp" {
  address     = "0.0.0.0:8200"
  cluster_address = "0.0.0.0:8201"  
  tls_disable   = false
  tls_cert_file = "/vault/certs/openbao1.crt"
  tls_key_file  = "/vault/certs/openbao1.key"
  tls_client_ca_file = "/vault/certs/ca.crt"
}

ui = true
api_addr     = "https://openbao1:8200"
cluster_addr = "https://openbao1:8201"