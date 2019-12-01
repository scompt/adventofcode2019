def fuel_for_mass(mass):
    """
    >>> fuel_for_mass(12)
    2
    >>> fuel_for_mass(14)
    2
    >>> fuel_for_mass(1969)
    654
    >>> fuel_for_mass(100756)
    33583
    >>> fuel_for_mass(0)
    0
    """
    return max(0, mass//3 - 2)

def weigh_fuel(fuel):
    """
    >>> weigh_fuel(12)
    2
    >>> weigh_fuel(1969)
    966
    >>> weigh_fuel(100756)
    50346
    """
    total_fuel = 0
    while True:
       fuel = fuel_for_mass(fuel)
       total_fuel += fuel

       if fuel == 0:
           return total_fuel

if __name__ == "__main__":
    import sys
    print(sum(weigh_fuel(int(line.strip())) for line in
        sys.stdin.readlines()))


