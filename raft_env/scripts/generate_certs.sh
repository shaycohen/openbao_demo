#!/bin/bash
set -e

CERTS_DIR="./certs"
mkdir -p "$CERTS_DIR"
cd "$CERTS_DIR"

echo "🔹 Generating CA..."
openssl genrsa -out ca.key 4096
openssl req -x509 -new -nodes -key ca.key -sha256 -days 3650 -out ca.crt \
  -subj "/C=US/ST=CA/L=SF/O=OpenBao/OU=CA/CN=OpenBao-CA"

# Node list for SANs and CN
ALL_DNS=("openbao1" "openbao2" "openbao3")
ALL_IPS=("127.0.0.1" "172.25.0.2" "172.25.0.3" "172.25.0.4")

# Format: cert_filename:CN:IP (cert_filename used for output files)
NODES=("openbao1:openbao1:172.25.0.2" "openbao2:openbao2:172.25.0.3" "openbao3:openbao3:172.25.0.4")

for entry in "${NODES[@]}"; do
  cert_name="${entry%%:*}"      # openbao1, openbao2, openbao3 (file names)
  rest="${entry#*:}"
  cn_name="${rest%%:*}"         # openbao1, openbao2, openbao3 (CN)
  ip="${rest##*:}"

  echo "🔹 Generating cert for $cn_name → $cert_name.crt / $cert_name.key"

  SAN_FILE="openssl-san-${cert_name}.cnf"
  {
    echo "[ req ]"
    echo "default_bits       = 2048"
    echo "prompt             = no"
    echo "default_md         = sha256"
    echo "req_extensions     = req_ext"
    echo "distinguished_name = dn"
    echo ""
    echo "[ dn ]"
    echo "C  = US"
    echo "ST = CA"
    echo "L  = SF"
    echo "O  = OpenBao"
    echo "OU = Node"
    echo "CN = ${cn_name}"
    echo ""
    echo "[ req_ext ]"
    echo "subjectAltName = @alt_names"
    echo ""
    echo "[ alt_names ]"
    i=1
    for d in "${ALL_DNS[@]}"; do
      echo "DNS.$i = $d"
      i=$((i+1))
    done
    for ipaddr in "${ALL_IPS[@]}"; do
      echo "IP.$i = $ipaddr"
      i=$((i+1))
    done
  } > "$SAN_FILE"

  # Generate key
  openssl genrsa -out "${cert_name}.key" 2048

  # Generate CSR with SANs
  openssl req -new -key "${cert_name}.key" -out "${cert_name}.csr" -config "$SAN_FILE" -reqexts req_ext

  # Sign certificate with SANs
  openssl x509 -req -in "${cert_name}.csr" -CA ca.crt -CAkey ca.key -CAcreateserial \
    -out "${cert_name}.crt" -days 365 -sha256 -extfile "$SAN_FILE" -extensions req_ext
done

echo "✅ All certs generated in $CERTS_DIR with CN=openbaoX and SANs for ALL nodes"