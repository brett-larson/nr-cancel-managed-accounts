from typing import Any

from cancel_managed_accounts.utils import Logger
from cancel_managed_accounts.api.nerdgraph import NerdGraphClient

# Create logger for the module
logger = Logger(__name__).get_logger()

class CanceledAccounts:
    GET_CANCELED_ACCOUNTS = """
    query GetCanceledAccounts($isCanceled: Boolean!) {
      actor {
        organization {
          accountManagement {
            managedAccounts(isCanceled: $isCanceled) {
              id
              name
              isCanceled
              regionCode
            }
          }
        }
      }
    }
    """

    def __init__(self, nerdgraph_client: NerdGraphClient):
        self.nerdgraph_client = nerdgraph_client

    def get_canceled_accounts(self, is_canceled: bool) -> list[int]:
        """
        Get canceled accounts using the isCanceled flag.
        :param is_canceled: Boolean. Set to true to get canceled accounts by default
        :return: dict
        """
        variables = {
            "isCanceled": is_canceled
        }

        try:
            result = self.nerdgraph_client.execute_query(self.GET_CANCELED_ACCOUNTS, variables)
            if result.get("errors"):
                raise Exception(f"Failed to get canceled accounts: {result['errors']}")
            logger.info("Successfully retrieved canceled accounts.")
            return self.parse_canceled_accounts_response(result)
        except Exception as e:
            logger.error(f"Error getting canceled accounts: {e}")
            return {}


    @staticmethod
    def parse_canceled_accounts_response(response: dict) -> list[int]:
        """
        Parse the response from the get canceled accounts API to extract canceled account numbers.
        :param response: dict
        :return: list of canceled account numbers
        """
        try:
            logger.info("Parsing canceled accounts response")
            managed_accounts = (
                response.get('data', {})
                        .get('actor', {})
                        .get('organization', {})
                        .get('accountManagement', {})
                        .get('managedAccounts', [])
            )
            return [account['id'] for account in managed_accounts if account.get('isCanceled')]
        except (KeyError, TypeError) as e:
            logger.error(f"Error parsing canceled accounts response: {e}")
            return []