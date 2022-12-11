# -*- coding: utf-8 -*-
import unittest

from ..tree.balanced_tree import BalancedJobTree
from ..tree.nodes import JobNode
from ..procedures.initialize import initialize_sigma_and_xi
from ..procedures.update import start_updating_sigma_and_xi_propagation_from


class UpdateTest(unittest.TestCase):
    """Test class for update
    """

    def setUp(self):
        """Set up each test

        In this test class, we use same jobs for each tests.
        """
        self.job_nodes = [
            JobNode(4, 2, 4, 'job1'),
            JobNode(1, 7, 8, 'job2'),
            JobNode(6, 4, 9, 'job3'),
        ]
        self.job_tree = BalancedJobTree(self.job_nodes)
        self.job_tree.build_and_set_leaves()
        initialize_sigma_and_xi(self.job_tree)

    def test_update_k_is_2(self):
        """Test the case that jobs are scheduled up to t = job2_node.r = 1
        """
        job1_node, job2_node, job3_node = self.job_nodes

        # There are no changes of every jobs's p_plus
        job1_node.p_plus = 2
        job2_node.p_plus = 7
        job3_node.p_plus = 4

        epsilon = 0
        # No update occurs on any jobs.
        for job_node in self.job_nodes:
            start_updating_sigma_and_xi_propagation_from(job_node, epsilon)

        self.assertEqual((2, 6), (job1_node.sigma, job1_node.xi))
        self.assertEqual((11, 19), (job2_node.sigma, job2_node.xi))
        self.assertEqual((4, 13), (job3_node.sigma, job3_node.xi))

    def test_update_k_is_1(self):
        """Test the case that jobs are scheduled up to t = job1_node.r = 4
        """
        job1_node, job2_node, job3_node = self.job_nodes

        # NOTE: No jobs were scheduled between t = 0 and t = 1,
        #        so we don't need to consider update in this interval.

        # According to JPS, job2 was scheduled between t = 1 and t = 4.
        job1_node.p_plus = 2
        job2_node.p_plus = 4
        job3_node.p_plus = 4

        # Job2 is scheduled for 3 time units from t = 1, so epsilon = 4 - 7 = -3.
        epsilon = -3
        start_updating_sigma_and_xi_propagation_from(job2_node, epsilon)

        self.assertEqual((2, 6), (job1_node.sigma, job1_node.xi))
        self.assertEqual((8, 16), (job2_node.sigma, job2_node.xi))
        self.assertEqual((4, 13), (job3_node.sigma, job3_node.xi))

    def test_update_k_is_3(self):
        """Test the case that jobs are scheduled up to t = job3_node.r = 6
        """
        job1_node, job2_node, job3_node = self.job_nodes

        # According to JPS, job2 was scheduled between t = 1 and t = 4.
        job1_node.p_plus = 2
        job2_node.p_plus = 4
        job3_node.p_plus = 4

        # Job2 was scheduled for 3 time units from t = 1, so epsilon = 4 - 7 = -3.
        epsilon = -3
        start_updating_sigma_and_xi_propagation_from(job2_node, epsilon)

        # According to JPS, job2 was scheduled between t = 4 and t = 6.
        job1_node.p_plus = 2
        job2_node.p_plus = 2
        job3_node.p_plus = 4

        # Job2 was scheduled for 2 time units from t = 4, so epsilon = 2 - 4 = -2.
        epsilon = -2
        start_updating_sigma_and_xi_propagation_from(job2_node, epsilon)

        self.assertEqual((2, 6), (job1_node.sigma, job1_node.xi))
        self.assertEqual((6, 14), (job2_node.sigma, job2_node.xi))
        self.assertEqual((4, 13), (job3_node.sigma, job3_node.xi))


if __name__ == '__main__':
    unittest.main()
