import csv
from typing import List
from cancel_managed_accounts.utils.logger import Logger

# Create logger for the module
logger = Logger(__name__).get_logger()

class CSVHandler:
    def __init__(self, file_path: str):
        self.file_path = file_path

    def read_account_numbers(self) -> List[int]:
        """
        Reads account numbers from a CSV file.
        :return: List of account numbers
        """
        account_numbers = []

        try:
            with open(self.file_path, mode='r') as file:
                csv_reader = csv.DictReader(file)
                for row in csv_reader:
                    account_numbers.append(int(row['account_id']))
            logger.info(f"Successfully read {len(account_numbers)} account numbers from {self.file_path}.")
        except FileNotFoundError:
            logger.error(f"File not found: {self.file_path}")
        except Exception as e:
            logger.error(f"Error reading CSV file: {e}")

        return account_numbers