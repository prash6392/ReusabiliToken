"""@package SimulationEngine
Implementation of a simulation Engine
"""
from Customer import GoodCustomer, BadCustomer, NeutralCustomer
from Shop import Shop
from ShopListOracle import ShopListOracle
from SmartContract import SmartContract
from SimulationTimeOracle import SimulationTimeOracle
import numpy as np
from Visualization import visualize_market
import matplotlib.pyplot as plt


class SimulationEngine(object):
    def __init__(self, num_customers, num_shops, sim_iters, coin_limit, rep_limit, coin_rep_factor, payment_due):
        self.num_customers = num_customers
        self.num_shops = num_shops
        self.sim_iters = sim_iters
        self.customers = self._create_customers([0.3, 0.1, 0.6])
        self.shops = self._create_shops()
        self.time_oracle = SimulationTimeOracle()
        self.shop_list_oracle = ShopListOracle()
        for shop in self.shops:
            self.shop_list_oracle.register_new_shop(shop.get_shop_address())
        self.address = np.random.randint(200000, 3300000, 1)
        self.smart_contract = SmartContract(self.address[0])
        self.smart_contract.set_oracle(self.address, self.shop_list_oracle, self.time_oracle)
        self.smart_contract.set_coin_limit(self.address, coin_limit)
        self.coin_limit = coin_limit
        self.smart_contract.set_reputation_limit(self.address, rep_limit)
        self.rep_limit = rep_limit
        self.smart_contract.set_payment_duration(self.address, payment_due)
        self.payment_due = payment_due
        self.smart_contract.set_coins_per_reputation_token(self.address, coin_rep_factor)
        self.coin_rep_factor = coin_rep_factor

    def run(self, claim_failure_probability=0.00001):
        shop_addresses = [shop.get_shop_address() for shop in self.shops]
        ax = [None, None, None, None]
        plt.ion()
        for day in range(self.sim_iters):
            self.time_oracle.increment_time()

            # check if there are any valid shops left in the smart contract
            if self.smart_contract.valid_shops_left(shop_addresses) is False:
                print('\n' + '*' * 15 + '\n')
                print('Tough luck. No shop earned enough coin to pay their dues.')
                print('The experiment ran for {} days.'.format(day))
                print('\n' + '*' * 15 + '\n')
                return

            # for every customer, choose a shop
            for customer in self.customers:
                chosen_shop = customer.choose_shop(self.num_shops)
                shop_address = self.shops[chosen_shop].get_shop_address()
                # choose whether the customer wants to pay by coin
                buy_with_coins = customer.choose_to_pay_by_coin()
                if buy_with_coins is True:
                    # notify the smart contract
                    self.smart_contract.customer_buys_with_coin(customer.get_address(),
                                                                shop_address,
                                                                customer.get_coin_spend())
                    self.shops[chosen_shop].buy_with_coins(customer.get_coin_spend())

                # for every decision, choose if a recycle happens
                recyling_decision = customer.choose_to_recycle()

                if recyling_decision is True:
                    self.smart_contract.make_claim(shop_address, customer.get_address())

                    if self._simulate_claim_failure(prob=claim_failure_probability):
                        # simulate a failure by verifying with our own address
                        self.smart_contract.verify_claim(self.address, customer.get_address())
                        print('claim failed')
                    else:
                        res, coins, reps = self.smart_contract.verify_claim(shop_address, customer.get_address())
                        if res is True:
                            customer.transfer_coin(coins)

                            if customer.get_reputation(shop_address) > self.smart_contract.reputation_limit:
                                customer.set_reputation(shop_address, self.smart_contract.reputation_limit)
                            else:
                                customer.transfer_reputation(reps, shop_address)

            if day != 0 and np.mod(day, self.payment_due):
                for shop in self.shops:
                    shop.pay_dues_to_smart_contract(self.smart_contract)

                self.smart_contract.check_payments(self.address, day)

            # deteriorate customer reputation at every simulation step
            self.smart_contract.deteriorate_customer_reputation(self.address, value=30.0)

            # visualize the market at every time step
            ax = visualize_market(self.smart_contract, self.customers, self.shops, ax[0], ax[1], ax[2], ax[3])
            plt.suptitle('Market after {} days'.format(day))
            plt.pause(0.05)
            plt.show()

        print('\n' + '*' * 15 + '\n')
        print('Customers recycled their goods and shops paid their dues.')
        print('The experiment ran successfully for {} days.'.format(self.sim_iters))
        print('\n' + '*' * 15 + '\n')

    def _create_customers(self, customer_distribution):
        customers = []
        gc = 0
        bc = 0
        nc = 0
        for i in range(self.num_customers):
            # choose the type of customer to create
            customer_type = np.argmax(np.random.multinomial(1, customer_distribution, 1))
            if customer_type == 0:
                customers.append(GoodCustomer())
                gc += 1
            elif customer_type == 1:
                customers.append(BadCustomer())
                bc += 1
            else:
                customers.append(NeutralCustomer())
                nc += 1
        print('gc: {}\tbc: {}\tnc: {}'.format(gc, bc, nc))
        return customers

    def _create_shops(self):
        shops = []
        for i in range(self.num_shops):
            shops.append(Shop())
        return shops

    def _simulate_claim_failure(self, prob):
        res = np.random.binomial(1, prob, 1)[0]
        if res == 1:
            return True
        else:
            return False


