# -*- coding: utf-8 -*-
from typing import List, Set

from .procedures.initialize import initialize_sigma_and_xi
from .procedures.update import start_updating_sigma_and_xi_propagation_from
from .procedures.find import find_s_of
from .tree.balanced_tree import BalancedJobTree
from .tree.nodes import JobNode, NullJobNode
from .utils.sort import sort_job_nodes_by_qval


def adjust_heads(
    r_list: List[int],
    p_list: List[int],
    q_list: List[int],
    UB: int
) -> List[int]:
    """Adjust each jobs's r based on Carlier, J., and Pinson, E.(1994)

    If such a job exists, we set it to variable s, and otherwise set NullJobNode to s.

    Args:
        r_list (List[int]):
            The list of every job's release time r.
            Each list index corresponds to job number.
        p_list (List[int]):
            The list of every job's processing time p.
            Each list index corresponds to job number.
        q_list (List[int]):
            The list of every job's after processed time q.
            Each list index corresponds to job number.
        UB (int):
            Upper Bound of the last completed job's completion time.

    Returns:
        List[int]:
            Adjusted every job's r by this algorithm.

    Note:
        1. This function returns result, not in place.
        2. Job's r not all adjusted, only some jobs are adjusted.
        3. Adjustment results will change with given UB value.
    """
    def _select_just_released_job_nodes_from(target: Set[JobNode], time: int) -> Set[JobNode]:
        """Select jobs which satisfy r = t from target
        """
        return {job_node for job_node in target if job_node.r == time}

    # Initializations
    unsorted_job_nodes = [
        JobNode(r, p, q, name=f"job{i+1}")
        for i, (r, p, q) in enumerate(zip(r_list, p_list, q_list))
    ]
    sorted_job_nodes = sort_job_nodes_by_qval(unsorted_job_nodes)
    job_tree = BalancedJobTree(sorted_job_nodes)
    job_tree.build_and_set_leaves()

    initialize_sigma_and_xi(job_tree)
    t = min(job_node.r for job_node in sorted_job_nodes)

    non_completed_job_nodes = set(sorted_job_nodes)
    available_non_delayed_job_nodes = _select_just_released_job_nodes_from(
        target=non_completed_job_nodes,
        time=t
    )
    delayed_job_nodes = set()

    # main step
    while True:
        just_released_job_nodes = _select_just_released_job_nodes_from(
            target=available_non_delayed_job_nodes,
            time=t
        )
        for jobc_node in just_released_job_nodes:
            find_s_of(jobc_node, job_tree, UB)
            if not isinstance(jobc_node.s, NullJobNode):
                available_non_delayed_job_nodes -= {jobc_node}
                delayed_job_nodes |= {jobc_node}

        already_released_job_nodes = {
            job_node
            for job_node in non_completed_job_nodes if job_node.r <= t
        }
        still_not_released_job_nodes = non_completed_job_nodes - already_released_job_nodes
        jobi_node = max(already_released_job_nodes, key=lambda job_node: job_node.q)
        tmp_job_node = min(still_not_released_job_nodes, key=lambda job_node: job_node.r,
                           default=NullJobNode())
        t_tilde = tmp_job_node.r

        epsilon = min(jobi_node.p_plus, t_tilde - t)
        t += epsilon
        jobi_node.p_plus -= epsilon
        start_updating_sigma_and_xi_propagation_from(jobi_node, -epsilon)

        if jobi_node.is_done():
            jobi_node.complete_time = t
            non_completed_job_nodes -= {jobi_node}
            available_non_delayed_job_nodes -= {jobi_node}

        if not non_completed_job_nodes:
            return [job_node.r for job_node in unsorted_job_nodes]

        jobv_node = max(non_completed_job_nodes, key=lambda job_node: job_node.q)
        job_nodes_transited_from_delayed_to_non_delayed = {
            job_node
            for job_node in delayed_job_nodes
            if job_node.s.q > jobv_node.q
        }
        for jobj_node in job_nodes_transited_from_delayed_to_non_delayed:
            jobj_node.r = max(jobj_node.r, t)
            delayed_job_nodes -= {jobj_node}
            available_non_delayed_job_nodes |= {jobj_node}

        just_released_job_nodes = _select_just_released_job_nodes_from(
            target=non_completed_job_nodes - delayed_job_nodes,
            time=t
        )
        available_non_delayed_job_nodes |= just_released_job_nodes

        if not available_non_delayed_job_nodes:
            t = min(job_node.r for job_node in non_completed_job_nodes - delayed_job_nodes)
            just_released_job_nodes = _select_just_released_job_nodes_from(
                target=non_completed_job_nodes,
                time=t
            )
            available_non_delayed_job_nodes = just_released_job_nodes


def adjust_tails(
    r_list: List[int],
    p_list: List[int],
    q_list: List[int],
    UB: int
) -> List[int]:
    return adjust_heads(r_list=q_list, p_list=p_list, q_list=r_list, UB=UB)
