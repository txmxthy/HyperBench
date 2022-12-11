# -*- coding: utf-8 -*-
import unittest

from ..procedures.initialize import initialize_sigma_and_xi
from ..procedures.update import start_updating_sigma_and_xi_propagation_from
from ..procedures.find import find_s_of
from ..tree.balanced_tree import BalancedJobTree
from ..tree.nodes import JobNode
from ..utils.sort import sort_job_nodes_by_qval


class FindTest(unittest.TestCase):
    """Test class for find

    Expected:
        Please refer the following article.
            Authors: Carlier, J., and Pinson, E. (1990)
            Title:     A PRACTICAL USE OF JACKSON'S PREEMPTIVE SCHEDULE FOR SOLVING THE JOB SHOP PROBLEM
            Journal:  Annals of Operations Research 26, 272-275
            URL:     https://link.springer.com/article/10.1007/BF03543071

    Note:
        1. In this test class, we take 'unsorted' jobs as an test case.
        2. Variable name is not always equal to its value in following tests.
            e.g.) Variable job1 holds JobNode(15, 5, 9, 'job4') instance.
    """

    def setUp(self):
        """Set up each test
        In this test class, we use same jobs for each tests.
        """

        unsorted_job_nodes = [
            JobNode(4, 6, 20, 'job1'),
            JobNode(0, 8, 25, 'job2'),
            JobNode(9, 4, 30, 'job3'),
            JobNode(15, 5, 9, 'job4'),
            JobNode(20, 8, 14, 'job5'),
            JobNode(21, 8, 16, 'job6'),
        ]
        sorted_job_nodes = sort_job_nodes_by_qval(unsorted_job_nodes)
        self.job_nodes = sorted_job_nodes
        self.job_tree = BalancedJobTree(sorted_job_nodes)
        self.job_tree.build_and_set_leaves()
        initialize_sigma_and_xi(self.job_tree)

    def test_initialize(self):
        job1_node, job2_node, job3_node, job4_node, job5_node, job6_node = self.job_nodes

        self.assertEqual((5, 14), (job1_node.sigma, job1_node.xi))
        self.assertEqual((16, 30), (job2_node.sigma, job2_node.xi))
        self.assertEqual((8, 24), (job3_node.sigma, job3_node.xi))
        self.assertEqual((18, 48), (job4_node.sigma, job4_node.xi))
        self.assertEqual((8, 33), (job5_node.sigma, job5_node.xi))
        self.assertEqual((4, 37), (job6_node.sigma, job6_node.xi))

    @unittest.skip(reason='This case has yet to be calculated manually.')
    def test_update(self):
        pass

    def test_find1(self):
        """Test the case that c = 1 and UB = 52

        Expected:
            jobc_node.s = 2
        """
        # メモ： update のテストから jobk_nodeとしているが，それ以前は単純にjobk としてる。
        # どっちかに統一しなければ
        job1_node, job2_node, _, job4_node, job5_node, job6_node = self.job_nodes

        jobc_node = job1_node
        # Process jobs until t = jobc_node.r = 15

        # According to JPS, job5 was scheduled between t = 0 and t = 8.
        # Job5 is scheduled for 8 time units from t = 1, so epsilon = 0 - 8 = -8.
        job5_node.p_plus = 0
        epsilon = -8
        start_updating_sigma_and_xi_propagation_from(job5_node, epsilon)

        # Job4 was scheduled between t = 8 and t = 9.
        # Job4 is scheduled for 1 time units from t = 8, so epsilon = 5 - 6 = -1.
        job4_node.p_plus = 5
        epsilon = -1
        start_updating_sigma_and_xi_propagation_from(job4_node, epsilon)

        # Job6 was scheduled between t = 9 and t = 13.
        # Job6 is scheduled for 4 time units from t = 9, so epsilon = 0 - 4 = -4.
        job6_node.p_plus = 0
        epsilon = -4
        start_updating_sigma_and_xi_propagation_from(job6_node, epsilon)

        # Job4 was scheduled between t = 13 and t = 15(= jobc_node.r)
        # Job4 is scheduled for 2 time units from t = 13, so epsilon = 3 - 5 = -2.
        job4_node.p_plus = 3
        epsilon = -2
        start_updating_sigma_and_xi_propagation_from(job4_node, epsilon)

        # Find
        find_s_of(jobc_node, self.job_tree, UB=52)
        expected_s = job2_node

        self.assertEqual(jobc_node.s, expected_s)

    def test_find2(self):
        """Test the case that c = 1 and UB = 51

        Expected:
            jobc_node.s = 2
        """
        # メモ： update のテストから jobk_nodeとしているが，それ以前は単純にjobk としてる。
        # どっちかに統一しなければ
        job1_node, job2_node, _, job4_node, job5_node, job6_node = self.job_nodes

        jobc_node = job1_node
        # Process jobs until t = jobc_node.r = 15

        # According to JPS, job5 was scheduled between t = 0 and t = 8.
        # Job5 is scheduled for 8 time units from t = 1, so epsilon = 0 - 8 = -8.
        job5_node.p_plus = 0
        epsilon = -8
        start_updating_sigma_and_xi_propagation_from(job5_node, epsilon)

        # Job4 was scheduled between t = 8 and t = 9.
        # Job4 is scheduled for 1 time units from t = 8, so epsilon = 5 - 6 = -1.
        job4_node.p_plus = 5
        epsilon = -1
        start_updating_sigma_and_xi_propagation_from(job4_node, epsilon)

        # Job6 was scheduled between t = 9 and t = 13.
        # Job6 is scheduled for 4 time units from t = 9, so epsilon = 0 - 4 = -4.
        job6_node.p_plus = 0
        epsilon = -4
        start_updating_sigma_and_xi_propagation_from(job6_node, epsilon)

        # Job4 was scheduled between t = 13 and t = 15(= jobc_node.r)
        # Job4 is scheduled for 2 time units from t = 13, so epsilon = 3 - 5 = -2.
        job4_node.p_plus = 3
        epsilon = -2
        start_updating_sigma_and_xi_propagation_from(job4_node, epsilon)

        # Find
        find_s_of(jobc_node, self.job_tree, UB=51)
        expected_s = job2_node

        self.assertEqual(jobc_node.s, expected_s)

    def test_find3(self):
        """Test the case that c = 2 and UB = 51

        Expected:
            jobc_node.s = 3
        """
        # メモ： update のテストから jobk_nodeとしているが，それ以前は単純にjobk としてる。
        # どっちかに統一しなければ
        job1_node, job2_node, job3_node, job4_node, job5_node, job6_node = self.job_nodes

        jobc_node = job2_node
        # Process jobs until t = jobc_node.r = 20

        # According to JPS, job5 was scheduled between t = 0 and t = 8.
        # Job5 is scheduled for 8 time units from t = 1, so epsilon = 0 - 8 = -8.
        job5_node.p_plus = 0
        epsilon = -8
        start_updating_sigma_and_xi_propagation_from(job5_node, epsilon)

        # Job4 was scheduled between t = 8 and t = 9.
        # Job4 is scheduled for 1 time units from t = 8, so epsilon = 5 - 6 = -1.
        job4_node.p_plus = 5
        epsilon = -1
        start_updating_sigma_and_xi_propagation_from(job4_node, epsilon)

        # Job6 was scheduled between t = 9 and t = 13.
        # Job6 is scheduled for 4 time units from t = 9, so epsilon = 0 - 4 = -4.
        job6_node.p_plus = 0
        epsilon = -4
        start_updating_sigma_and_xi_propagation_from(job6_node, epsilon)

        # Job4 was scheduled between t = 13 and t = 18(= jobc_node.r)
        # Job4 is scheduled for 5 time units from t = 13, so epsilon = 0 - 5 = -5.
        job4_node.p_plus = 0
        epsilon = -5
        start_updating_sigma_and_xi_propagation_from(job4_node, epsilon)

        # Job1 was scheduled between t = 18 and t = 20(= jobc_node.r)
        # Job1 is scheduled for 5 time units from t = 18, so epsilon = 2 - 4 = -2.
        job1_node.p_plus = 2
        epsilon = -2
        start_updating_sigma_and_xi_propagation_from(job1_node, epsilon)

        # Find
        find_s_of(jobc_node, self.job_tree, UB=51)
        expected_s = job3_node

        self.assertEqual(jobc_node.s, expected_s)


if __name__ == '__main__':
    unittest.main()
