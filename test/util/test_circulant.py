from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import math
import torch
import unittest
from gpytorch.utils import circulant
from gpytorch import utils


class TestCirculant(unittest.TestCase):

    def test_rotate_vector_forward(self):
        a = torch.randn(5)
        Q0 = torch.zeros(5, 5)
        Q0[0, 4] = 1
        Q0[1:, :-1] = torch.eye(4)

        Q = Q0.clone()
        for i in range(1, 5):
            a_rotated_result = circulant.rotate(a, i)
            a_rotated_actual = Q.matmul(a)

            self.assertTrue(
                utils.approx_equal(a_rotated_actual, a_rotated_result)
            )
            Q = Q.matmul(Q0)

    def test_rotate_vector_reverse(self):
        a = torch.randn(5)
        Q0 = torch.zeros(5, 5)
        Q0[0, 4] = 1
        Q0[1:, :-1] = torch.eye(4)

        Q = Q0.clone()
        for i in range(1, 5):
            a_rotated_result = circulant.rotate(a, -i)
            a_rotated_actual = Q.inverse().matmul(a)

            self.assertTrue(
                utils.approx_equal(a_rotated_actual, a_rotated_result)
            )
            Q = Q.matmul(Q0)

    def test_rotate_matrix_forward(self):
        a = torch.randn(5, 5)
        Q0 = torch.zeros(5, 5)
        Q0[0, 4] = 1
        Q0[1:, :-1] = torch.eye(4)

        Q = Q0.clone()
        for i in range(1, 5):
            a_rotated_result = circulant.rotate(a, i)
            a_rotated_actual = Q.matmul(a)

            self.assertTrue(
                utils.approx_equal(a_rotated_actual, a_rotated_result)
            )
            Q = Q.matmul(Q0)

    def test_rotate_matrix_reverse(self):
        a = torch.randn(5, 5)
        Q0 = torch.zeros(5, 5)
        Q0[0, 4] = 1
        Q0[1:, :-1] = torch.eye(4)

        Q = Q0.clone()
        for i in range(1, 5):
            a_rotated_result = circulant.rotate(a, -i)
            a_rotated_actual = Q.inverse().matmul(a)

            self.assertTrue(
                utils.approx_equal(a_rotated_actual, a_rotated_result)
            )
            Q = Q.matmul(Q0)

    def test_left_rotate_trace(self):
        a = torch.randn(5, 5)

        for i in range(1, 5):
            actual = circulant.rotate(a, i).trace()
            result = circulant.left_rotate_trace(a, i)

            self.assertLess(math.fabs(actual - result), 1e-5)

    def test_right_rotate_trace(self):
        a = torch.randn(5, 5)

        for i in range(1, 5):
            actual = circulant.rotate(a, -i).trace()
            result = circulant.left_rotate_trace(a, -i)

            self.assertLess(math.fabs(actual - result), 1e-5)

    def test_circulant_transpose(self):
        a = torch.randn(5)

        C = circulant.circulant(a)
        C_T_actual = C.t()
        C_T_result = circulant.circulant(circulant.circulant_transpose(a))

        self.assertTrue(utils.approx_equal(C_T_actual, C_T_result))

    def test_circulant_matmul(self):
        a = torch.randn(5)
        M = torch.randn(5, 5)

        aM_result = circulant.circulant_matmul(a, M)
        C = circulant.circulant(a)
        aM_actual = C.mm(M)

        self.assertTrue(utils.approx_equal(aM_result, aM_actual))

    def test_circulant_inv_matmul(self):
        a = torch.randn(5)
        M = torch.randn(5, 5)

        aM_result = circulant.circulant_inv_matmul(a, M)
        C = circulant.circulant(a)
        aM_actual = C.inverse().mm(M)

        self.assertTrue(utils.approx_equal(aM_result, aM_actual))

    def test_frobenius_circulant_approximation(self):
        A = torch.randn(5, 5)

        C1 = circulant.frobenius_circulant_approximation(A)
        C2 = circulant.frobenius_circulant_approximation(circulant.circulant(C1))

        self.assertTrue(utils.approx_equal(C1, C2))

    def test_frobenius_circulant_approximation_toeplitz(self):
        toeplitz_column = torch.randn(5)

        C1 = circulant.frobenius_circulant_approximation_toeplitz(toeplitz_column)
        C2 = circulant.frobenius_circulant_approximation_toeplitz(C1)

        self.assertLess(torch.norm(C1 - C2), 1e-3)


if __name__ == '__main__':
    unittest.main()
