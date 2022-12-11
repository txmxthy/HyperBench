# -*- coding: utf-8 -*-
from ..tree.balanced_tree import BalancedJobTree
from ..tree.nodes import JobNode, NullJobNode
from ..procedures.update import start_updating_sigma_and_xi_propagation_from


def find_s_of(jobc_node: JobNode, job_tree: BalancedJobTree, UB: int) -> None:
    """Find a job 's' which satisfy (5) and (6) in Carlier, J., and Pinson, E.(1994) in a given job

    If such a job exists, we set it to variable s, and otherwise set NullJobNode to s.

    Args:
        jobc_node (JobNode):
            Target job which is scanned if it has s or not.
        job_tree (BalancedJobTree):
            BalancedJobTree instance containing jobc_node.
        UB (int):
            Upper Bound of the last completed job's completion time.
    Note:
        1. This function find s and set it to jobc_node in place.
        2. All of jobs's sigma, xi, and p_plus must be updated before passed.
    """
    jobc_node.s = NullJobNode()

    # Assume that jobc is processed between t = jobc.r to t = jobc.r + jobc.p
    start_updating_sigma_and_xi_propagation_from(jobc_node, epsilon=-jobc_node.p)
    # Margin until constraint (5) is satisfied.
    delta = UB - (jobc_node.r + jobc_node.p)

    jobk_node = job_tree.root
    # If following condition is satisfied even once, then a job 's' exists.     # 本当か？？？
    while jobk_node.xi > delta:
        lchild_job_node = jobk_node.left
        rchild_job_node = jobk_node.right

        if lchild_job_node.xi + jobk_node.sigma > delta:
            delta -= jobk_node.sigma
            jobk_node = lchild_job_node
        else:
            if jobk_node.q + jobk_node.sigma > delta and not jobk_node.is_done():
                jobc_node.s = jobk_node
                jobk_node = NullJobNode()
            else:
                jobk_node = rchild_job_node

    # Rollback previous assumption
    start_updating_sigma_and_xi_propagation_from(jobc_node, epsilon=jobc_node.p)
