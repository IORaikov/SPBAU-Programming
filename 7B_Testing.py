import functools
import unittest


def is_simple(value: 'int') -> 'bool':
    if(value == 1):
        return False
    if(value == 2):
        return True
    if(value % 2 == 0):
        return False
    a = 3
    while(a * a <= value):
        if(value % a == 0):
            return False
        a += 2
    return True


@functools.lru_cache()
def is_simple_cached(value: 'int') -> 'bool':
    return is_simple(value)


class TestIsPrime(unittest.TestCase):

    def test_2(self):
        self.assertTrue(is_simple(2))
        self.assertTrue(is_simple_cached(2))

    def test_1(self):
        self.assertFalse(is_simple(1))
        self.assertFalse(is_simple_cached(1))

    def test_big_prime(self):
        self.assertTrue(is_simple(1000000000039))
        self.assertTrue(is_simple_cached(1000000000039))

    def test_big_even(self):
        self.assertFalse(is_simple(100000003127831239212))
        self.assertFalse(is_simple_cached(100000003127831239212))

    def test_prime_multiple(self):
        self.assertFalse(is_simple(1009 * 1123))
        self.assertFalse(is_simple_cached(1009 * 1123))


if __name__ == '__main__':
    unittest.main(verbosity=2)

