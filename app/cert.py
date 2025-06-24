from fastapi import APIRouter
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
import os

router = APIRouter()

@router.get("/fetch-cert")
def fetch_ssl_cert():
    key_vault_url = os.getenv("AZURE_KEY_VAULT_URL")
    secret_name = os.getenv("AZURE_CERT_SECRET_NAME")
    credential = DefaultAzureCredential()
    client = SecretClient(vault_url=key_vault_url, credential=credential)
    cert = client.get_secret(secret_name)

    with open("nginx_cert.pem", "w") as f:
        f.write(cert.value)

    return {"message": "SSL cert fetched and written to nginx_cert.pem"}
