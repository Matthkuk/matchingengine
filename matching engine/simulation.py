#simulation of users placing orders
from functions import *
import random as rand

'''user_count = 10#must be 1 or above
max_order_count = 10
max_quantity = 50#max quantity a user can buy or sell in a single order'''

df_orderBook, df_inputq, df_transaction = orderBook_init()
#print(df_orderBook)

def generate(user_count, max_quantity):
    '''
    Randomly generate numbers to be used in adding an order.
    Prints a sentance that conveys what numbers / order was generated.
    '''

    #choose a random user
    user_id = rand.randint(1, user_count)
    #user id's will always look like user1, user2, user3, etc

    #buy or sell
    order_type = rand.randint(0, 1)

    #instrument
    instrument = rand.randint(1, 3)

    #quantity
    quantity = rand.randint(1, max_quantity)

    #prices
    btc = eth = usdt = None #initialize to null
    if not instrument == 1: 
        btc = round(rand.random()*2, 2)#generate decimal number from 0-2, and round to 2 decimal places
    if not instrument == 2:
        eth = round(rand.random()*2, 2)
    if not instrument == 3:
        usdt = round(rand.random()*2, 2)

    if order_type == 1:
        order_type_str = "buy"
    elif order_type == 0:
        order_type_str = "sell"
    
    if instrument == 1:
        instrument_str = "Bitcoin"
    elif instrument == 2:
        instrument_str = "Ethereum"
    elif instrument == 3:
        instrument_str = "USDT"

    #print("User ID: {0} wants to {1} {2} {3} for {4} Bitcoin, {5} Ethereum, and {6} USDT".format(user_id, order_type_str, quantity, instrument_str, btc, eth, usdt))#CHANGE
    return user_id, order_type, instrument, quantity, btc, eth, usdt

#print(df_orderBook)
    

    




