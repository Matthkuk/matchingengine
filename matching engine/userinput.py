from functions import *

df_orderbook, df_inputq, df_transaction = orderBook_init()


def isfloat(num):
    '''
    Check if number is float
    '''
    try:
        float(num)
        return True
    except ValueError:
        return False


def userID_loop():
    # user id loop
    '''
    Manage the user input for user ID
    '''
    while (True):
        user_id = str(input("Enter your User ID (Numbers)\n")).replace(" ", "")

        if len(user_id) <= 8 and user_id.isnumeric():
            return user_id

        print("Invalid Input, please retry.")


def instrument_loop(order_type_str=None):
    # instrument loop, input can be bitcoin, bit, btc, ethereum, eth, or usdt
    '''
    Manage the user input for instrument selection. Input can be bitcoin, bit, btc, ethereum, eth, or usdt
    '''
    while (True):
        if order_type_str is not None:
            instrument_str = str(input('What instrument are you ' + order_type_str +
                                 'ing? (Enter "Bitcoin", "Ethereum", or "USDT")\n').replace(" ", ""))

        else:
            instrument_str = str(input(
                'Which instrument do you want to filter by? (Enter "Bitcoin", "Ethereum", or "USDT")').replace(" ", ""))

        instrument_str = instrument_str.lower()
        if (instrument_str == "bitcoin" or instrument_str == "bit" or instrument_str == "btc" or instrument_str == "1"):
            return 1
        elif (instrument_str == "ethereum" or instrument_str == "eth" or instrument_str == "2"):
            return 2
        elif (instrument_str == "usdt" or instrument_str == "3"):
            return 3
        else:
            print("Invalid Input, please retry.")
            continue


def add_order_loop():
    '''
    A function that prompts users to enter all information necessary to add an order.
    '''
    # user_id loop
    user_id = userID_loop()

    # order type loop, input has to be saying "buy" or "sell", caps dont matter
    while (True):
        order_type_str = str(
            input('Are you Buying or Selling? (Enter "Buy" or "Sell")\n').replace(" ", ""))

        order_type_str = order_type_str.lower()

        if (order_type_str == "buy" or order_type_str == "1"):
            order_type = 1
            order_type_str = "buy"
            break
        elif (order_type_str == "sell" or order_type_str == "0"):
            order_type = 0
            order_type_str = "sell"
            break
        else:
            print("Invalid Input, please retry.")
            continue

    # instrument loop
    instrument = instrument_loop(order_type_str)

    # quantity loop, must be number
    while (True):
        quantity = input('How much are you ' + order_type_str +
                         'ing? (Enter numbers)\n').replace(" ", "")
        if not quantity.isnumeric():
            print("Invalid Input, please retry.")
            continue
        quantity = int(quantity)
        break

    btc = eth = usdt = None  # initialize to null
    # price loop
    while (True):
        if not instrument == 1:
            btc = input(
                "How much Bitcoin do you want for it? (Per unit)\n").replace(" ", "")
            if not isfloat(btc):
                print("Invalid Input, please retry.")
                continue
            btc = float(btc)
        if not instrument == 2:
            eth = input(
                "How much Ethereum do you want for it? (Per unit)\n").replace(" ", "")
            if not isfloat(eth):
                print("Invalid Input, please retry.")
                continue
            eth = float(eth)
        if not instrument == 3:
            usdt = input(
                "How much USDT do you want for it? (Per unit)\n").replace(" ", "")
            if not isfloat(usdt):
                print("Invalid Input, please retry.")
                continue
            usdt = float(usdt)
        break

    return user_id, order_type, instrument, quantity, btc, eth, usdt


# loops for manual input
def prompt_user_action(df_orderbook, df_transaction):
    # prompt user action
    '''
    Asks the user if he wants to add or delete an order. image.png
    '''
    while (True):
        action = input('Do you want to input or delete an order? (Enter "Order" or "Delete")\nTo retrieve current orderbook for a specific instrument, enter "2"\nTo retrieve executed trades for a specific instrument, enter "3"\n(To exit, enter "-1")')
        action = action.lower()
        if action == "delete" or action == "0":

            user_id = userID_loop()
            filtered_orderbook = get_user_order(df_orderbook, int(user_id))
            print(filtered_orderbook)

            row = 0
            while row == 0:
                order_id = int(
                    input('Which order ID would you like to delete? ("Enter "-1" to go back)'))
                if row == -1:
                    return 0

                if (filtered_orderbook['order_id'] == order_id).any() == True:
                    break
                else:
                    row = 0
                    print("Invalid order ID entered.")

            df_orderbook = delete_order_orderbook(df_orderbook, order_id)
            print("Order ID: " + str(order_id) +
                  " has been removed.\nPrinting updated orderbook.")
            print(df_orderbook)
            pass
        elif action == "order" or action == "1":
            return 1
        # get filtered orderbook by instrument
        elif action == "2":

            # prompt user for instrument
            instrument = instrument_loop()

            filtered_orderbook = get_instrument_orderbook(
                df_orderbook, instrument)
            if len(filtered_orderbook) == 0:
                print('No orders found for this instrument\n')
            else:
                print(filtered_orderbook)
        elif action == "3":
            instrument = instrument_loop()
            filtered_orderbook = get_instrument_orderbook(
                df_transaction, instrument)
            if len(filtered_orderbook) == 0:
                print('No transaction found for this instrument\n')
            else:
                print(filtered_orderbook)
        elif action == "-1":
            return -1
        else:
            print("Invalid Input, please retry")
            continue
        break


def main(df_orderbook, df_transaction, df_inputq):
    '''
    Main function for manual input
    '''
    while (True):
        result = prompt_user_action(df_orderbook, df_transaction)
        if (result == 1):

            user_id, order_type, instrument, quantity, btc, eth, usdt = add_order_loop()

            df_inputq = new_order_inputq(
                df_inputq, user_id, order_type, instrument, quantity, btc, eth, usdt)

            popped_row = pop_inputq(df_inputq)
            df_inputq = delete_last_order(df_inputq)

            df_orderbook, df_transaction, flag = match_sequence(
                df_orderbook, df_transaction, popped_row)

            print('Orderbook:')
            print(df_orderbook)
            print('\n')
            print('Transaction book:')
            print(df_transaction)
            print('\n')

            while (True):

                i = input("Do you want to continue? (y/n)")
                i = i.lower()
                if i == "y":
                    pass
                elif i == "n":
                    exit()
                else:
                    print("Invalid Input, please retry")
                    continue
                break
        elif (result == -1):
            exit()


main(df_orderbook, df_transaction, df_inputq)
