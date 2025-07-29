storage "postgresql" {
  connection_url = "postgresql://vault:vaultpass@postgres:5432/vaultdb?sslmode=require"
  ha_enabled     = "true"
}

listener "tcp" {
  address     = "0.0.0.0:8200"
  cluster_address = "0.0.0.0:8201"  
  tls_disable   = false
  tls_cert_file = "/vault/certs/openbao2.crt"
  tls_key_file  = "/vault/certs/openbao2.key"
  tls_client_ca_file = "/vault/certs/ca.crt"
}

ui = true
api_addr     = "https://openbao2:8200"
cluster_addr = "https://openbao2:8201"