from simulation import Simulation
from regelsysteem import regelsysteem
from pin import simulated_pin
from bindings import init

def main():
    sim = Simulation()
    temp_func, humid_func = init(sim)
    print(temp_func(), humid_func())
    # regelsysteem()

if __name__ == '__main__':
    main()