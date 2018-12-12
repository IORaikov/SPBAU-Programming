# -*- coding: utf-8 -*-
import functools
import unittest


@functools.lru_cache()
def gcd_recursive(a: 'int', b: 'int') -> 'int':
    if(b == 0):
        return a
    return gcd_recursive(b, a % b)


@functools.lru_cache()
def gcd_cyclic(a: 'int', b: 'int') -> 'int':
    if(b > a):
        a, b = b, a
    while(a > 0 and b > 0):
        d = b
        b = a % b
        a = d
    return a


class TestSimpleEuclid(unittest.TestCase):

    def test_big_primes(self):
        self.assertEqual(gcd_cyclic(1000000007, 10000000033), 1)


class TestEuclidEquivalence(unittest.TestCase):

    def test_first_1000(self):
        for i in range(0, 1000):
            for j in range(0, 1000):
                self.assertEqual(gcd_recursive(i, j), gcd_cyclic(i, j))


if __name__ == '__main__':
    unittest.main(verbosity=2)
