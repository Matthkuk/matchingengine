class Transaction:
    def __init__(self, transaction_id, buyer_id, instrument, quantity, btc, eth, usdt, seller_id):
        self.transaction_id = transaction_id
        self.buyer_id = buyer_id
        self.instrument = instrument
        self.quantity = quantity
        self.btc = btc
        self.eth = eth
        self.usdt = usdt
        self.seller_id = seller_id