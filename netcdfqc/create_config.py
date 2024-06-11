"""
Module for creating the base for a config file that can be used for the QualityControl object
by parsing other more general config files.
"""

from pathlib import Path
from typing import List, Dict, Union
import yaml

from netcdfqc.QCnetCDF import yaml2dict

def create_config_dict_from_conf(path: Path,
                                 dimensions_names: str = 'dimensions',
                                 variables_names: str = 'variables',
                                 global_attributes_names: str = 'global_attributes',
                                 min_file_size: int = 0) -> Dict:
    """
    Creates a config file for QC by parsing the given config file.

    :param path: path to the config file to parse
    :param dimension_names: name or list of names of the groups containing the dimensions
    :param variables_names: name or list of names of the groups containing the variables
    :param global_attributes_names: name or list of names of the groups containing the global attributes
    :param path: the minimal file size that the netCDF files should have
    :return: a dictionary which contains the structure for specifying QC checks
    """
    new_checks_dict = yaml2dict(path_qc_checks_file)
    return create_config_file_from_dict(input_dict=new_checks_dict,
                                        dimensions_names=dimensions_names,
                                        variables_names=variables_names,
                                        global_attributes_names=global_attributes_names,
                                        min_file_size=min_file_size)

def create_config_dict_from_dict(input_dict: Dict,
                                 dimensions_names: str = 'dimensions',
                                 variables_names: str = 'variables',
                                 global_attributes_names: str = 'global_attributes',
                                 min_file_size: int = 0) -> Dict:
    """
    Creates a config file for QC by parsing the given dictionary.

    :param dict: the dictionary to parse
    :param dimension_names: name or list of names of the groups containing the dimensions
    :param variables_names: name or list of names of the groups containing the variables
    :param global_attributes_names: name or list of names of the groups containing the global attributes
    :param path: the minimal file size that the netCDF files should have
    :return: a dictionary which contains the structure for specifying QC checks
    """
    qc_dict = {
        'dimensions': {},
        'variables': {},
        'global_attributes': {},
        'min_file_size': min_file_size
    }

    if dimensions_names in list(input_dict.keys()):
        qc_dict['dimensions'].update(input_dict[dimensions_names])

    if variables_names in list(input_dict.keys()):
        qc_dict['variables'].update(input_dict[variables_names])

    if global_attributes_names in list(input_dict.keys()):
        qc_dict['global_attributes'].update(input_dict[global_attributes_names])

    for dim in qc_dict['dimensions']:
        qc_dict['dimensions'][dim] = {
            'does_it_exist_check': 'TODO'
        }

    for var in qc_dict['variables']:
        qc_dict['variables'][var] = {
            'does_it_exist_check': 'TODO',
            'is_it_empty_check': 'TODO',
            'is_data_within_boundaries_check': {
                'perform_check': 'TODO',
                'lower_bound': 'TODO',
                'upper_bound': 'TODO'
            }
        }

    for attr in qc_dict['global_attributes']:
        qc_dict['global_attributes'][attr] = {
            'does_it_exist_check': 'TODO',
            'is_it_empty_check': 'TODO'
        }

    return qc_dict
