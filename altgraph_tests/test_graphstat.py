import unittest

from altgraph import GraphStat
import sys

class TestDegreesDist (unittest.TestCase):

    @unittest.expectedFailure
    def test_missing(self):
        self.fail("add tests for GraphStat.degrees_dist")

class TestBinning (unittest.TestCase):
    def test_simple(self):

        # Binning [0, 100) into 10 bins
        a = list(xrange(100))
        out = GraphStat._binning(a, limits=(0, 100), bin_num=10)

        self.assertEquals(out,
                [ (x*1.0, 10) for x in xrange(5, 100, 10) ])


        # Check that outliers are ignored.
        a = list(xrange(100))
        out = GraphStat._binning(a, limits=(0, 90), bin_num=9)

        self.assertEquals(out,
                [ (x*1.0, 10) for x in xrange(5, 90, 10) ])


        out = GraphStat._binning(a, limits=(0, 100), bin_num=15)
        binSize = 100 / 15.0
        result = [0]*15
        for i in range(100):
            bin = int(i/binSize)
            try:
                result[bin] += 1
            except IndexError:
                pass

        result = [ (i * binSize + binSize/2, result[i]) for i in xrange(len(result))]

        self.assertEquals(result, out)

if __name__ == "__main__":
    unittest.main()
