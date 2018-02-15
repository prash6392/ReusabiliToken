"""@package app_reusabilityToken_simulator
Simulates a market where resuabilty tokens are at work
"""
import argparse
from SimulationEngine import SimulationEngine

num_iterations = 100
num_customers = 3
num_shops = 2


def setup_args():
    global num_iterations, num_customers, num_shops
    parser = argparse.ArgumentParser('ReusabiliToken Simulator')
    parser.add_argument('--num_iterations', type=int, help='Number of iterations', default=100)
    parser.add_argument('--num_customers', type=int, help='Number of customers', default=100)
    parser.add_argument('--num_shops', type=int, help='Number of shops', default=5)
    args = parser.parse_args()
    num_iterations = args.num_iterations
    num_customers = args.num_customers
    num_shops = args.num_shops


def run_simulator():
    global num_iterations, num_customers, num_shops
    sim_engine = SimulationEngine(num_customers=num_customers,
                                  num_shops=num_shops,
                                  sim_iters=num_iterations,
                                  coin_limit=200,
                                  rep_limit=100,
                                  coin_rep_factor=1.0,
                                  payment_due=30)
    sim_engine.run()


if __name__ == '__main__':
    setup_args()
    run_simulator()

