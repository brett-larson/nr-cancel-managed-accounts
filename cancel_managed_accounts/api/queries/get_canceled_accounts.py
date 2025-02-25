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

    def get_canceled_accounts(self, is_canceled: bool) -> dict:
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
    def parse_canceled_accounts_response(response: dict) -> list[Any] | Any:
        """
        Parse the response from the get canceled accounts API.
        :param response: dict
        :return: dict
        """
        try:
            logger.info("Parsing canceled accounts response")
            if 'data' in response and 'actor' in response['data'] and 'organization' in response['data']['actor'] and 'accountManagement' in response['data']['actor']['organization']:
                return response['data']['actor']['organization']['accountManagement']['managedAccounts']
            else:
                raise KeyError("Missing 'data', 'actor', 'organization', or 'accountManagement' in response")
        except (KeyError, TypeError) as e:
            logger.error(f"Error parsing canceled accounts response: {e}")
            return []