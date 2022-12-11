# -*- coding: utf-8 -*-
from __future__ import annotations
import dataclasses
import json
import os
import sys
from typing import Any, Dict, List, NewType, Optional

from .jsp import Operation, Job, JSP


JobName = NewType('JobName', str)

HOMEDIR = os.path.dirname(__file__)


@dataclasses.dataclass
class JSPMetaData(object):
    """Meta data for JSP instance"""
    n_jobs: int
    n_machines: int
    instance_path: str
    name: str = 'JSP-instance'
    ub: Optional[int] = None
    lb: Optional[int] = None
    optimum: Optional[int] = None

    @staticmethod
    def instantiate_from(meta_data_dict: Dict[str, Any]) -> JSPMetaData:
        """Create JSPMetaData instance from valid dict

        Args:
            meta_data_dict (Dict[str, Any]):
                Valid dict containing meta data.

        Returns:
            JSPMetaData:
                Meta data object of JSP.
        """
        assert 'n_jobs' in meta_data_dict, "'n_jobs' must be included in meta_data_dict"
        assert 'n_machines' in meta_data_dict, "'n_machines' must be included in meta_data_dict"
        assert 'instance_path' in meta_data_dict, "'instance_path' must be included in meta_data_dict"
        assert os.path.isfile(os.path.join(HOMEDIR, meta_data_dict['instance_path'])), "instance file doesn't exists."
        return JSPMetaData(**meta_data_dict)

    def parse_instancefile(self) -> JSPInstance:
        """Parse instance file and create 'JSPInstance' instance
        """
        jsp = JSP()

        abspath = os.path.join(HOMEDIR, self.instance_path)
        with open(abspath) as instance_file:
            # skip first line
            instance_file.readline()

            for job_idx, line in enumerate(instance_file):
                if not line:
                    # last line of instance file
                    break

                job = Job(name=f"job{job_idx}")
                elements = line.strip().split()
                try:
                    elements = [int(element) for element in elements]
                except ValueError:
                    sys.exit(f"InvalidFileFormat: {self.instance_path}")

                for i in range(0, 2 * self.n_machines, 2):
                    machine_idx, processing_time = elements[i], elements[i + 1]
                    job.append(Operation(
                        processed_by=machine_idx,
                        p=processing_time,
                        name=f"O_{job_idx}{i//2}"
                    ))
                jsp.append(job)

        return JSPInstance(jsp=jsp, meta_data=self)


@dataclasses.dataclass
class JSPInstance(object):
    """JSP Instance class"""
    jsp: JSP
    meta_data: JSPMetaData

    def __str__(self):
        return self.meta_data.name

    def __repr__(self):
        return self.meta_data.__repr__()

    def is_already_solved(self):
        return self.meta_data.optimum is not None


class JSPInstanceLoader(object):
    """Loader of JSP Instance"""

    def __init__(self, meta_data_json_file: str = './instance_meta_data.json'):
        self.__all_meta_data = dict()

        abspath = os.path.join(HOMEDIR, meta_data_json_file)
        with open(abspath) as meta_data_file:
            meta_data_list = json.load(meta_data_file)
        for meta_data in meta_data_list:
            self.__all_meta_data[meta_data['name']] = JSPMetaData.instantiate_from(meta_data_dict=meta_data)

    def available_instance_names(self) -> List[str]:
        """Return the list of available instance names

        Returns:
            List[str]: list of available instance names
        """
        return list(self.__all_meta_data.keys())

    def is_available_instance(self, instance_name: str) -> bool:
        """Determine if given instance is available or not

        Args:
            instance_name (str): The instance name.

        Returns:
            is_available (bool): if 'instance_name' is available, then True. Otherwise False.
        """
        is_available = instance_name in self.available_instance_names()
        return is_available

    def load(self, instance_name: str) -> JSPInstance:
        """Load JSP instance

        Args:
            instance_name (str): The instance name.

        Returns:
            [JSPInstance]: The representation of given JSP instance
        """
        err_msg = f"Instance '{instance_name}' is not available."
        assert self.is_available_instance(instance_name), err_msg

        meta_data = self.__all_meta_data[instance_name]
        return meta_data.parse_instancefile()

    def show_instance_details(self, instance_name: Optional[str] = None):
        """Show about every JSP instance's difficulty
        """
        if instance_name is None:
            meta_data_list = self.__all_meta_data.values()
        else:
            err_msg = f"Instance '{instance_name}' is not available."
            assert self.is_available_instance(instance_name), err_msg
            meta_data_list = [self.__all_meta_data[instance_name]]

        print(f"{'*'*50}")
        print('name n_jobs n_machines ub lb optimum')
        for meta_data in meta_data_list:
            print(
                meta_data.name,
                meta_data.n_jobs,
                meta_data.n_machines,
                meta_data.ub,
                meta_data.lb,
                meta_data.optimum
            )
        print(f"{'*'*50}")
