import pandas as pd
from order import Order
from input import Input
from transaction import Transaction

# buy = 1, sell = 0
# instrument, 1 = btccoin, 2 = ethereum, 3 = usdt


def orderBook_init():
    '''
    Initialise all the Input Queue, Orderbook, and Output Queue
    '''
    df_orderbook = pd.read_excel('orderbookdata\orderbook.xlsx')
    df_inputq = pd.DataFrame(columns=[
                             'input_id', 'user_id', 'order_type', 'instrument', 'quantity', 'btc', 'eth', 'usdt'])
    df_transaction = pd.DataFrame(columns=[
                                  'transaction_id', 'buyer_id', 'seller_id', 'instrument', 'quantity', 'btc', 'eth', 'usdt'])
    return df_orderbook, df_inputq, df_transaction


def new_order_orderbook(df_orderbook, user_id, order_type, instrument, quantity, btc, eth, usdt):
    '''
    Returns the orderbook after it adds a new order into the orderbook
    '''
    if (len(df_orderbook) >= 1):
        order_id = df_orderbook['order_id'].max() + 1
    else:
        order_id = 1
    new_order = pd.DataFrame(Order(order_id, user_id, order_type,
                             instrument, quantity, btc, eth, usdt).__dict__, index=[0])
    df_orderbook = pd.concat(
        [new_order, df_orderbook.loc[:]], ignore_index=True).sort_values('order_id')
    print('Output Queue:')
    print('Order successfully added to orderbook!\n')
    return df_orderbook


def edit_order_orderbook(df_orderbook, order_id, user_id, order_type, instrument, quantity, btc, eth, usdt):
    '''
    Returns the orderbook after it adds an edited order into the orderbook
    '''
    if (order_id is None):
        order_id = df_orderbook['order_id'].max() + 1

    order_id = order_id.values[0]

    new_order = pd.DataFrame(Order(order_id, user_id, order_type,
                             instrument, quantity, btc, eth, usdt).__dict__, index=[0])
    df_orderbook = pd.concat(
        [new_order, df_orderbook.loc[:]], ignore_index=True).sort_values('order_id')
    print('Output Queue:')
    print('Order successfully added to orderbook!\n')
    return df_orderbook


def delete_order_orderbook(df_orderbook, found_match_id):
    '''
    Returns the orderbook after it deletes an order for the orderbook based on inputted parameter
    '''
    try:
        found_match_id = found_match_id.values[0]
    except AttributeError:
        pass
    df_orderbook.drop(
        df_orderbook[df_orderbook['order_id'] == found_match_id].index, inplace=True)
    return df_orderbook


def new_order_inputq(df_inputq, user_id, order_type, instrument, quantity, btc, eth, usdt):
    '''
    Returns the input queue after it adds an order into the input queue
    '''
    if (len(df_inputq) >= 1):
        input_id = df_inputq['input_id'].max() + 1
    else:
        input_id = 1
    new_input = pd.DataFrame(Input(input_id, user_id, order_type,
                             instrument, quantity, btc, eth, usdt).__dict__, index=[0])
    df_inputq = pd.concat([new_input, df_inputq.loc[:]], ignore_index=True)
    return df_inputq


def delete_last_order(df_inputq):
    '''
    Deletes the oldest order in the orderbook
    '''
    df_delete_row = df_inputq.iloc[:-1, :]
    return df_delete_row


def pop_inputq(df_inputq):
    '''
    Returns the oldest entry in the databook
    '''
    popped_row = df_inputq.values[-1:]
    popped_row = pd.DataFrame(popped_row, columns=[
                              'input_id', 'user_id', 'order_type', 'instrument', 'quantity', 'btc', 'eth', 'usdt'])
    return popped_row


def get_user_order(df_orderbook, user_id):
    '''
    Returns all the orders of a specified user ID
    '''
    user_orderbook = df_orderbook[df_orderbook['user_id'] == user_id]
    return user_orderbook


def get_instrument_orderbook(df_orderbook, instrument):
    '''
    Return all the orders of a specified instrument
    '''
    df_instrument_orderbook = df_orderbook[df_orderbook['instrument'] == instrument]
    return df_instrument_orderbook


