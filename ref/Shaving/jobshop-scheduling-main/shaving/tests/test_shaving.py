# -*- coding: utf-8 -*-
import unittest

from ..shaving import adjust_heads


class AdjustReleaseTimeTest(unittest.TestCase):
    """Test class for adjust_heads
    """

    def test_adjustment1(self):
        """Test the case with 3 jobs

        Expected:
            Please refer the following article.
                Authors: Brinkkotter, W. and P. Brucker (2001)
                Title:     Solving open data instances for the job-shop problem by parallel head–tail adjustments.
                Journal:  Journal of Scheduling 4, 56
                URL:     https://onlinelibrary.wiley.com/doi/10.1002/1099-1425(200101/02)4:1%3C53::AID-JOS59%3E3.0.CO;2-Y
        """
        r_list = [2, 3, 4]
        p_list = [3, 2, 2]
        q_list = [2, 6, 8]

        adjusted_r_list = adjust_heads(r_list, p_list, q_list, UB=14)

        expected_adjusted_r_list = [7, 6, 4]
        self.assertEqual(expected_adjusted_r_list, adjusted_r_list)

    def test_adjustment2(self):
        """Test the case with 5 jobs

        Expected:
            Please refer the following article.
                Authors: Carlier, J., and Rebai, I. (1996)
                Title:    Two branch and bound algorithms for the permutation flow shop problem
                Journal:  European Journal of Operational Research 90, 240
                URL:     https://www.sciencedirect.com/science/article/pii/0377221795003525
        """
        r_list = [4, 0, 2, 10, 15]
        p_list = [3, 5, 9, 6, 7]
        q_list = [8, 5, 10, 11, 20]

        adjusted_r_list = adjust_heads(r_list, p_list, q_list, UB=42)

        expected_adjusted_r_list = [4, 0, 2, 22, 15]
        self.assertEqual(expected_adjusted_r_list, adjusted_r_list)

    def test_adjustment3(self):
        """Test the case with 6 jobs

        Expected:
            Please refer the following article.
                Authors: Carlier, J., and Pinson, E. (1990)
                Title:     A PRACTICAL USE OF JACKSON'S PREEMPTIVE SCHEDULE FOR SOLVING THE JOB SHOP PROBLEM
                Journal:  Annals of Operations Research 26, 272-275
                URL:     https://link.springer.com/article/10.1007/BF03543071
        """
        r_list = [4, 0, 9, 15, 20, 21]
        p_list = [6, 8, 4, 5, 8, 8]
        q_list = [20, 25, 30, 9, 14, 16]

        adjusted_r_list = adjust_heads(r_list, p_list, q_list, UB=52)

        expected_adjusted_r_list = [4, 0, 9, 36, 20, 21]
        self.assertEqual(expected_adjusted_r_list, adjusted_r_list)

    def test_adjustment4(self):
        """Test the case with 6 jobs

        We use same jobs as test_adjustment3, but change the UB to 51
        """
        r_list = [4, 0, 9, 15, 20, 21]
        p_list = [6, 8, 4, 5, 8, 8]
        q_list = [20, 25, 30, 9, 14, 16]

        adjusted_r_list = adjust_heads(r_list, p_list, q_list, UB=51)

        expected_adjusted_r_list = [4, 0, 9, 36, 29, 21]
        self.assertEqual(expected_adjusted_r_list, adjusted_r_list)


if __name__ == '__main__':
    unittest.main()
