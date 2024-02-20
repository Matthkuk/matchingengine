#input queue, 


#matching engine, 


#order book as SQL database, 
#BUY OR SELL ORDER - user 1, BUYS / SELLS, X INSTRUMENT, Y QUANTITY, Z1 BTC, Z2 ETH, Z3 USDT


#output queue
#USER 1, BOUGHT, X CURRENCY, Y QUANTITY, FOR Z CURRENCY, FROM USER 2


#To do:
'''
Quantity - Edit the quantity of the order after a transaction if there is leftover or delete
Find matches - change for first match DONE, get order_id, user_id, how to say nothing happens if no match is found
Orderbook - add a column for flag or delete or set everything to NULL
Transaction - takes the matches and does the transaction, returns something into the output queue, leftover editing

Input Queue:
User input

Output Queue:
Print in console code using output from transaction?
'''

#project flow
#2 files, manual input or simulation

# manual input
#run file, run userInput() in a while loop, at the end ask user if he wants to keep entering orders, if no, print remaining order table and exit, 
#I should print transactions if they are successful as soon as the user inputted an order that can be matched

# simulation
#user can enter how many users and how many orders he wants to generate, I will print every new order, and every successful transaction as they happen. 