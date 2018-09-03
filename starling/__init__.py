from requests import get

BASE_URL = "https://api.starlingbank.com/api/v1"

class AccountBalance():

    def __init__(self):
        self.currency = None
        self.cleared_balance = None
        self.effective_balance = None
        self.pending_transactions = None
        self.available_to_spend = None
        self.accepted_overdraft = None
        self.amount = None

class StarlingAccount():

    def __init__(self, api_token):
        self._api_token = api_token
        
        self.balance = AccountBalance()
    
    def _url(self, endpoint):
        """Build a URL from the API's base URL."""
        return "{0}{1}".format(BASE_URL, endpoint)
    
    def _headers(self):
        """Build the headers required to authorise with the API."""
        return {"Authorization": "Bearer {0}".format(self._api_token)}

    def update_balance(self):
        """Get the latest balance information for the account."""
        response = get(self._url("/accounts/balance"), headers = self._headers()).json()

        self.balance.currency = response['currency']
        self.balance.cleared_balance = response['clearedBalance']
        self.balance.effective_balance = response['effectiveBalance']
        self.balance.pending_transactions = response['pendingTransactions']
        self.balance.available_to_spend = response['availableToSpend']
        self.balance.accepted_overdraft = response['acceptedOverdraft']
        self.balance.amount = response['amount']