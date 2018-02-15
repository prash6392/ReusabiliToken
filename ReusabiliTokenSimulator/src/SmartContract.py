"""@package SmartContract
Implementation of a smart contract
"""
import numpy as np


class SmartContract(object):

    def __init__(self, owner_address):
        self.coin_map = {}
        self.reputation_map = {}
        self.shop_coin_map = {}
        self.cus_buys_with_coin_map = {}
        self.status = 'ready'
        self.current_customer_address = -1
        self.current_shop_address = -1
        self.owner_address = owner_address
        self.shop_oracle = None
        self.time_oracle = None
        self.known_shops = []
        self.black_listed_shops = []
        self.shop_payment_times = {}
        # some default values
        self.reputation_limit = 100
        self.coin_limit = 100
        self.coins_per_reputation_token = 1
        self.payment_due_date = 30

    def set_oracle(self, sender_address, shop_oracle, time_oracle):
        if sender_address == self.owner_address:
            self.shop_oracle = shop_oracle
            self.time_oracle = time_oracle

    def set_coin_limit(self, sender_address, coin_limit):
        if self.owner_address == sender_address:
            self.coin_limit = coin_limit

    def set_reputation_limit(self, sender_address, reputation_limit):
        if self.owner_address == sender_address:
            self.reputation_limit = reputation_limit

    def set_coins_per_reputation_token(self, sender_address, factor):
        if self.owner_address == sender_address:
            self.coins_per_reputation_token = factor

    def set_payment_duration(self, sender_address, duration):
        if self.owner_address == sender_address:
            self.payment_due_date = duration

    def check_payments(self, sender_address, current_time):
        if sender_address != self.owner_address:
            return False

        for shop_address in self.known_shops:
            if self.shop_payment_times[shop_address] - current_time >= self.payment_due_date:
                if shop_address not in self.black_listed_shops:
                    self.black_listed_shops.append(shop_address)

    def make_payment(self, shop_address, payment):
        if shop_address not in self.known_shops:
            return False

        payment_due = self.calculate_shop_reputation(shop_address)

        # Yeah, one technically needs to take care of multiple payments, additional payments, etc.
        # Not taking into account all of that now.
        if payment < payment_due:
            return False

        if self.time_oracle is not None:
            payment_time = self.time_oracle.get_time()
            self.shop_payment_times[shop_address] = payment_time

    def make_claim(self, shop_address, customer_address):
        if self.status != 'ready':
            return False
        self.status = 'pending'
        self.current_customer_address = customer_address
        self.current_shop_address = shop_address
        return True

    def verify_claim(self, shop_address, customer_address):
        if self.status != 'pending':
            return False, -1, -1

        # verify if the shop_address is indeed a valid shop by asking an Oracle
        if self.shop_oracle is None:
            self.status = 'ready'
            return False, -1, -1

        if shop_address not in self.known_shops:
            if (self.shop_oracle.verify_shop(shop_address=shop_address)) is False:
                self.status = 'ready'
                return False, -1, -1
            else:
                self.known_shops.append(shop_address)

        if shop_address in self.black_listed_shops:
            self.status = 'ready'
            return False, -1, -1

        # check if this verification matches a previous customer claim
        if self.current_customer_address == customer_address and self.current_shop_address == shop_address:
            self.status = 'ready'

            # get customer reputation
            customer_rep = 0
            if self.reputation_map.has_key(customer_address):
                if self.reputation_map[customer_address].has_key(shop_address):
                    customer_rep = self.reputation_map[customer_address][shop_address]
            # calculate the number of coins to issue
            new_coins = self._calculate_new_coins_for_customer(customer_rep)
            new_rep = self._calculate_reputation_for_customer(customer_rep)
            # transfer coins and reputation to the customer
            if self.coin_map.has_key(customer_address):
                if self.coin_map[customer_address].has_key(shop_address):
                    if self.coin_map[customer_address][shop_address] >= self.coin_limit:
                        self.coin_map[customer_address][shop_address] = self.coin_limit
                    else:
                        self.coin_map[customer_address][shop_address] += new_coins
                else:
                    self.coin_map[customer_address][shop_address] = new_coins
            else:
                self.coin_map[customer_address] = {}
                self.coin_map[customer_address][shop_address] = new_coins

            if self.reputation_map.has_key(customer_address):
                if self.reputation_map[customer_address].has_key(shop_address):
                    if self.reputation_map[customer_address][shop_address] >= self.reputation_limit:
                        self.reputation_map[customer_address][shop_address] = self.reputation_limit
                    else:
                        self.reputation_map[customer_address][shop_address] += new_rep
                else:
                    self.reputation_map[customer_address][shop_address] = new_rep
            else:
                self.reputation_map[customer_address] = {}
                self.reputation_map[customer_address][shop_address] = new_rep

            if not self.shop_payment_times.has_key(shop_address):
                self.shop_payment_times[shop_address] = self.time_oracle.get_time()

            return True, new_coins, new_rep

        return False, -1, -1

    def customer_buys_with_coin(self, customer_address, shop_address, num_coins):
        self.coin_map[customer_address][shop_address] -= num_coins
        if self.shop_coin_map.has_key(shop_address):
            self.shop_coin_map[shop_address] += num_coins
        else:
            self.shop_coin_map[shop_address] = num_coins

        if self.cus_buys_with_coin_map.has_key(customer_address):
            self.cus_buys_with_coin_map[customer_address] += 1
        else:
            self.cus_buys_with_coin_map[customer_address] = 1

    def _calculate_new_coins_for_customer(self, customer_reputation):
        new_coins = customer_reputation*self.coins_per_reputation_token
        # diminishing returns functions
        new_coins = self.coin_limit - np.exp(np.log(self.coin_limit) - 0.1*new_coins)
        return new_coins

    def _calculate_reputation_for_customer(self, customer_reputation):
        new_rep = customer_reputation+1
        new_rep = self.reputation_limit - np.exp(np.log(self.reputation_limit) - 0.1*new_rep)
        return new_rep

    def calculate_shop_reputation(self, shop_address):
        reputation = 0
        for customer in self.reputation_map:
            for iter_shops in self.reputation_map[customer]:
                if iter_shops == shop_address:
                     reputation += self.reputation_map[customer][shop_address]
        return reputation

    def calculate_customer_reputation(self, customer_address):
        reputation = 0
        if self.reputation_map.has_key(customer_address):
            for iter_shops in self.reputation_map[customer_address]:
                reputation += self.reputation_map[customer_address][iter_shops]
        return reputation

    def valid_shops_left(self, shop_addresses):
        if len(self.black_listed_shops) == len(shop_addresses):
            return False
        else:
            return True

    def get_coin_map(self):
        return self.coin_map

    def get_reputation_map(self):
        return self.reputation_map

    def get_coin_purchase_map(self):
        return self.cus_buys_with_coin_map

