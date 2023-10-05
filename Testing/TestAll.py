import unittest

import Test_Flight
import Test_Main
from Test_Player import Test_Player


def main():
    modules = [Test_Main, Test_Flight, Test_Player]
    for module in modules:
        suite = unittest.TestLoader().loadTestsFromModule(module)
        unittest.TextTestRunner().run(suite)


if __name__ == "__main__":
    main()
