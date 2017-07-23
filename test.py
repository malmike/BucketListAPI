import unittest

suite = unittest.TestLoader()

unittest.TextTestRunner(verbosity=1).run(suite)