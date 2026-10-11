from functools import lru_cache
import logging
import os

from azure.identity import ClientSecretCredential
from azure.keyvault.secrets import SecretClient

logger = logging.getLogger(__name__)


@lru_cache
def _client() -> SecretClient | None:
    vault_uri = os.environ.get("AZURE_KEY_VAULT_URI")
    if not vault_uri:
        return None
    try:
        credential = ClientSecretCredential(
            tenant_id=os.environ["AZURE_TENANT_ID"],
            client_id=os.environ["AZURE_CLIENT_ID"],
            client_secret=os.environ["AZURE_CLIENT_SECRET"],
        )
        return SecretClient(vault_url=vault_uri, credential=credential)
    except Exception:
        # Missing/invalid credential env vars — fall back rather than block app startup.
        logger.warning("Key Vault is configured but the client could not be built.", exc_info=True)
        return None


def get_secret(name: str) -> str | None:
    """
    Returns the named Key Vault secret, or None if no vault is configured for this workspace,
    or the vault can't be reached right now (DNS failure, network block, missing secret, bad
    credentials, ...). A secret fetch failing must never crash app startup — config.py falls
    back to its .env default whenever this returns None.
    """
    client = _client()
    if client is None:
        return None
    try:
        return client.get_secret(name).value
    except Exception:
        logger.warning("Could not fetch secret '%s' from Key Vault.", name, exc_info=True)
        return None
