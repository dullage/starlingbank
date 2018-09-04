from requests import get

BASE_URL = "https://api.starlingbank.com/api/v1"


def _url(endpoint):
    """Build a URL from the API's base URL."""
    return "{0}{1}".format(BASE_URL, endpoint)


class AccountBalance():

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
            _url("/accounts/balance"),
            headers=self._starling_account._auth_headers
        )
        response = response.json()

        self.currency = response['currency']
        self.cleared_balance = response['clearedBalance']
        self.effective_balance = response['effectiveBalance']
        self.pending_transactions = response['pendingTransactions']
        self.available_to_spend = response['availableToSpend']
        self.accepted_overdraft = response['acceptedOverdraft']
        self.amount = response['amount']


class StarlingAccount():

    def _get_account_data(self):
        """Get basic information for the account."""
        response = get(
            _url("/accounts"),
            headers=self._auth_headers
        )
        response = response.json()

        self.id = response['id']
        self.name = response['name']
        self.number = response['number']
        self.account_number = response['accountNumber']
        self.sort_code = response['sortCode']
        self.currency = response['currency']
        self.iban = response['iban']
        self.bic = response['bic']
        self.created_at = response['createdAt']

    def __init__(self, api_token):
        self._api_token = api_token
        self._auth_headers = {
            "Authorization": "Bearer {0}".format(self._api_token)
        }

        self._get_account_data()
        self.balance = AccountBalance(self)
