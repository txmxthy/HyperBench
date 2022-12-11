# -*- coding: utf-8 -*-
from ..tree.nodes import JobNode, NullJobNode
from ..tree.balanced_tree import BalancedJobTree


def initialize_sigma_and_xi(job_tree: BalancedJobTree) -> None:
    """Calculate initial value of each job's sigma and xi in balanced binary tree.

    Args:
        job_tree (BalancedJobTree):
            An BalancedJobTree instance whose build_and_set_leaves method already called.

    Note:
        This function initialize each job's sigma and xi in place.
    """
    err_msg = "job_tree must be called 'build_and_set_leaves' method before passed."
    assert isinstance(job_tree.root, JobNode), err_msg

    # initialization starts from leaves
    job_nodes = job_tree.leaves.copy()
    initialized_nodes = set()
    while True:
        job_node = job_nodes.popleft()
        if isinstance(job_node, NullJobNode):
            # This block is executed when root node is initialized right before.
            # This algorithm proceeds from leaves to root, so finish initialization.
            return

        parent_job_node = job_node.parent
        lchild_job_node = job_node.left
        rchild_job_node = job_node.right

        # Calculate sigma, xi and supplementary variable tau
        job_node.tau = lchild_job_node.tau + rchild_job_node.tau + job_node.p
        job_node.sigma = job_node.p + rchild_job_node.tau
        job_node.xi = max(
            lchild_job_node.xi + job_node.sigma,
            job_node.q + job_node.sigma,
            rchild_job_node.xi
        )
        initialized_nodes = {job_node} | initialized_nodes

        # NOTE: the data structure of job_nodes is deque, not set.
        # We need to take measures to initialize twice accidentally.
        if parent_job_node not in initialized_nodes:
            job_nodes.append(parent_job_node)
