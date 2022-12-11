# -*- coding: utf-8 -*-
from ..tree.nodes import JobNode, NullJobNode


def start_updating_sigma_and_xi_propagation_from(
    jobk_node: JobNode,
    epsilon: int
) -> None:
    """Update some jobs's sigma and xi in balanced binary tree.

    Args:
        jobk_node (JobNode):
            The job which has been processed right before.
            Start update propagation from this job node to root.
        epsilon (int):
            Difference of jobk_node's p_plus value.
    Note:
        This function update jobk_node's sigma and xi in place.
    """
    def _update_xi(job_node: JobNode) -> None:
        """Update a job's xi

        Args:
            job_node (JobNode):
                Target job whose xi will be updated.
        Note:
            1. This function update job_node's xi in place.
            2. There is no update simga function because it's very simple formula.
        """
        lchild_job_node = job_node.left
        rchild_job_node = job_node.right

        if job_node.is_done():
            job_node.xi = max(
                lchild_job_node.xi + job_node.sigma,
                rchild_job_node.xi
            )
        else:
            job_node.xi = max(
                lchild_job_node.xi + job_node.sigma,
                job_node.q + job_node.sigma,
                rchild_job_node.xi
            )

    jobk_node.sigma += epsilon
    _update_xi(jobk_node)

    jobj_node = jobk_node
    while not isinstance(jobj_node.parent, NullJobNode):
        # Propagete update from jobk_node to root one by one.
        # Only jobs whose q is larger than jobk_node are updated.
        jobj_node = jobj_node.parent

        if jobj_node.q < jobk_node.q:
            jobj_node.sigma += epsilon
        _update_xi(jobj_node)

    return
