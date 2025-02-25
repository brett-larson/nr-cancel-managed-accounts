from api.nerdgraph import NerdGraphClient
from utils import Logger
from api.rate_limiter import RateLimiter
from data.csv_handler import CSVHandler
from api.queries.cancel_account import AccountManager
from api.queries.get_account_share import AccountShares
from api.queries.get_canceled_accounts import CanceledAccounts

# Create logger for the module
logger = Logger(__name__).get_logger()

def main():
    logger.info("********** Application started. **********")
    response = None
    rate_limiter = RateLimiter(calls_per_minute=100)
    csv_handler = CSVHandler(file_path='../cancel_managed_accounts/data/cancel-accounts.csv')
    nerdgraph_client = NerdGraphClient()

    # Get account numbers we want to cancel from the CSV file
    try:
        account_numbers = csv_handler.read_account_numbers()
        logger.info(f"Account numbers: {account_numbers}")
    except Exception as e:
        logger.error(f"Error reading account numbers from CSV: {e}")
        return

    # Get all canceled accounts to compare to the list of accounts we want to cancel
    try:
        canceled_accounts = CanceledAccounts(nerdgraph_client)
        canceled_accounts_data = canceled_accounts.get_canceled_accounts(True)
    except Exception as e:
        logger.error(f"Error getting canceled accounts: {e}")
        return

    # Check if any of the accounts we want to cancel are already canceled
    try:
        for account in account_numbers:
            print(account)
            for canceled_account in canceled_accounts_data:
                print(canceled_account)
                if account == canceled_account['id']:
                    logger.info(f"Account {account} is already canceled. Removing from list.")
                    account_numbers.remove(account)
                    break
    except Exception as e:
        logger.error(f"Error checking if accounts are already canceled: {e}")
        return
    logger.info(f"Accounts to cancel: {account_numbers}")


    account_shares = AccountShares(nerdgraph_client)
    # response = account_shares.get_account_shares(229775)
    # logger.info(f"Response: {response}")
    # print(account_shares.get_account_shares(229775))

    for account in account_numbers:
        rate_limiter.wait_if_needed()
        logger.info(f"Checking if account {account} is shared.")

        try:
            response = account_shares.get_account_shares(account)
            logger.info(f"Response: {response}")
        except Exception as e:
            logger.error(f"Error checking account shares for account {account}: {e}")

        if not response:
            logger.info(f"No account shares found for account {account}.")
        else:
            logger.info(f"Account shares found for account {account}.")

    # account_manager = AccountManager(nerdgraph_client)
    #
    # account_numbers = csv_handler.read_account_numbers()
    # logger.info(f"Account numbers: {account_numbers}")
    #
    # for account in account_numbers:
    #     rate_limiter.wait_if_needed()
    #     logger.info(f"Canceling account {account}.")
    #
    #     try:
    #         response = account_manager.cancel_account(account)
    #         logger.info(f"Response: {response}")
    #     except Exception as e:
    #         logger.error(f"Error canceling account {account}: {e}")

    logger.info("********** Application finished. **********")

if __name__ == "__main__":
    main()