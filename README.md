# python-starling
**WORK IN PROGRESS**

A python package that provides limited access to the Starling bank API.

## Links

* https://www.starlingbank.com/
* https://developer.starlingbank.com/

## Usage
```
# Import the StarlingAccount class:
from starling import StarlingAccount

# Create a StarlingAccount object:
my_account = StarlingAccount("<INSERT API TOKEN HERE>")

# Update the objects account balance data:
my_account.balance.update()

# Print account effective balance:
print(my_account.balance.effective_balance)
```