import unittest

from benchmarks.base_functions import sphere as base_sphere
from benchmarks.shifted_functions import _load_shift_vector
from benchmarks.shifted_functions import *
from test_cases import *


class TestShiftedFunctions(unittest.TestCase):
    def test_generate_shift_vector(self):
        shift_vector = generate_shift_vector('sphere', 2, -5, 10, 0)
        self.assertEqual(shift_vector.size, 2)
        self.assertTrue(np.all(shift_vector >= -5))
        self.assertTrue(np.all(shift_vector < 10))
        self.assertTrue(np.allclose(shift_vector, [4.554425309821814594e+00, -9.531992935419451030e-01]))

        shift_vector = generate_shift_vector(base_sphere, 2, [-1, -2], [1, 2], 0)
        self.assertEqual(shift_vector.size, 2)
        self.assertTrue(np.all(shift_vector >= [-1, -2]))
        self.assertTrue(np.all(shift_vector < [1, 2]))
        self.assertTrue(np.allclose(shift_vector, [2.739233746429086125e-01, -9.208531449445187533e-01]))

        shift_vector = generate_shift_vector(base_sphere, 1, -100, 100, 7)
        self.assertEqual(shift_vector.size, 1)
        self.assertTrue(np.all(shift_vector >= -100))
        self.assertTrue(np.all(shift_vector < 100))
        self.assertTrue(np.allclose(shift_vector, 2.501909332093339344e+01))

    def test_load_shift_vector(self):
        func = base_sphere
        generate_shift_vector(func, 2, [-1, -2], [1, 2], 0)
        shift_vector = _load_shift_vector(func, [0, 0])
        self.assertTrue(np.allclose(shift_vector, [2.739233746429086125e-01, -9.208531449445187533e-01]))

        generate_shift_vector(func, 3, -100, 100, 7)
        shift_vector = _load_shift_vector(func, [0, 0, 0])
        self.assertTrue(np.allclose(shift_vector,
                                    [2.501909332093339344e+01, 7.944276019391509180e+01, 5.513713804903869686e+01]))

        shift_vector = _load_shift_vector(func, 0, 77)
        self.assertTrue(np.allclose(shift_vector, 77))

    def test_sphere(self):
        sample = TestCases(is_shifted=True)
        for func in [sphere, Sphere()]:
            for ndim in range(1, 8):
                self.assertTrue(sample.compare(func, ndim, get_y_sphere(ndim - 1)))
            self.assertTrue(sample.check_origin(func))

    def test_cigar(self):
        sample = TestCases(is_shifted=True)
        for func in [cigar, Cigar()]:
            for ndim in range(2, 8):
                self.assertTrue(sample.compare(func, ndim, get_y_cigar(ndim - 2)))
            with self.assertRaisesRegex(TypeError, 'The size should > 1+'):
                sample.compare(func, 1, np.empty((5,)))
            self.assertTrue(sample.check_origin(func))

    def test_discus(self):
        sample = TestCases(is_shifted=True)
        for func in [discus, Discus()]:
            for ndim in range(2, 8):
                self.assertTrue(sample.compare(func, ndim, get_y_discus(ndim - 2)))
            with self.assertRaisesRegex(TypeError, 'The size should > 1+'):
                sample.compare(func, 1, np.empty((5,)))
            self.assertTrue(sample.check_origin(func))

    def test_cigar_discus(self):
        sample = TestCases(is_shifted=True)
        for func in [cigar_discus, CigarDiscus()]:
            for ndim in range(2, 8):
                self.assertTrue(sample.compare(func, ndim, get_y_cigar_discus(ndim - 2)))
            with self.assertRaisesRegex(TypeError, 'The size should > 1+'):
                sample.compare(func, 1, np.empty((5,)))
            self.assertTrue(sample.check_origin(func))

    def test_ellipsoid(self):
        sample = TestCases(is_shifted=True)
        for func in [ellipsoid, Ellipsoid()]:
            for ndim in range(2, 8):
                self.assertTrue(sample.compare(func, ndim, get_y_ellipsoid(ndim - 2)))
            with self.assertRaisesRegex(TypeError, 'The size should > 1+'):
                sample.compare(func, 1, np.empty((5,)))
            self.assertTrue(sample.check_origin(func))

    def test_different_powers(self):
        sample = TestCases(is_shifted=True)
        for func in [different_powers, DifferentPowers()]:
            for ndim in range(2, 8):
                self.assertTrue(sample.compare(func, ndim, get_y_different_powers(ndim - 2), atol=0.1))
            with self.assertRaisesRegex(TypeError, 'The size should > 1+'):
                sample.compare(func, 1, np.empty((5,)))
            self.assertTrue(sample.check_origin(func))

    def test_schwefel221(self):
        sample = TestCases(is_shifted=True)
        for func in [schwefel221, Schwefel221()]:
            for ndim in range(1, 8):
                self.assertTrue(sample.compare(func, ndim, get_y_schwefel221(ndim - 1)))
            self.assertTrue(sample.check_origin(func))

    def test_step(self):
        sample = TestCases(is_shifted=True)
        for func in [step, Step()]:
            for ndim in range(1, 8):
                self.assertTrue(sample.compare(func, ndim, get_y_step(ndim - 1)))
            self.assertTrue(sample.check_origin(func))

    def test_schwefel222(self):
        sample = TestCases(is_shifted=True)
        for func in [schwefel222, Schwefel222()]:
            for ndim in range(1, 8):
                self.assertTrue(sample.compare(func, ndim, get_y_schwefel222(ndim - 1)))
            self.assertTrue(sample.check_origin(func))

    def test_rosenbrock(self):
        sample = TestCases(is_shifted=True)
        for func in [rosenbrock, Rosenbrock()]:
            for ndim in range(2, 8):
                self.assertTrue(sample.compare(func, ndim, get_y_rosenbrock(ndim - 2)))
            with self.assertRaisesRegex(TypeError, 'The size should > 1+'):
                sample.compare(func, 1, np.empty((5,)))

    def test_schwefel12(self):
        sample = TestCases(is_shifted=True)
        for func in [schwefel12, Schwefel12()]:
            for ndim in range(2, 8):
                self.assertTrue(sample.compare(func, ndim, get_y_schwefel12(ndim - 2)))
            with self.assertRaisesRegex(TypeError, 'The size should > 1+'):
                sample.compare(func, 1, np.empty((5,)))
            self.assertTrue(sample.check_origin(func))

    def test_griewank(self):
        sample = TestCases(is_shifted=True)
        for func in [griewank, Griewank()]:
            for ndim in range(2, 8):
                self.assertTrue(sample.compare(func, ndim, get_y_griewank(ndim - 2), atol=0.001))
            self.assertTrue(sample.check_origin(func))

    def test_ackley(self):
        sample = TestCases(is_shifted=True)
        for func in [ackley, Ackley()]:
            for ndim in range(2, 8):
                self.assertTrue(sample.compare(func, ndim, get_y_ackley(ndim - 2), atol=0.001))
            self.assertTrue(sample.check_origin(func))

    def test_rastrigin(self):
        sample = TestCases(is_shifted=True)
        for func in [rastrigin, Rastrigin()]:
            for ndim in range(2, 8):
                self.assertTrue(sample.compare(func, ndim, get_y_rastrigin(ndim - 2)))
            self.assertTrue(sample.check_origin(func))


if __name__ == '__main__':
    unittest.main()
