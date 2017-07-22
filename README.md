# ibopt 
ibopt is an IbPy-like interface for the Interactive Brokers Python API.

The targeted audience for ibopt includes (a) old IbPy users who want to upgrade to the latest Interactive Brokers API release, or (b) non-IbPy Pythonistas who find the Java-centric paradigm of the IB API heavy on boilerplate and short on Pythonic elegance.

## Background

Prior to 2017, [IbPy](https://github.com/blampe/IbPy) was the de facto way to connect to the Interactive Brokers API using Python. Beginning with API release 9.73, Interactive Brokers now officially supports a Python API client, rendering IbPy largely obsolete. IbPy development stopped with API release 970, meaning users who still use IbPy don't have access to a considerable number of features which Interactive Brokers has added in subsequent API releases.

Although the Java-to-Python translation which IbPy provided is now superfluous, IbPy also provided its own so-called "optional" interface which many IbPy users found more convenient than the default paradigm of subclassing `EClient` and `EWrapper`. 

ibopt is a fork of IbPy which removes the translated Java code from `ib.ext` and updates the optional interface in `ib.opt` to support the offical Python API client. 

## Installation

Install from pip:

```
pip install ibopt
```

## Requirements

* Interactive Brokers Python API client. The client isn't automatically installed by ibopt; it is available [here](https://interactivebrokers.github.io/). The client requires Python 3.
* ibopt installs [ibapi-grease](https://github.com/quantrocket-llc/ibapi-grease) to deal with some current slowness in the Python API client implementation. If you don't want this, install ibopt with no dependencies: `pip install --no-deps ibopt`

## Quickstart

Usage looks very similar to IbPy:
    
```python
from ibopt import ibConnection, message
from ibapi.contract import Contract

def contractDetailsHandler(msg):
    print(msg.contractDetails)
    # do something with contractDetails msg

def errorHandler(msg):
    print(msg)

conn = ibConnection(port=4001, clientId=100)

conn.register(contractDetailsHandler, message.contractDetails)
conn.register(errorHandler, message.error)

contract = Contract()
contract.symbol = "AAPL"
contract.exchange = "SMART"
contract.secType = "STK"
contract.currency = "USD"

conn.connect()
conn.reqContractDetails(1, contract)

conn.unregister(contractDetailsHandler, message.contractDetails)
conn.unregister(errorHandler, message.error)

conn.disconnect()
```

## Migrating from IbPy

ibopt is IbPy-like but it is not a drop-in replacement for IbPy. Migrating existing code from IbPy to ibopt will involve, at minimum, the following changes:

* **import paths have changed**: Anything your code imports from `ib.opt` will now come from `ibopt`.
* **ib.ext is gone, use ibapi instead**: Anything your code imports from `ib.ext`, such as `Contract` and `Order` objects, will now need to come from the relevant `ibapi` module. Moreover, the attribute name for these objects have changed (for example, `Contract.m_conId` is now `Contract.conId`). Review the API client documentation for details: https://interactivebrokers.github.io/tws-api/index.html#gsc.tab=0
* **TickType.getField has changed**: If your code uses `TickType.getField(tickType)` to look up field names by tick type integers, the field names have changed. For example, `'bidSize'` is now `'BID_SIZE'`. You can see the new names by looking at `ibapi.ticktype.TickTypeEnum`.
* **Python 3 only**: The official Python client from Interactive Brokers requires Python 3. 


There are probably additional gotchas.  

## Contributing

Contributions and pull requests are welcome. Right now, updating the `demo` directory to work with `ibapi` would be especially welcome.

ibopt is maintained by the team at [QuantRocket](https://www.quantrocket.com). QuantRocket is a Docker-based microservice platform for automated trading with Interactive Brokers. QuantRocket is currently under development, so our focus is on building out the platform and updating ibopt as needed by the platform. In the short term, this may limit our bandwidth for making changes to ibopt not required by our platform; however, we are beneficiaries of open source software and intend to maintain ibopt indefinitely going forward.
 
## Usage guide
*[the following guide is taken directly from the IbPy wiki]*

ibopt provides an optional interface that does not require subclassing. This interface provides several conveniences for your use.

To interoperate with this package, first define your handlers. Each handler must take a single parameter, a Message instance. Instances of Message have attributes and values set by the connection object before they're passed to your handler.

After your handlers are defined, you associate them with the connection object via the register method. You pass your handler as the first parameter, and you indicate what message types to send it with parameters that follow it. Message types can be strings, or better, Message classes. Both forms are shown here:

    connection.register(my_account_handler, 'UpdateAccountValue')
    connection.register(my_tick_handler, message.TickPrice, message.TickSize)

You can break the association between your handlers and messages with the unregister method, like so:

    connection.unregister(my_tick_handler, message.TickSize)

In the above example, my_tick_handler will still be called with TickPrice messages.

Connection objects also allow you to associate a handler with all messages generated. The call looks like this:

    connection.registerAll(my_generic_handler)

And of course, there's an unregisterAll method as well:

    connection.unregisterAll(my_generic_handler)

### Attributes
The Connection class exposes the attributes of its connection, so you can write:

    connection.reqIds()

### Logging
The Connection class provides a basic logging facility (via the Python logging module). To activate it, call it like this:

    connection.enableLogging()

To deactivate logging, call the same method with False as the first parameter:

    connection.enableLogging(False)

### Message Objects
Your handlers are passed a single parameter, an instance of the Message class (or one of its subclasses). These instances will have attributes that match the parameter names from the underlying method call. For example, when you're passed a Message instance generated from a TickSize call, the object might look like this:

    msg.tickerId = 4
    msg.field = 3
    msg.size = 100
    
## License

ibopt is distributed under the New BSD License. See the LICENSE file in the
release for details.

## Note

ibopt is not a product of Interactive Brokers, nor is this project affiliated
with IB.
