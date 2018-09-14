# starlingbank

A python package that provides limited access to the Starling bank API.

## Links

* https://www.starlingbank.com/
* https://developer.starlingbank.com/

## Installation
```shell
pip install starlingbank
```

## Usage
### Import the StarlingAccount Class:
```python
from starlingbank import StarlingAccount
```

### Create a StarlingAccount Object:
```python
my_account = StarlingAccount("<INSERT API TOKEN HERE>")
```
If using a sandbox token:
```python
my_account = StarlingAccount("<INSERT API TOKEN HERE>", sandbox=True)
```

### Get Data
3 data sets are currently supported:

1. Basic Account Data
2. Balance Data
3. Savings Goal Data

To save on wasted API calls no data is collected when you initialise a StarlingAccount. You have to request / refresh each set of data as required with the following commands:

```python
my_account.get_account_data()
my_account.get_balance_data()
my_account.get_savings_goal_data()
```

#### Basic Account Data
Properties:

* id
* name
* number
* account_number
* sort_code
* currency
* iban
* bic
* created_at

Example:
```python
print(my_account.account_number)
```

#### Balance Data
Properties:

* currency
* cleared_balance
* effective_balance
* pending_transactions
* available_to_spend
* accepted_overdraft

Example:

```python
print(my_account.effective_balance)
```

#### Savings Goal Data
Savings goals are stored as a dictionary of objects where the dictionary key is the savings goals uid. To get a list of savings goal names and their respective uids you can run:

```python
for uid, goal in my_account.savings_goals.items():
    print("{0} = {1}".format(uid, goal.name))
```

Each goal has the following properties:

* uid
* name
* target_currency
* target_minor_units
* total_saved_currency
* total_saved_minor_units

_Note: Values are in minor units e.g. £1.50 will be represented as 150._

Example:
```python
print(my_account.savings_goals['c8553fd8-8260-65a6-885a-e0cb45691512'].total_saved_minor_units)
```

### Add to Savings Goal
You can add funds to a savings goal with the followng method:
```python
my_account.savings_goals['c8553fd8-8260-65a6-885a-e0cb45691512'].deposit(1000)
```

### Withdraw from a Savings Goal
You can add funds to a savings goal with the followng method:
```python
my_account.savings_goals['c8553fd8-8260-65a6-885a-e0cb45691512'].withdraw(1000)
```
