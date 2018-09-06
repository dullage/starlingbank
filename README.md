# starlingbank

A python package that provides limited access to the Starling bank API.

## Links

* https://www.starlingbank.com/
* https://developer.starlingbank.com/

## Installation
```
pip install starlingbank
```

## Usage
### Import the StarlingAccount class:
```
from starlingbank import StarlingAccount
```

### Create a StarlingAccount object:
```
my_account = StarlingAccount("<INSERT API TOKEN HERE>")
```

### Print account data:
```
print(my_account.id)
print(my_account.name)
print(my_account.number)
print(my_account.account_number)
print(my_account.sort_code)
print(my_account.currency)
print(my_account.iban)
print(my_account.bic)
print(my_account.created_at)
```

### Update the objects account balance data:
```
my_account.balance.update()
```

### Print account balance data:
```
print(my_account.balance.currency)
print(my_account.balance.cleared_balance)
print(my_account.balance.effective_balance)
print(my_account.balance.pending_transactions)
print(my_account.balance.available_to_spend)
print(my_account.balance.accepted_overdraft)
print(my_account.balance.amount)
```