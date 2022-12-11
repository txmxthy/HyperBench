# -*- coding: utf-8 -*-
from typing import List

from ..tree.nodes import JobNode


def sort_job_nodes_by_qval(unsorted_job_nodes: List[JobNode]):
    """Sort jobs by q value
    """
    return sorted(unsorted_job_nodes, key=lambda job: job.q)
