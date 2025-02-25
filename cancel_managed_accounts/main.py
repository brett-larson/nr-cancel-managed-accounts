from api.nerdgraph import NerdGraphClient
from utils import Logger
from api.rate_limiter import RateLimiter
from data.csv_handler import CSVHandler
from api.queries.cancel_account import AccountManager
from api.queries.get_account_share import AccountShares
from api.queries.get_canceled_accounts import CanceledAccounts
from api.queries.revoke_account_share import AccountSharesRevoke

# Create logger for the module
logger = Logger(__name__).get_logger()

def main():
    logger.info("********** Application started. **********")
    response = None
    rate_limiter = RateLimiter(calls_per_minute=100)
    csv_handler = CSVHandler(file_path='../cancel_managed_accounts/data/cancel-accounts.csv')
    nerdgraph_client = NerdGraphClient()
    account_shares = AccountShares(nerdgraph_client)
    account_share_revoke = AccountSharesRevoke(nerdgraph_client)
    account_manager = AccountManager(nerdgraph_client)

    # Get account numbers we want to cancel from the CSV file
    try:
        account_numbers = csv_handler.read_account_numbers()
        print(type(account_numbers))
        logger.info(f"Account numbers: {account_numbers}")
    except Exception as e:
        logger.error(f"Error reading account numbers from CSV: {e}")
        return

    # Get all canceled accounts to compare to the list of accounts we want to cancel
    try:
        canceled_accounts = CanceledAccounts(nerdgraph_client)
        print(type(canceled_accounts))
        canceled_account_ids = canceled_accounts.get_canceled_accounts(True)
        print(type(canceled_account_ids))
    except Exception as e:
        logger.error(f"Error getting canceled accounts: {e}")
        return

    # Check if any of the accounts we want to cancel are already canceled
    try:
        account_numbers_to_cancel = [
            account for account in account_numbers if account not in canceled_account_ids
        ]

        logger.info(f"Accounts to cancel: {account_numbers_to_cancel}")
    except Exception as e:
        logger.error(f"Error checking if accounts are already canceled: {e}")
        return

    # If there are no accounts to cancel, exit the application.
    if not account_numbers:
        logger.info("No accounts to cancel. Exiting application.")
        return

    """
    Check if any of the accounts we want to cancel are shared, and revoke any account shares.
    Account shares must be revoked before an account can be canceled.
    """
    for account in account_numbers:
        rate_limiter.wait_if_needed()
        logger.info(f"Checking if account {account} is shared.")

        try:
            response = account_shares.get_account_shares(account)
            logger.info(f"Response: {response}")
        except Exception as e:
            logger.error(f"Error checking account shares for account {account}: {e}")

        if not response:
            logger.info(f"No account shares found for account {account}. Cancelling account.")

            try:
                rate_limiter.wait_if_needed()
                response = account_manager.cancel_account(account)
                logger.info(f"Response: {response}")
            except Exception as e:
                logger.error(f"Error canceling account {account}: {e}")

        else:
            logger.info(f"Account shares found for account {account}. Revoking account shares.")

            try:
                for shared_account in response:
                    rate_limiter.wait_if_needed()
                    logger.info(f"Revoking account share {shared_account['id']}.")
                    response = account_share_revoke.revoke_account_share(shared_account['id'])
                    logger.info(f"Response: {response}")
            except Exception as e:
                logger.error(f"Error revoking account shares for account {account}: {e}")

            logger.info(f"Account shares revoked for account {account}. Cancelling account.")

            try:
                rate_limiter.wait_if_needed()
                # Comment out the following line to prevent account cancellation.
                response = account_manager.cancel_account(account)
                logger.info(f"Successfully canceled account {account}. Response: {response}")
            except Exception as e:
                logger.error(f"Error canceling account {account}: {e}")

    logger.info("********** Application finished. **********")

if __name__ == "__main__":
    main()