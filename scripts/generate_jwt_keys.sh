#!/bin/bash
set -e


# ==============================
#  Generate RSA keys for JWT
#  Keys are created in ./keys/
#  relative to where the script is run
# ==============================


SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
WORK_DIR="$(pwd)"
KEYS_DIR="$WORK_DIR/keys"

PRIVATE_KEY="$KEYS_DIR/private.pem"
PUBLIC_KEY="$KEYS_DIR/public.pem"

if [[ -f "$PRIVATE_KEY" && -f "$PUBLIC_KEY" ]]; then
    echo "🔑 JWT keys already exist. Skipping generation."
    exit 0
fi

mkdir -p "$KEYS_DIR"

openssl genrsa -out "$PRIVATE_KEY" 2048
openssl rsa -in "$PRIVATE_KEY" -pubout -out "$PUBLIC_KEY"

chmod 600 "$PRIVATE_KEY"
chmod 644 "$PUBLIC_KEY"

echo "✅ RSA key pair generated successfully!"
echo "📁 Private key: $PRIVATE_KEY"
echo "📁 Public key:  $PUBLIC_KEY"
