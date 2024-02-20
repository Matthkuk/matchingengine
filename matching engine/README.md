Manual Input:
Manual Input with different values can be prompted by running the userinput.py file. The functions capable in manual control are delete/cancelling an existing order, adding a specific order, retrieving the orderbook for a specific instrument, and retrieving the executed trades for a specific instrument. The instructions for what to enter, the format, and etc are outlined in the prompts in the terminal. The terminal will print the messages in the output queue as well as additional relevant information. After an action, the system will prompt if you would like to continue or not; continuing will continue the current orderbook and any changes made; stopping the session will revert all changes and restore the orderbook to its starting state.

Simulation mode:
To run a simulation of different users and a large number of orders, run the thr.py file. This file will simultaneously start the generation of orders and matching engine. The parameters for generating users can be changed in thr.py 'max_order_count, user_count, max_quantity' The orders will go into the input queue and will be matched accordingly with outputs outputted into the output queue. The final orderbook and transaction book will be printed, but more information can be found in the orderbookdata\simul_orderbook.xlsx and orderbookdata\simul_transactions.xlsx files respectively.

Pre-requisites to download:
pandas
random
threading
time