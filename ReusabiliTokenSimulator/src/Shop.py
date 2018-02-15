"""@package Shop
Implementation of a shop
"""


class Shop(object):

    SHOP_ID = 0
    def __init__(self):
        self.shop_id = Shop.SHOP_ID
        Shop.SHOP_ID += 1
        self.name = 'shop ' + str(self.shop_id)
        self.coin_count = 0

    def get_shop_address(self):
        return self.shop_id

    def get_coin_count(self):
        return self.coin_count

    def buy_with_coins(self, coins):
        self.coin_count += coins

    def pay_dues_to_smart_contract(self, smart_contract):
        smart_contract.make_payment(self.shop_id, self.coin_count)

