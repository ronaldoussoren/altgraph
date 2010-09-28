import unittest
from altgraph import GraphUtil


class TestGraphUtil (unittest.TestCase):

    @unittest.expectedFailure
    def test_generate_random(self):
        self.fail("missing tests for GraphUtil.generate_random_graph")

    @unittest.expectedFailure
    def test_generate_scale_free(self):
        self.fail("missing tests for GraphUtil.generate_scale_free_graph")

    @unittest.expectedFailure
    def test_filter_stack(self):
        self.fail("missing tests for GraphUtil.filter_stack")

if __name__ == "__main__":
    unittest.main()
