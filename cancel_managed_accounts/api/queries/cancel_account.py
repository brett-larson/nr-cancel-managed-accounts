from cancel_managed_accounts.utils import Logger
from cancel_managed_accounts.api.nerdgraph import NerdGraphClient

# Create logger for the module
logger = Logger(__name__).get_logger()

class AccountManager:
    CANCEL_ACCOUNT_QUERY = """
    mutation CancelAccount($id: Int!) {
      accountManagementCancelAccount(id: $id) {
        id
        isCanceled
        name
      }
    }
    """

    def __init__(self, nerdgraph_client: NerdGraphClient):
        self.nerdgraph_client = nerdgraph_client

    def cancel_account(self, account_id: int) -> dict:
        """
        Cancel an account using the account ID.
        :param account_id: Account ID
        :return: dict
        """
        variables = {
            "id": account_id
        }

        result = self.nerdgraph_client.execute_query(self.CANCEL_ACCOUNT_QUERY, variables)
        if result.get("errors"):
            raise Exception(f"Failed to cancel account {account_id}: {result['errors']}")
        else:
            logger.info(f"Successfully canceled account {account_id}.")
            return result["data"]["accountManagementCancelAccount"]

    @staticmethod
    def parse_cancel_account_response(response: dict) -> dict:
        """
        Parse the response from the cancel account API.
        :param response: dict
        :return: dict
        """
        try:
            logger.info("Parsing cancel account response")
            if 'data' in response and 'accountManagementCancelAccount' in response['data']:
                account_data = response['data']['accountManagementCancelAccount']
                return {
                    "id": account_data['id'],
                    "isCanceled": account_data['isCanceled'],
                    "name": account_data['name']
                }
            else:
                raise KeyError("Missing 'data' or 'accountManagementCancelAccount' in response")
        except (KeyError, TypeError) as e:
            logger.error(f"Error parsing cancel account response: {e}")
            return {
                "id": None,
                "isCanceled": None,
                "name": None
            }
