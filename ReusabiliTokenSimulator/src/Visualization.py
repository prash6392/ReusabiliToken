"""@package Visualization
Implementation of a few visualizers
"""
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.cm as cm


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

    cus_reps = []
    shop_reps = []
    customer_colors = []
    for c in customer_list:
        if c.get_type() == 'g':
            customer_colors.append('green')
        if c.get_type() == 'b':
            customer_colors.append('red')
        if c.get_type() == 'n':
            customer_colors.append('yellow')

    ax_cus.set_title('customer reputation')
    ax_cus.grid(True)
    cus_labels = ['c' + str(i) for i in range(len(customer_list))]
    ax_cus.set_xticklabels(cus_labels)
    for xtick, color in zip(ax_cus.get_xticklabels(), customer_colors):
        xtick.set_color(color)
    ax_cus.set_xticks(np.arange(len(customer_list)))
    ax_cus.set_ylim(0, smart_contract.reputation_limit+100)
    ax_shop.set_title('shop reputation')
    ax_shop.grid(True)
    shop_labels = ['s' + str(i) for i in range(len(shop_list))]
    ax_shop.set_xticklabels(shop_labels)
    ax_shop.set_xticks(np.arange(len(shop_list)))
    ax_cp.set_title('coin purchases')
    ax_cp.grid(True)
    ax_cp.set_xticklabels(cus_labels)
    for xtick, color in zip(ax_cp.get_xticklabels(), customer_colors):
        xtick.set_color(color)
    ax_cp.set_xticks(np.arange(len(customer_list)))
    ax_ca.set_title('coins re-collected at shops')
    ax_ca.grid(True)
    ax_ca.set_xticklabels(shop_labels)
    ax_ca.set_xticks(np.arange(len(shop_list)))

    for customer in customer_list:
        cus_reps.append(smart_contract.calculate_customer_reputation(customer.get_address()))

    for shop in shop_list:
        shop_reps.append(smart_contract.calculate_shop_reputation(shop.get_shop_address()))

    cp_map = smart_contract.get_coin_purchase_map()
    coin_purchases = np.zeros(len(customer_list))
    for customer in cp_map:
        coin_purchases[customer] = cp_map[customer]

    coins_collected_in_shops = [shop.get_coin_count() for shop in shop_list]

    ax_cus.bar(np.arange(len(customer_list)), cus_reps, color=customer_colors)
    ax_shop.bar(np.arange(len(shop_list)), shop_reps, color='blue')
    ax_cp.bar(np.arange(len(customer_list)), coin_purchases, color=customer_colors)
    ax_ca.bar(np.arange(len(shop_list)), coins_collected_in_shops, color='magenta')
    plt.tight_layout()
    return ax_cus, ax_shop, ax_cp, ax_ca


def diminishing_returns(max_val, b1, num_samples=100):
    x = np.arange(0, num_samples)
    return max_val - np.exp(np.log(max_val) - b1*x)


if __name__ == '__main__':
    visualize_function(diminishing_returns(max_val=20000, b1=0.0005, num_samples=10000), 'diminishing returns', color='blue')
    plt.show()
