from cancel_managed_accounts.api.nerdgraph import NerdGraphClient
from cancel_managed_accounts.utils import Logger
from cancel_managed_accounts.api.rate_limiter import RateLimiter
from cancel_managed_accounts.data.csv_handler import CSVHandler
from cancel_managed_accounts.api.queries.cancel_account import AccountManager

# Create logger for the module
logger = Logger(__name__).get_logger()

def main():
    logger.info("********** Application started. **********")

    rate_limiter = RateLimiter(calls_per_minute=5)
    csv_handler = CSVHandler(file_path='cancel_managed_accounts/data/cancel-accounts.csv')
    nerdgraph_client = NerdGraphClient()
    account_manager = AccountManager(nerdgraph_client)

    account_numbers = csv_handler.read_account_numbers()
    logger.info(f"Account numbers: {account_numbers}")

    for account in account_numbers:
        rate_limiter.wait_if_needed()
        logger.info(f"Canceling account {account}.")

        try:
            response = account_manager.cancel_account(account)
            logger.info(f"Response: {response}")
        except Exception as e:
            logger.error(f"Error canceling account {account}: {e}")

    logger.info("********** Application finished. **********")

if __name__ == "__main__":
    main()