"""@package Visualization
Implementation of a few visualizers
"""
import matplotlib.pyplot as plt
import numpy as np


def visualize_function(values, name, color, ax=None):
    if ax is None:
        f = plt.figure()
        ax = f.add_subplot(1, 1, 1)
    ax.plot(values, c=color)
    ax.set_title(name)
    ax.grid(True)
    return ax


def visualize_market(smart_contract, customer_list, shop_list, ax_cus=None, ax_shop=None, ax_cp=None, ax_ca=None):
    if ax_cus is None or ax_shop is None:
        f = plt.figure()
        ax_cus = f.add_subplot(2, 2, 1)
        ax_shop = f.add_subplot(2, 2, 2)
        ax_cp = f.add_subplot(2, 2, 3)
        ax_ca = f.add_subplot(2, 2, 4)
    ax_cus.set_title('customer reputation')
    ax_cus.grid(True)
    ax_shop.set_title('shop reputation')
    ax_shop.grid(True)
    ax_cp.set_title('coin purchases')
    ax_cp.grid(True)
    ax_ca.set_title('coins re-collected at shops')
    ax_ca.grid(True)
    cus_reps = []
    shop_reps = []
    for customer in customer_list:
        cus_reps.append(smart_contract.calculate_customer_reputation(customer.get_address()))

    for shop in shop_list:
        shop_reps.append(smart_contract.calculate_shop_reputation(shop.get_shop_address()))

    cp_map = smart_contract.get_coin_purchase_map()
    coin_purchases = np.zeros(len(customer_list))
    for customer in cp_map:
        coin_purchases[customer] = cp_map[customer]

    coins_collected_in_shops = [shop.get_coin_count() for shop in shop_list]

    ax_cus.bar(np.arange(len(customer_list)), cus_reps, color='red')
    ax_shop.bar(np.arange(len(shop_list)), shop_reps, color='blue')
    ax_cp.bar(np.arange(len(customer_list)), coin_purchases, color='green')
    ax_ca.bar(np.arange(len(shop_list)), coins_collected_in_shops, color='magenta')
    plt.tight_layout()
    return ax_cus, ax_shop, ax_cp, ax_ca


def diminishing_returns(max_val, b1, num_samples=100):
    x = np.arange(0, num_samples)
    return max_val - np.exp(np.log(max_val) - b1*x)



