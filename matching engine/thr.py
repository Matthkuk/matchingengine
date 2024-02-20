from threading import *
from functions import *
from simulation import generate
import time
#from run import match_sequence

'''global df_orderbook
global df_inputq
global df_transaction'''

# initialize all dataframes
df_orderbook, df_inputq, df_transaction = orderBook_init()

# number of orders to be generated
max_order_count = 100

user_count = 10  # must be 1 or above

max_quantity = 50  # max quantity a user can buy or sell in a single order

# declare a semaphore (lock)
lock = Semaphore(1)

# thread function to generate orders


def generate_thread():
    '''
    A thread function to generate an order using generate() and then input the generated values into the input queue
    '''
    for i in range(max_order_count):
        lock.acquire()

        user_id, order_type, instrument, quantity, btc, eth, usdt = generate(
            user_count, max_quantity)
        global df_inputq
        df_inputq = new_order_inputq(
            df_inputq, user_id, order_type, instrument, quantity, btc, eth, usdt)

        lock.release()

        # before generating the next, let matching run at least once
        time.sleep(0.1)

# thread function for matching engine


def match_thread():
    '''
    A thread function that takes the oldest order from the input queue, and puts it into the matching engine. 
    '''
    global df_inputq
    global df_transaction
    global df_orderbook
    time.sleep(0.1)  # before start, allow for input queue to fill up
    # while input queue is not empty
    while (len(df_inputq) != 0):

        lock.acquire()

        popped_row = pop_inputq(df_inputq)
        df_inputq = delete_last_order(df_inputq)

        df_orderbook, df_transaction, flag = match_sequence(
            df_orderbook, df_transaction, popped_row)

        lock.release()
        time.sleep(0.1)  # let time to fill up queue


t1 = Thread(target=generate_thread)
t2 = Thread(target=match_thread)

t1.start()
t2.start()
t1.join()
t2.join()

print('Orderbook:')
print(df_orderbook)
print('For full information check the folder orderbookdata\simul_orderbook.xlsx\n')
print('Transaction book:')
print(df_transaction)
print('For full information check the folder orderbookdata\simul_transactions.xlsx\n')

df_orderbook.to_excel('orderbookdata\simul_orderbook.xlsx', index=False)
df_transaction.to_excel('orderbookdata\simul_transactions.xlsx', index=False)
