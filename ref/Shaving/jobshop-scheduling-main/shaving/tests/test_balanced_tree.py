# -*- coding: utf-8 -*-
import unittest

from ..tree.balanced_tree import BalancedJobTree
from ..tree.nodes import JobNode


class BalancedJobTreeTest(unittest.TestCase):
    """Test class for balanced job tree
    """

    def test_even_number_jobs(self):
        """Test the case with six jobs

        Expected:
                            job4
                           /    \
                          /      \
                         /        \
                       job2       job6
                       /  \       /
                     job1 job3  job5
        """
        job1_node = JobNode(15, 5, 9, 'job1')
        job2_node = JobNode(20, 8, 14, 'job2')
        job3_node = JobNode(21, 8, 16, 'job3')
        job4_node = JobNode(4, 6, 20, 'job4')
        job5_node = JobNode(0, 8, 25, 'job5')
        job6_node = JobNode(9, 4, 30, 'job6')
        job_nodes = [job1_node, job2_node, job3_node, job4_node, job5_node, job6_node]
        job_tree = BalancedJobTree(job_nodes)
        job_tree.build_and_set_leaves()

        # root
        self.assertEqual(job4_node, job_tree.root)

        # left subtree
        self.assertEqual(job2_node, job_tree.root.left)
        self.assertEqual(job1_node, job_tree.root.left.left)
        self.assertEqual(job3_node, job_tree.root.left.right)

        # right subtree
        self.assertEqual(job6_node, job_tree.root.right)
        self.assertEqual(job5_node, job_tree.root.right.left)

    def test_odd_number_jobs(self):
        """Test the case with fifteen jobs

        Expected:
            Please refer the following article.
                Authors: Carlier, J., and Pinson, E. (1994)
                Title:     Adjustments of heads and tails for the job-shop problem
                Journal:  European Journal of Operational Research 78, 152
                URL:     https://www.sciencedirect.com/science/article/pii/0377221794903794
        """
        job_nodes = [JobNode(0, 0, i, f"job{i}") for i in range(1, 16)]
        job_tree = BalancedJobTree(job_nodes)
        job_tree.build_and_set_leaves()

        # root
        self.assertEqual(job_nodes[7], job_tree.root)

        # left subtree
        self.assertEqual(job_nodes[3], job_tree.root.left)
        self.assertEqual(job_nodes[1], job_tree.root.left.left)
        self.assertEqual(job_nodes[0], job_tree.root.left.left.left)
        self.assertEqual(job_nodes[2], job_tree.root.left.left.right)
        self.assertEqual(job_nodes[5], job_tree.root.left.right)
        self.assertEqual(job_nodes[4], job_tree.root.left.right.left)
        self.assertEqual(job_nodes[6], job_tree.root.left.right.right)

        # right subtree
        self.assertEqual(job_nodes[11], job_tree.root.right)
        self.assertEqual(job_nodes[9], job_tree.root.right.left)
        self.assertEqual(job_nodes[8], job_tree.root.right.left.left)
        self.assertEqual(job_nodes[10], job_tree.root.right.left.right)
        self.assertEqual(job_nodes[13], job_tree.root.right.right)
        self.assertEqual(job_nodes[12], job_tree.root.right.right.left)
        self.assertEqual(job_nodes[14], job_tree.root.right.right.right)


if __name__ == '__main__':
    unittest.main()
