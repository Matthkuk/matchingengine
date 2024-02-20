class Order:
    def __init__(self, order_id, user_id, order_type, instrument, quantity, btc, eth, usdt):
        self.order_id = order_id
        self.user_id = user_id
        self.order_type = order_type
        self.instrument = instrument
        self.quantity = quantity
        self.btc = btc
        self.eth = eth
        self.usdt = usdt
    
'''class Order:
    def __init__(self, user_id, order_type, instrument, quantity, btc, eth, usdt):
        self.user_id = user_id
        self.order_type = order_type
        self.instrument = instrument
        self.quantity = quantity
        self.btc = btc
        self.eth = eth
        self.usdt = usdt'''