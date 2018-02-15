"""@package Customer
Implementation of a generic Customer
"""
from abc import ABCMeta, abstractmethod
import numpy as np


class Customer(object):
    __metaclass__ = ABCMeta
    CUSTOMER_ID = 0
    def __init__(self, type_):
        self.customer_id = Customer.CUSTOMER_ID
        Customer.CUSTOMER_ID += 1
        self.reputation = {}
        self.coins = 0
        self.recycle_prob = 0.9
        self.preferred_shop = -1
        self.type_ = type_

    def transfer_coin(self, coin_count):
        self.coins += coin_count

    def set_coin(self, coins):
        self.coins = coins

    def transfer_reputation(self, reputation, shop_address):
        if shop_address in self.reputation:
            self.reputation[shop_address]['reputation'] += reputation
        else:
            self.set_reputation(shop_address, reputation)

    def set_reputation(self, shop_address, reputation):
        self.reputation[shop_address] = {}
        self.reputation[shop_address]['reputation'] = reputation

    def get_address(self):
        return self.customer_id

    def choose_to_recycle(self):
        res = np.random.binomial(1, self.recycle_prob, 1)
        if res == 1:
            return True
        else:
            return False

    def choose_to_pay_by_coin(self):
        if self.coins > 10000:
                return True
        else:
            return False

    def get_coin_spend(self):
        return 10000

    def get_coin(self):
        return self.coins

    def get_reputation(self, shop_address):
        if shop_address in self.reputation:
            return self.reputation[shop_address]['reputation']
        else:
            return 0

    def get_type(self):
        return self.type_

    @abstractmethod
    def choose_shop(self, num_shops):
        pass


class GoodCustomer(Customer):

    def __init__(self):
        super(GoodCustomer, self).__init__('g')
        self.recycle_prob = 0.9

    def choose_shop(self, num_shops):
        if self.preferred_shop == -1:
            self.preferred_shop = np.random.randint(0, num_shops, 1)[0]

        return self.preferred_shop


class BadCustomer(Customer):

    def __init__(self):
        super(BadCustomer, self).__init__('b')
        self.recycle_prob = 0.1

    def choose_shop(self, num_shops):
        return np.random.randint(0, num_shops, 1)[0]


class NeutralCustomer(Customer):

    def __init__(self):
        super(NeutralCustomer, self).__init__('n')
        self.recycle_prob = 0.60
        self.preferred_shops = []
        self.preference_ratio = 0.30

    def choose_shop(self, num_shops):

        if len(self.preferred_shops) == 0:
            chosen_shops = np.random.choice(np.arange(num_shops), int(max(1, np.ceil(self.preference_ratio*num_shops))),
                                            replace=False)
            for shop in chosen_shops:
                self.preferred_shops.append(shop)

        # choose one of the preferred shops at random
        return np.random.choice(np.arange(len(self.preferred_shops)), 1, replace=False)[0]



