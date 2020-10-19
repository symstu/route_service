import unittest
from v1.models import user, metadata


class TestSeed(unittest.TestCase):
    def test_seed(self):
        import pdb
        user.create()
        pdb.set_trace()
