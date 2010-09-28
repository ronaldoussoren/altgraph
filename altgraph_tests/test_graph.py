import unittest

class TestGraph (unittest.TestCase):

    @unittest.expectedFailure
    def test_missing(self):
        self.fail("add tests for algraph.Graph")

if __name__ == "__main__":
    unittest.main()
