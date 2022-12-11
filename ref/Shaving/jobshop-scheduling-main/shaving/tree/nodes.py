# -*- coding: utf-8 -*-
from __future__ import annotations
from typing import Union


class BaseJob(object):
    """Base class for jobs
    """

    def __init__(self, r: int, p: int, q: int, name: str = 'job'):
        # Once an instance is created, p and name cannot be modified.
        self.__r = r
        self.__p = p
        self.__q = q
        self.__name = name

    def __str__(self) -> str:
        return self.__name

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(r={self.__r}, p={self.__p}, q={self.__q}, name='{self.__name}')"

    @property
    def r(self) -> int:
        return self.__r

    @r.setter
    def r(self, new_val: int) -> None:
        err_msg = 'Your adjustment of r is invalid because it makes situation worse.'
        assert self.__r <= new_val, err_msg
        self.__r = new_val

    @property
    def p(self) -> int:
        return self.__p

    @property
    def q(self) -> int:
        return self.__q

    @q.setter
    def q(self, new_val: int) -> None:
        err_msg = 'Your adjustment of q is invalid because it makes situation worse.'
        assert self.__q <= new_val, err_msg
        self.__q = new_val

    @property
    def name(self) -> str:
        return self.__name


class NullJobNode(BaseJob):
    """Representation of not existing JobNode.
    """
    __singleton = None

    def __new__(cls):
        if cls.__singleton is None:
            cls.__singleton = super().__new__(cls)
        return cls.__singleton

    def __init__(self):
        super().__init__(r=float('+inf'), p=float('+inf'), q=float('+inf'), name='null')
        self.sigma = 0
        self.tau = 0
        self.xi = float('-inf')


class JobNode(BaseJob):
    """Job node of balanced binary tree.

    Note:
        1. JobNode keeps parent pointer for adjusting algorithm.
        2. JobNode instances don't have sigma, xi, and tau initially.
    """

    def __init__(self, r: int, p: int, q: int, name: str = 'job'):
        super().__init__(r, p, q, name)

        # rest of processing time
        self.__p_plus = p

        self.__parent = NullJobNode()
        self.__left = NullJobNode()
        self.__right = NullJobNode()

    @property
    def p_plus(self) -> int:
        return self.__p_plus

    @p_plus.setter
    def p_plus(self, new_val: int) -> None:
        """Validate new p_plus value is valid or not.

        Args:
            new_val (int): new p_plus value. If it is valid, it must be a positive integer.
        """
        assert new_val >= 0, f"job '{self.name}' is overscheduled. Please check your code."
        self.__p_plus = new_val

    @property
    def parent(self) -> Union[JobNode, NullJobNode]:
        return self.__parent

    @parent.setter
    def parent(self, job_node: Union[JobNode, NullJobNode]):
        err_msg = (
            'parent node must be JobNode or NullJobNode instance, '
            f"but got {job_node.__class__.__name__} instance."
        )
        assert isinstance(job_node, BaseJob), err_msg
        self.__parent = job_node

    @property
    def left(self) -> Union[JobNode, NullJobNode]:
        return self.__left

    @left.setter
    def left(self, job_node: Union[JobNode, NullJobNode]):
        err_msg = (
            'left node must be JobNode or NullJobNode instance, '
            f"but got {job_node.__class__.__name__} instance."
        )
        assert isinstance(job_node, BaseJob), err_msg
        self.__left = job_node

    @property
    def right(self) -> Union[JobNode, NullJobNode]:
        return self.__right

    @right.setter
    def right(self, job_node: Union[JobNode, NullJobNode]):
        err_msg = (
            'right node must be JobNode or NullJobNode instance, '
            f"but got {job_node.__class__.__name__} instance."
        )
        assert isinstance(job_node, BaseJob), err_msg
        self.__right = job_node

    def is_done(self) -> bool:
        """Return the job is already completed or not.

        Returns:
            bool: If job is already completed, then return True. Otherwise False.
        """
        return self.p_plus == 0
