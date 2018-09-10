"""Provides limited access to the Starling bank API."""
from requests import get

__version__ = "1.2"

BASE_URL = "https://api.starlingbank.com/api/v1"
BASE_URL_SANDBOX = "https://api-sandbox.starlingbank.com/api/v1"


def _url(endpoint, sandbox=False):
    """Build a URL from the API's base URL."""
    if sandbox is True:
        url = BASE_URL_SANDBOX
    else:
        url = BASE_URL
    return "{0}{1}".format(url, endpoint)


class _AccountBalance():

    def __init__(self, starling_account):
        self._starling_account = starling_account

        self.currency = None
        self.cleared_balance = None
        self.effective_balance = None
        self.pending_transactions = None
        self.available_to_spend = None
        self.accepted_overdraft = None
        self.amount = None

    def update(self):
        """Get the latest balance information for the account."""
        response = get(
            _url("/accounts/balance", self._starling_account._sandbox),
            headers=self._starling_account._auth_headers
        )
        response.raise_for_status()

        response = response.json()
        self.currency = response.get('currency')
        self.cleared_balance = response.get('clearedBalance')
        self.effective_balance = response.get('effectiveBalance')
        self.pending_transactions = response.get('pendingTransactions')
        self.available_to_spend = response.get('availableToSpend')
        self.accepted_overdraft = response.get('acceptedOverdraft')
        self.amount = response.get('amount')


class StarlingAccount():
    """Representation of a Starling Account."""

    def _get_account_data(self):
        """Get basic information for the account."""
        response = get(
            _url("/accounts", self._sandbox),
            headers=self._auth_headers
        )
        response.raise_for_status()

        response = response.json()
        self.id = response.get('id')
        self.name = response.get('name')
        self.number = response.get('number')
        self.account_number = response.get('accountNumber')
        self.sort_code = response.get('sortCode')
        self.currency = response.get('currency')
        self.iban = response.get('iban')
        self.bic = response.get('bic')
        self.created_at = response.get('createdAt')

    def __init__(self, api_token, sandbox=False):
        self._api_token = api_token
        self._sandbox = sandbox
        self._auth_headers = {
            "Authorization": "Bearer {0}".format(self._api_token)
        }

        self._get_account_data()
        self.balance = _AccountBalance(self)
