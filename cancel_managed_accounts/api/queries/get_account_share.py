from cancel_managed_accounts.utils import Logger
from cancel_managed_accounts.api.nerdgraph import NerdGraphClient

# Create logger for the module
logger = Logger(__name__).get_logger()

class AccountShares:
    GET_ACCOUNT_SHARES_QUERY = """
    query GetAccountShares($accountId: Int!) {
      customerAdministration {
        accountShares(filter: {accountId: {eq: $accountId}}) {
          items {
            accountId
            id
            name
          }
        }
      }
    }
    """

    def __init__(self, nerdgraph_client: NerdGraphClient):
        self.nerdgraph_client = nerdgraph_client

    def get_account_shares(self, account_id: int) -> dict:
        """
        Get account shares using the account ID.
        :param account_id: Account ID
        :return: dict
        """
        variables = {
            "accountId": account_id
        }

        result = self.nerdgraph_client.execute_query(self.GET_ACCOUNT_SHARES_QUERY, variables)
        if result.get("errors"):
            raise Exception(f"Failed to get account shares for account {account_id}: {result['errors']}")
        else:
            logger.info(f"Successfully got account shares for account {account_id}.")
            return result["data"]["customerAdministration"]["accountShares"]["items"]