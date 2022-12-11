import unittest

from ..tree.balanced_tree import BalancedJobTree
from ..tree.nodes import JobNode
from ..procedures.initialize import initialize_sigma_and_xi


class InitializeTest(unittest.TestCase):
    """Test class for initialize

    Note:
        r value is anything ok in this test.
    """

    def test_initialize_small_tree(self):
        """Test small balanced binary tree
        """
        job1_node = JobNode(-1, 2, 4, 'job1')
        job2_node = JobNode(-1, 7, 8, 'job2')
        job3_node = JobNode(-1, 4, 9, 'job3')

        job_nodes = [job1_node, job2_node, job3_node]
        job_tree = BalancedJobTree(job_nodes)
        job_tree.build_and_set_leaves()

        initialize_sigma_and_xi(job_tree)
        self.assertEqual((2, 6), (job1_node.sigma, job1_node.xi))
        self.assertEqual((11, 19), (job2_node.sigma, job2_node.xi))
        self.assertEqual((4, 13), (job3_node.sigma, job3_node.xi))

    @unittest.skip(reason='This case has yet to be calculated manually.')
    def test_initialize_large_tree(self):
        """Test large balanced binary tree

        Expected:
            Please refer the following article.
                Authors: Carlier, J., and Pinson, E. (1994)
                Title:     Adjustments of heads and tails for the job-shop problem
                Journal:  European Journal of Operational Research 78, 152
                URL:     https://www.sciencedirect.com/science/article/pii/0377221794903794
        """
        # We can set p-values arbitrarily, but initialization results will change with them.
        p_values = {
            'job1': 3, 'job2': 8, 'job3': 4, 'job4': 1, 'job5': 5, 'job6': 9, 'job7': 1,
            'job8': 2, 'job9': 7, 'job10': 6, 'job11': 3, 'job12': 9, 'job13': 4,
            'job14': 7, 'job15': 1
        }
        job_nodes = [JobNode(1, p, int(name[3:]), name) for name, p in p_values.items()]
        job_tree = BalancedJobTree(job_nodes)
        job_tree.build_and_set_leaves()

        initialize_sigma_and_xi(job_tree)

        # root

        # left subtree

        # right subtree


if __name__ == '__main__':
    unittest.main()
