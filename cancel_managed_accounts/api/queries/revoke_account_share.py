from cancel_managed_accounts.utils import Logger
from cancel_managed_accounts.api.nerdgraph import NerdGraphClient

# Create logger for the module
logger = Logger(__name__).get_logger()

class AccountSharesRevoke:
    ACCOUNT_SHARE_REVOKE_QUERY = """mutation RevokeSharedAccount($sharedAccountId: String!) {
  organizationRevokeSharedAccount(
    sharedAccount: {id: $sharedAccountId}
  ) {
    sharedAccount {
      accountId
      id
      name
      sourceOrganizationId
      sourceOrganizationName
      targetOrganizationId
      targetOrganizationName
    }
  }
}
"""

    def __init__(self, nerdgraph_client: NerdGraphClient):
        self.nerdgraph_client = nerdgraph_client

    def revoke_account_share(self, shared_account_id: str) -> dict:
        """
        Revoke a shared account using the shared account ID.
        :param shared_account_id: Shared account ID
        :return: dict
        """
        variables = {
            "sharedAccountId": shared_account_id
        }

        result = self.nerdgraph_client.execute_query(self.ACCOUNT_SHARE_REVOKE_QUERY, variables)
        if result.get("errors"):
            raise Exception(f"Failed to revoke shared account {shared_account_id}: {result['errors']}")
        else:
            logger.info(f"Successfully revoked shared account {shared_account_id}.")
            logger.info(f"Response: {result}")
            return result["data"]["organizationRevokeSharedAccount"]["sharedAccount"]