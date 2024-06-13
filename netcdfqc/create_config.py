"""
Module for creating the base for a config file that can be used for the QualityControl object
by parsing other more general config files.

The functions in this module can be used by specifying either the path to a .yml file or a dictionary
and specifying the names of the groups containing the dimensions, variables and global attributes
via dimensions_name, variables_name, and global_attributes_names.

If there are multiple groups of variables stored in different ways, other_variable_name_paths can be used.
This takes a list of lists of strings, each of which indicates the 'path' to the names of a variables.
For example, with the below structure, ['telegram_fields'] would result in '01' getting added as a variable
since that's the name of each field, but then making it ['telegram_fields']['var_attrs']['standard_name']
would result in 'rain_intensity' getting added as a variable.

telegram_fields:
    '01':                 
        var_attrs:
            standard_name: 'rain_intensity'


Functions:
- create_config_dict_from_yaml: Parses the given config file to create a dictionary which can be used for QC
- create_config_dict_from_dict: Parses the given dictionary to create a dictionary which can be used for QC
"""

from pathlib import Path
from typing import List, Dict

from netcdfqc.QCnetCDF import yaml2dict

def create_config_dict_from_yaml(path: Path, # pylint: disable=dangerous-default-value
                                 dimensions_name: str = 'dimensions',
                                 variables_name: str = 'variables',
                                 global_attributes_name: str = 'global_attributes',
                                 other_variable_name_paths: List[List[str]] = [['telegram_fields']]):
    """
    Parses the given yaml file to create a dictionary which can be used for QC

    :param path: path to the config file to parse
    :param dimension_names: name of the groups containing the dimensions
    :param variables_name: name of the groups containing the variables
    :param global_attributes_name: name of the groups containing the global attributes
    :return: a dictionary which contains the structure for specifying QC checks,
        where the specific values still need to be filled in
    """
    new_checks_dict = yaml2dict(path)
    return create_config_dict_from_dict(input_dict=new_checks_dict,
                                        dimensions_name=dimensions_name,
                                        variables_name=variables_name,
                                        global_attributes_name=global_attributes_name,
                                        other_variable_name_paths=other_variable_name_paths)

def create_config_dict_from_dict(input_dict: Dict, # pylint: disable=dangerous-default-value
                                 dimensions_name: str = 'dimensions',
                                 variables_name: str = 'variables',
                                 global_attributes_name: str = 'global_attributes',
                                 other_variable_name_paths: List[List[str]] = [['telegram_fields']]) -> Dict:
    """
    Creates a config dict for QC by parsing the given dictionary.

    :param dict: the dictionary to parse
    :param dimension_names: name of the groups containing the dimensions
    :param variables_name: name of the groups containing the variables
    :param global_attributes_name: name of the groups containing the global attributes
    :param other_variable_name_paths: a list of names to follow to get the names of field variables
    :return: a dictionary which contains the structure for specifying QC checks,
        where the specific values still need to be filled in
    """

    qc_dict = {
        'dimensions': {},
        'variables': {},
        'global_attributes': {},
        'file_size': {
            'perform_check': 'TODO',
            'lower_bound': 'TODO',
            'upper_bound': 'TODO'
        }
    }

    # Add the dimensions to the dimensions group of the dictionary
    if dimensions_name in list(input_dict.keys()):
        qc_dict['dimensions'].update(input_dict[dimensions_name])

    # Add the variables to the variables group of the dictionary
    if variables_name in list(input_dict.keys()):
        qc_dict['variables'].update(input_dict[variables_name])

    # Loop over all specified other variables names
    for variable_name_path in other_variable_name_paths:
        # Add the variable to the variables group of the dictionary
        if len(variable_name_path) > 0 and variable_name_path[0] in list(input_dict.keys()):
            # If there is just one item in the list, add all fields within the group which that string defines
            if len(variable_name_path) == 1:
                qc_dict['variables'].update(input_dict[variable_name_path[0]])
            # Individually go through the fields of that group
            else:
                for field in input_dict[variable_name_path[0]]:
                    field_name = input_dict[variable_name_path[0]][field]

                    i = 1
                    # Use the remaining strings in the list as a "path" to get to the name
                    while i < len(variable_name_path):
                        field_name = field_name[variable_name_path[i]]
                        i += 1

                    qc_dict['variables'].update({field_name: {}})

    # Add the global attributes to the global attributes group of the dictionary
    if global_attributes_name in list(input_dict.keys()):
        qc_dict['global_attributes'].update(input_dict[global_attributes_name])

    # Give every dimension the setup for potentially applicable checks with "TO DO" for values
    for dim in qc_dict['dimensions']:
        qc_dict['dimensions'][dim] = {
            'does_it_exist_check': 'TODO'
        }

    # Give every variable the setup for potentially applicable checks with "TO DO" for values,
    # which have to be manually edited
    for var in qc_dict['variables']:
        qc_dict['variables'][var] = {
            'does_it_exist_check': 'TODO',
            'is_it_empty_check': 'TODO',
            'is_data_within_boundaries_check': {
                'perform_check': 'TODO',
                'lower_bound': 'TODO',
                'upper_bound': 'TODO'
            },
            'are_there_enough_data_points_check': {
                'perform_check': 'TODO',
                'threshold': 'TODO',
                'dimension': 'TODO'
            },
            'do_values_change_at_acceptable_rate_check': {
                'perform_check': 'TODO',
                'acceptable_difference': 'TODO'
            },
            'is_value_constant_for_too_long_check': {
                'perform_check': 'TODO',
                'threshold': 'TODO'
            }
        }

    # Give every global attribute the setup for potentially applicable checks with "TO DO" for values
    for attr in qc_dict['global_attributes']:
        qc_dict['global_attributes'][attr] = {
            'does_it_exist_check': 'TODO',
            'is_it_empty_check': 'TODO'
        }

    return qc_dict
