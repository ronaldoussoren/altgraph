import unittest

from altgraph import Dot

class TestDot (unittest.TestCase):

    @unittest.expectedFailure
    def test_missing(self):
        self.fail("add tests for altgraph.Dot")

if __name__ == "__main__":
    unittest.main()