def find_match(df_orderbook, user_id, order_type, instrument, quantity, btc, eth, usdt):
    '''
    Returns the first matching order of the entered in parameters from the orderbook
    Returns None if no match is found
    '''
    if order_type == 1:
        look_for_order_type = 0
    elif order_type == 0:
        look_for_order_type = 1

    for i in range(len(df_orderbook)):
        matching_orders = df_orderbook.values[i]
        matching_orders = pd.DataFrame([matching_orders], columns=[
                                       'order_id', 'user_id', 'order_type', 'instrument', 'quantity', 'btc', 'eth', 'usdt'])

        if ((matching_orders['order_type'] == look_for_order_type) & (matching_orders['instrument'] == instrument)).any() == True:
            if look_for_order_type == 0:
                if instrument == 1:
                    if ((matching_orders['eth'] <= eth) | (matching_orders['usdt'] <= usdt)).any() == True:
                        return matching_orders
                elif instrument == 2:
                    if ((matching_orders['btc'] <= btc) | (matching_orders['usdt'] <= usdt)).any() == True:
                        return matching_orders
                elif instrument == 3:
                    if ((matching_orders['btc'] <= btc) | (matching_orders['eth'] <= eth)).any() == True:
                        return matching_orders
            elif look_for_order_type == 1:
                if instrument == 1:
                    if ((matching_orders['eth'] >= eth) | (matching_orders['usdt'] >= usdt)).any() == True:
                        return matching_orders
                elif instrument == 2:
                    if ((matching_orders['btc'] >= btc) | (matching_orders['usdt'] >= usdt)).any() == True:
                        return matching_orders
                elif instrument == 3:
                    if ((matching_orders['btc'] >= btc) | (matching_orders['eth'] >= eth)).any() == True:
                        return matching_orders


def transaction(new_match, found_match):
    '''
    Returns the parameters for a completed transaction
    '''
    new_match = new_match.reset_index(drop=True)
    found_match = found_match.reset_index(drop=True)
    if (new_match['quantity'] > found_match['quantity']).any() == True:
        quantity = found_match['quantity'].values[0]
    elif (new_match['quantity'] < found_match['quantity']).any() == True:
        quantity = new_match['quantity'].values[0]
    elif (new_match['quantity'] == found_match['quantity']).any() == True:
        quantity = found_match['quantity'].values[0]

    if (new_match['order_type'] == 1).any() == True:
        buyer_id = new_match['user_id'].values[0]
        instrument = new_match['instrument'].values[0]
        seller_id = found_match['user_id'].values[0]
        if (new_match['instrument'] == 1).any() == True:
            if (new_match['eth'] >= found_match['eth']).any() == True:
                eth = found_match['eth'].values[0]
                btc = None
                usdt = None
            elif (new_match['usdt'] >= found_match['usdt']).any() == True:
                usdt = found_match['usdt'].values[0]
                btc = None
                eth = None
        elif (new_match['instrument'] == 2).any() == True:
            if (new_match['btc'] >= found_match['btc']).any() == True:
                btc = found_match['btc']
                eth = None
                usdt = None
            elif (new_match['usdt'] >= found_match['usdt']).any() == True:
                usdt = found_match['usdt'].values[0]
                btc = None
                eth = None
        elif (new_match['instrument'] == 3).any() == True:
            if (new_match['eth'] >= found_match['eth']).any() == True:
                eth = found_match['eth'].values[0]
                btc = None
                usdt = None
            elif (new_match['btc'] >= found_match['btc']).any() == True:
                btc = found_match['btc'].values[0]
                usdt = None
                eth = None
    elif (new_match['order_type'] == 0).any() == True:
        buyer_id = found_match['user_id'].values[0]
        instrument = new_match['instrument'].values[0]
        seller_id = new_match['user_id'].values[0]
        if (new_match['instrument'] == 1).any() == True:
            if (new_match['eth'] <= found_match['eth']).any() == True:
                eth = new_match['eth'].values[0]
                btc = None
                usdt = None
            elif (new_match['usdt'] <= found_match['usdt']).any() == True:
                usdt = new_match['usdt'].values[0]
                btc = None
                eth = None
        elif (new_match['instrument'] == 2).any() == True:
            if (new_match['btc'] <= found_match['btc']).any() == True:
                btc = new_match['btc'].values[0]
                eth = None
                usdt = None
            elif (new_match['usdt'] <= found_match['usdt']).any() == True:
                usdt = new_match['usdt'].values[0]
                btc = None
                eth = None
        elif (new_match['instrument'] == 3).any() == True:
            if (new_match['eth'] <= found_match['eth']).any() == True:
                eth = new_match['eth'].values[0]
                btc = None
                usdt = None
            elif (new_match['btc'] <= found_match['btc']).any() == True:
                btc = new_match['btc'].values[0]
                usdt = None
                eth = None
    return buyer_id, instrument, quantity, btc, eth, usdt, seller_id


