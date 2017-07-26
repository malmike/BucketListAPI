import unittest
from tests import base_test

suite = unittest.TestLoader().loadTestsFromTestCase(base_test.BaseTest)

unittest.TextTestRunner(verbosity=1).run(suite)