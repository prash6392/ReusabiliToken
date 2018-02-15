"""@package ShopListOracle
Implementation of a simple shop list oracle
"""


class ShopListOracle(object):

    def __init__(self):
        self.shop_list = []

    def verify_shop(self, shop_address):
        if shop_address in self.shop_list:
            return True
        else:
            return False

    def register_new_shop(self, shop_address):
        if shop_address not in self.shop_list:
            self.shop_list.append(shop_address)
