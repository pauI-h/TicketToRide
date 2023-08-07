import unittest

import Test_Flight
import Test_Main


def main():
    modules = [Test_Main, Test_Flight]
    for module in modules:
        suite = unittest.TestLoader().loadTestsFromModule(module)
        unittest.TextTestRunner().run(suite)


if __name__ == "__main__":
    main()
