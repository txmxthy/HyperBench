# -*- coding: utf-8 -*-
from collections import deque
from typing import List, Optional

from ..utils.sort import sort_job_nodes_by_qval
from .nodes import JobNode, NullJobNode


class BalancedJobTree(object):
    """Balanced binary tree for adjustment of heads and tails
    """

    def __init__(self, job_nodes_sorted_asc_order_by_qval: List[JobNode]):
        err_msg = 'job nodes must be sorted in ascending order by q-val before passed.'
        is_asc_order = (
            job_nodes_sorted_asc_order_by_qval
            == sort_job_nodes_by_qval(job_nodes_sorted_asc_order_by_qval)
        )
        assert is_asc_order, err_msg

        self.__job_nodes = job_nodes_sorted_asc_order_by_qval
        self.__root = NullJobNode()
        self.__leaves = deque()

    @property
    def job_nodes(self):
        return self.__job_nodes

    @property
    def root(self) -> Optional[JobNode]:
        return self.__root

    @property
    def leaves(self) -> deque:
        return self.__leaves

    def build_and_set_leaves(self) -> None:
        """Build balanced binary tree according to jobs and assign leaves to variable.

        Logic is very simple.
        Each instance of this class has jobs which sorted in ascending order by q value,
        so we only need to pick up a job in the middle of job list and put it on root.
        By applying this procedure to jobs on the left side of root and the other side
        recursively until job list length is equal to 0 or 1, we can obtain balanced binary tree.
        """

        def _build_balanced_tree(job_nodes: List[JobNode]) -> JobNode:
            """Inner function for recursion
            """
            num_jobs = len(job_nodes)
            if num_jobs == 0:
                # This block is executed when the first input length is even.
                return NullJobNode()
            if num_jobs == 1:
                # This block is executed when the first input length is odd.
                leaf = job_nodes[0]
                self.__leaves.append(leaf)
                return leaf

            mid = num_jobs // 2
            root = job_nodes[mid]

            root.left = _build_balanced_tree(job_nodes[:mid])
            if not isinstance(root.left, NullJobNode):
                root.left.parent = root

            root.right = _build_balanced_tree(job_nodes[mid + 1:])
            if not isinstance(root.right, NullJobNode):
                root.right.parent = root

            return root

        self.__root = _build_balanced_tree(self.__job_nodes)
        return
