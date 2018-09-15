"""Provides limited access to the Starling bank API."""
from requests import get, put
from uuid import uuid4
from json import dumps as json_dumps
from base64 import b64decode
from typing import Dict

__version__ = "2.0dev"

BASE_URL = "https://api.starlingbank.com/api/v1"
BASE_URL_SANDBOX = "https://api-sandbox.starlingbank.com/api/v1"


def _url(endpoint: str, sandbox: bool=False) -> str:
    """Build a URL from the API's base URLs."""
    if sandbox is True:
        url = BASE_URL_SANDBOX
    else:
        url = BASE_URL
    return "{0}{1}".format(url, endpoint)


class SavingsGoal():
    """Representation of a Savings Goal."""

    def __init__(self, auth_headers: Dict, sandbox: bool) -> None:
        self._auth_headers = auth_headers
        self._sandbox = sandbox

        self.uid = None
        self.name = None
        self.target_currency = None
        self.target_minor_units = None
        self.total_saved_currency = None
        self.total_saved_minor_units = None

    def update(self, goal: Dict=None) -> None:
        """Update a single savings goals data."""
        if goal is None:
            endpoint = "/savings-goals/{0}".format(self.uid)

            response = get(
                _url(endpoint, self._sandbox),
                headers=self._auth_headers
            )
            response.raise_for_status()
            goal = response.json()

        self.uid = goal.get('uid')
        self.name = goal.get('name')

        target = goal.get('target', {})
        self.target_currency = target.get('currency')
        self.target_minor_units = target.get('minorUnits')

        total_saved = goal.get('totalSaved', {})
        self.total_saved_currency = total_saved.get('currency')
        self.total_saved_minor_units = total_saved.get('minorUnits')

    def deposit(self, deposit_minor_units: int) -> None:
        """Add funds to a savings goal."""
        endpoint = "/savings-goals/{0}/add-money/{1}".format(self.uid, uuid4())

        body = {
            "amount": {
                "currency": self.total_saved_currency,
                "minorUnits": deposit_minor_units
            }
        }

        response = put(
            _url(endpoint, self._sandbox),
            headers=self._auth_headers,
            data=json_dumps(body)
        )
        response.raise_for_status()

        self.update()

    def withdraw(self, withdraw_minor_units: int) -> None:
        """Withdraw funds from a savings goal."""
        endpoint = "/savings-goals/{0}/withdraw-money/{1}".format(
            self.uid,
            uuid4()
        )

        body = {
            "amount": {
                "currency": self.total_saved_currency,
                "minorUnits": withdraw_minor_units
            }
        }

        response = put(
            _url(endpoint, self._sandbox),
            headers=self._auth_headers,
            data=json_dumps(body)
        )
        response.raise_for_status()

        self.update()

    def get_image(self, filename: str=None) -> None:
        """Download the photo associated with a Savings Goal."""
        if filename is None:
            filename = "{0}.png".format(self.name)

        endpoint = "/savings-goals/{0}/photo".format(
            self.uid
        )

        response = get(
            _url(endpoint, self._sandbox),
            headers=self._auth_headers
        )
        response.raise_for_status()

        base64_image = response.json()['base64EncodedPhoto']
        with open(filename, 'wb') as file:
            file.write(b64decode(base64_image))


class StarlingAccount():
    """Representation of a Starling Account."""

    def update_account_data(self) -> None:
        """Get basic information for the account."""
        response = get(
            _url("/accounts", self._sandbox),
            headers=self._auth_headers
        )
        response.raise_for_status()

        response = response.json()
        self.id = response.get('id')
        self.name = response.get('name')
        self.account_number = response.get('accountNumber')
        self.sort_code = response.get('sortCode')
        self.currency = response.get('currency')
        self.iban = response.get('iban')
        self.bic = response.get('bic')
        self.created_at = response.get('createdAt')

    def update_balance_data(self) -> None:
        """Get the latest balance information for the account."""
        response = get(
            _url("/accounts/balance", self._sandbox),
            headers=self._auth_headers
        )
        response.raise_for_status()

        response = response.json()
        self.currency = response.get('currency')
        self.cleared_balance = response.get('clearedBalance')
        self.effective_balance = response.get('effectiveBalance')
        self.pending_transactions = response.get('pendingTransactions')
        self.available_to_spend = response.get('availableToSpend')
        self.accepted_overdraft = response.get('acceptedOverdraft')

    def update_savings_goal_data(self) -> None:
        """Get the latest savings goal information for the account."""
        response = get(
            _url("/savings-goals", self._sandbox),
            headers=self._auth_headers
        )
        response.raise_for_status()

        response = response.json()
        response_savings_goals = response.get('savingsGoalList', {})

        returned_uids = []

        # New / Update
        for goal in response_savings_goals:
            uid = goal.get('uid')
            returned_uids.append(uid)

            # Intiialise new _SavingsGoal object if new
            if uid not in self.savings_goals:
                self.savings_goals[uid] = SavingsGoal(
                    self._auth_headers,
                    self._sandbox
                )

            self.savings_goals[uid].update(goal)

        # Forget about savings goals if the UID isn't returned by Starling
        for uid in list(self.savings_goals):
            if uid not in returned_uids:
                self.savings_goals.pop(uid)

    def __init__(self, api_token: str, sandbox: bool=False) -> None:
        """Call to initialise a StarlingAccount object."""
        self._api_token = api_token
        self._sandbox = sandbox
        self._auth_headers = {
            "Authorization": "Bearer {0}".format(self._api_token),
            "Content-Type": "application/json"
        }

        # Account Data
        self.id = None
        self.name = None
        self.account_number = None
        self.sort_code = None
        self.currency = None
        self.iban = None
        self.bic = None
        self.created_at = None

        # Balance Data
        self.currency = None
        self.cleared_balance = None
        self.effective_balance = None
        self.pending_transactions = None
        self.available_to_spend = None
        self.accepted_overdraft = None

        # Savings Goals Data
        self.savings_goals: Dict[str: SavingsGoal] = {}
