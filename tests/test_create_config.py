"""
Module for testing the automatic creation of config files for specifying checks.
"""
import unittest
from unittest.mock import patch, Mock

from netcdfqc.create_config import create_config_dict_from_dict

def test_create_dict_success():
    test_dict = {
        'dimensions': {
            'dim1': 'value1',
            'dim2': 'value2'
        },
        'variables': {
            'var1': 'value1',
            'var2': 'value2'
        },
        'global_attributes': {
            'glattr1': 'value1'
        }
    }

    expected_dict = {
        'dimensions': {
            'dim1': {'does_it_exist_check': 'TODO'},
            'dim2': {'does_it_exist_check': 'TODO'}
        },
        'variables': {
            'var1': {
                'does_it_exist_check': 'TODO',
                'is_it_empty_check': 'TODO',
                'is_data_within_boundaries_check': {
                    'perform_check': 'TODO',
                    'lower_bound': 'TODO',
                    'upper_bound': 'TODO'
                }
            },
            'var2': {
                'does_it_exist_check': 'TODO',
                'is_it_empty_check': 'TODO',
                'is_data_within_boundaries_check': {
                    'perform_check': 'TODO',
                    'lower_bound': 'TODO',
                    'upper_bound': 'TODO'
                }
            }
        },
        'global_attributes': {
            'glattr1': {
                'does_it_exist_check': 'TODO',
                'is_it_empty_check': 'TODO'
            }
        },
        'min_file_size': 0
    }

    qc_dict = create_config_dict_from_dict(input_dict=test_dict)

    print(qc_dict)

    assert qc_dict == expected_dict
