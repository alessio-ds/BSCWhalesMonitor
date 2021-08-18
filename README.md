# BSC Whales Monitor
Monitors the latest transactions on any token you want.

Fully automated and tested, will (probably) never stop checking new transactions.

If it's >=$10k, it prints it and saves it in a logs.txt file. Or you can simply edit the line n°109 and choose by yourself:

`if dolla>=100000:`

![](https://i.imgur.com/Pt0LK0V.gif)

(updated version)

![](https://i.imgur.com/M7aKmHL.gif)

## How to use:

### **Python**:
You will need to install the [requests](https://pypi.org/project/requests/ "requests") library, by typing in your console:

`pip install requests`

Then, input your bscscan API key (get it from https://bscscan.com/myapikey) and any token you want. 

I tested this with $CAKE (0x0e09fabb73bd3ade0a17ecc321fd13a19e81ce82) and it works fine.
