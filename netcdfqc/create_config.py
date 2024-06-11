"""
Module for creating the base for a config file that can be used for the QualityControl object
by parsing other more general config files.

Functions:
- create_config_dict_from_conf: Parses the given config file to create a dictionary which can be used for QC
- create_config_dict_from_dict: Parses the given dictionary to create a dictionary which can be used for QC
"""

from pathlib import Path
from typing import List, Dict, Union
import yaml

from netcdfqc.QCnetCDF import yaml2dict

def create_config_dict_from_conf(path: Path,
                                 dimensions_name: str = 'dimensions',
                                 variables_name: str = 'variables',
                                 global_attributes_name: str = 'global_attributes',
                                 field_names: List[str] = ['telegram_fields', 'var_attrs', 'standard_name'],
                                 min_file_size: int = 0) -> Dict:
    """
    Creates a config file for QC by parsing the given config file.

    :param path: path to the config file to parse
    :param dimension_names: name of the groups containing the dimensions
    :param variables_name: name of the groups containing the variables
    :param global_attributes_name: name of the groups containing the global attributes
    :param path: the minimal file size that the netCDF files should have
    :return: a dictionary which contains the structure for specifying QC checks
    """
    new_checks_dict = yaml2dict(path)
    return create_config_dict_from_dict(input_dict=new_checks_dict,
                                        dimensions_name=dimensions_name,
                                        variables_name=variables_name,
                                        global_attributes_name=global_attributes_name,
                                        field_names=field_names,
                                        min_file_size=min_file_size)

def create_config_dict_from_dict(input_dict: Dict,
                                 dimensions_name: str = 'dimensions',
                                 variables_name: str = 'variables',
                                 global_attributes_name: str = 'global_attributes',
                                 field_names: List[str] = ['telegram_fields', 'var_attrs', 'standard_name'],
                                 min_file_size: int = 0) -> Dict:
    """
    Creates a config file for QC by parsing the given dictionary.

    :param dict: the dictionary to parse
    :param dimension_names: name of the groups containing the dimensions
    :param variables_name: name of the groups containing the variables
    :param global_attributes_name: name of the groups containing the global attributes
    :param field_names: a list of names to follow to get the names of field variables
    :param min_file_size: the minimal file size that the netCDF files should have
    :return: a dictionary which contains the structure for specifying QC checks
    """
    qc_dict = {
        'dimensions': {},
        'variables': {},
        'global_attributes': {},
        'min_file_size': min_file_size
    }

    # Add the dimensions to the dimensions group of the dictionary
    if dimensions_name in list(input_dict.keys()):
        qc_dict['dimensions'].update(input_dict[dimensions_name])

    # Add the variables to the variables group of the dictionary
    if variables_name in list(input_dict.keys()):
        qc_dict['variables'].update(input_dict[variables_name])

    # Add the (telegram_)fields to the variables group of the dictionary
    if field_names[0] in list(input_dict.keys()):
        # If there is just one item in the list, add all fields within the group which that string defines
        if len(field_names) == 1:
            qc_dict['variables'].update(input_dict[field_names[0]])
        # Individually go through the fields of that group
        else:
            for field in input_dict[field_names[0]]:
                field_name = input_dict[field_names[0]][field]

                i = 1
                # Use the remaining strings in the list as a "path" to get to the name
                while i < len(field_names):
                    field_name = field_name[field_names[i]]
                    i += 1
                    print(len(dimensions_name))

                qc_dict['variables'].update({field_name: {}})

    # Add the global attributes to the global attributes group of the dictionary
    if global_attributes_name in list(input_dict.keys()):
        qc_dict['global_attributes'].update(input_dict[global_attributes_name])

    # Give every dimension the setup for potentially applicable checks with "TO DO" for values
    for dim in qc_dict['dimensions']:
        qc_dict['dimensions'][dim] = {
            'does_it_exist_check': 'TODO'
        }

    # Give every variable the setup for potentially applicable checks with "TO DO" for values
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

    # Give every global attribute the setup for potentially applicable checks with "TO DO" for values
    for attr in qc_dict['global_attributes']:
        qc_dict['global_attributes'][attr] = {
            'does_it_exist_check': 'TODO',
            'is_it_empty_check': 'TODO'
        }

    return qc_dict