def edit_after_transaction(new_match, found_match):
    '''
    Returns an edited version of the resulting order after one or both orders are fulfilled
    If existing order is fulfilled return the resulting order with the no order ID
    If new order is fulfilled return the resulting order with the corresponding order ID
    If both are fulfilled return None to signify that everything is fulfilled
    '''
    new_match = new_match.reset_index(drop=True)
    found_match = found_match.reset_index(drop=True)
    if (new_match['quantity'] > found_match['quantity']).any():
        new_quantity = (new_match['quantity'] - found_match['quantity'])
        edited_match = pd.DataFrame(Order(None, new_match['user_id'], new_match['order_type'], new_match['instrument'],
                                          new_quantity, new_match['btc'], new_match['eth'], new_match['usdt']).__dict__, index=[0])
        return edited_match
    elif (new_match['quantity'] < found_match['quantity']).any():
        new_quantity = (found_match['quantity'] - new_match['quantity'])
        edited_match = pd.DataFrame(Order(found_match['order_id'], found_match['user_id'], found_match['order_type'], found_match['instrument'],
                                          new_quantity, found_match['btc'], found_match['eth'], found_match['usdt']).__dict__, index=[0])
        return edited_match
    elif (new_match['quantity'] == found_match['quantity']).any():
        return None


def output_dataframe(df_transaction, buyer_id, instrument, quantity, btc, eth, usdt, seller_id):
    '''
    Returns a dataframe containing all completed transactions
    '''
    if (df_transaction['transaction_id'] >= 1).any():
        transaction_id = df_transaction['transaction_id'].max() + 1
    else:
        transaction_id = 1
    new_transaction = pd.DataFrame(Transaction(
        transaction_id, buyer_id, instrument, quantity, btc, eth, usdt, seller_id).__dict__, index=[0])
    df_transaction = pd.concat(
        [new_transaction, df_transaction.loc[:]], ignore_index=True).sort_values('transaction_id')
    if instrument == 1:
        instrument = 'BTC'
    elif instrument == 2:
        instrument = 'ETH'
    elif instrument == 3:
        instrument = 'USDT'

    try:
        usdt = usdt.values[0]
    except AttributeError:
        pass
    try:
        btc = btc.values[0]
    except AttributeError:
        pass
    try:
        eth = eth.values[0]
    except AttributeError:
        pass

    if usdt is not None:
        price_per_unit = usdt
        price = f'{usdt} USDT'
    elif btc is not None:
        price_per_unit = btc
        price = f'{btc} BTC'
    else:
        price_per_unit = eth
        price = f'{eth} ETH'

    try:
        price_per_unit = price_per_unit.values[0]
    except AttributeError:
        pass

    try:
        quantity = quantity.values[0]
    except AttributeError:
        pass

    print('Output Queue:')
    print(f"Transaction ID = {transaction_id}: User {buyer_id} bought {quantity} {instrument} for {price} per unit (Total: {round(price_per_unit * quantity, 2)}) from User {seller_id}\n")
    return df_transaction


def match_sequence(df_orderBook, df_transaction, popped_row):
    '''
    Matching Engine
    Returns the updated orderbook and output queue after it runs all the required matching engine functions
    '''
    if (popped_row is None):
        return df_orderBook, df_transaction, -1
    found_match = find_match(df_orderBook, popped_row[popped_row.columns[0]], popped_row["order_type"].values[0], popped_row["instrument"].values[0],
                             popped_row["quantity"].values[0], popped_row["btc"].values[0], popped_row["eth"].values[0], popped_row["usdt"].values[0])
    if found_match is not None:
        buyer_id, instrument, quantity, btc, eth, usdt, seller_id = transaction(
            popped_row, found_match)
        edited_order = edit_after_transaction(popped_row, found_match)
        df_orderBook = delete_order_orderbook(
            df_orderBook, found_match['order_id'])
        df_transaction = output_dataframe(
            df_transaction, buyer_id, instrument, quantity, btc, eth, usdt, seller_id)
        df_orderBook, df_transaction, flag = match_sequence(
            df_orderBook, df_transaction, edited_order)
        if (flag == -1):
            return df_orderBook, df_transaction, -1
        df_orderBook = edit_order_orderbook(df_orderBook, edited_order["order_id"], edited_order["user_id"], edited_order["order_type"],
                                            edited_order["instrument"], edited_order["quantity"], edited_order["btc"], edited_order["eth"], edited_order["usdt"])
    else:
        df_orderBook = new_order_orderbook(df_orderBook, popped_row['user_id'], popped_row["order_type"],
                                           popped_row["instrument"], popped_row["quantity"], popped_row["btc"], popped_row["eth"], popped_row["usdt"])
        return df_orderBook, df_transaction, -1

    return df_orderBook, df_transaction, -1
