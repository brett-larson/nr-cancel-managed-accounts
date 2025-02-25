# New Relic Account Management Tool

A Python utility designed to programmatically cancel managed accounts in New Relic using the NerdGraph API.

## Overview

This application provides automation for canceling managed accounts in New Relic. It uses the NerdGraph GraphQL API to:

1. Read account IDs from a CSV file
2. Check if accounts are shared with other organizations
3. Revoke account sharing if necessary
4. Cancel the accounts

The tool includes rate limiting functionality to prevent API throttling and comprehensive logging to track all operations.

## Features

- CSV-based account processing
- Automatic revocation of account shares before cancellation
- Rate limiting to prevent API throttling
- Comprehensive logging of all actions and responses
- Error handling and reporting

## Prerequisites

- Python 3.8 or higher
- A New Relic account with appropriate permissions
- A New Relic User API key with permissions to cancel accounts

## Installation

### Using Poetry (Recommended)

```bash
# Clone the repository
git clone https://github.com/yourusername/nr-cancel-managed-accounts.git
cd nr-cancel-managed-accounts

# Install dependencies using Poetry
poetry install

# Activate the virtual environment
poetry shell
```

### Using pip

```bash
# Clone the repository
git clone https://github.com/yourusername/nr-cancel-managed-accounts.git
cd nr-cancel-managed-accounts

# Create and activate a virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Configuration

1. Create a `.env` file in the root directory with your New Relic API key:

```
NEW_RELIC_API_KEY=your_api_key_here
```

2. Prepare a CSV file with the account IDs you want to cancel. The file should be placed in the `cancel_managed_accounts/data/` directory and named `cancel-accounts.csv`. The CSV should have the following format:

```csv
account_id
1234567
1234568
1234569
```

## Usage

### Using Poetry

```bash
poetry run cancel-accounts
```

### Direct Python Execution

```bash
python -m cancel_managed_accounts.main
```

## How It Works

1. The application reads account IDs from the CSV file
2. For each account:
   - Checks if the account is already canceled
   - Checks if the account is shared with other organizations
   - If shared, revokes all account shares
   - Cancels the account
3. All actions are logged to the console and to a log file in the `logs` directory

## Project Structure

```
nr-cancel-managed-accounts/
├── cancel_managed_accounts/
│   ├── api/
│   │   ├── queries/
│   │   │   ├── __init__.py
│   │   │   ├── cancel_account.py
│   │   │   ├── get_account_share.py
│   │   │   ├── get_canceled_accounts.py
│   │   │   └── revoke_account_share.py
│   │   ├── __init__.py
│   │   ├── nerdgraph.py
│   │   └── rate_limiter.py
│   ├── data/
│   │   ├── __init__.py
│   │   └── csv_handler.py
│   ├── logs/
│   │   └── README.md
│   ├── utils/
│   │   ├── __init__.py
│   │   └── logger.py
│   ├── __init__.py
│   └── main.py
├── .env (not tracked in git)
├── .gitignore
├── LICENSE
├── README.md
├── poetry.lock
├── pyproject.toml
└── requirements.txt
```

## GraphQL Queries

The application uses the following GraphQL queries to interact with the New Relic API:

1. `CancelAccount` - Cancels a New Relic account
2. `GetAccountShares` - Gets all accounts shared with the specified account
3. `GetCanceledAccounts` - Gets all accounts that are already canceled
4. `RevokeSharedAccount` - Revokes an account share

## Logging

Logs are stored in the `cancel_managed_accounts/logs/` directory with the format `app_YYYYMMDD.log`. The logs contain detailed information about each step of the process, including API responses and any errors that occur.

## Error Handling

The application includes comprehensive error handling for various scenarios:
- Missing API key
- Failed API requests
- Invalid CSV format
- Failed account cancellations

## Rate Limiting

To prevent API throttling, the application includes a rate limiter that restricts the number of API calls to 100 per minute by default. This can be adjusted in the `main.py` file.

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Disclaimer

This tool has the potential to permanently cancel New Relic accounts. Use with caution and ensure you have appropriate permissions before running it.
