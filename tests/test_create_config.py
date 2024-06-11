"""
Module for testing the automatic creation of config files for specifying checks.
"""
import unittest
from pathlib import Path
from unittest.mock import patch, Mock

from netcdfqc.create_config import create_config_dict_from_conf, create_config_dict_from_dict

@patch('netcdfqc.create_config.yaml2dict')
def test_replace_qc_checks_conf(mock_yaml2dict):
    mock_yaml2dict.return_value = {
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
        },
        'telegram_fields': {
            '01': {
                'dimensions': 'time',
                'var_attrs': {
                    'long_name': 'telegram field one',
                    'standard_name': 'field_1'
                }
            },
            '02': {
                'dimensions': 'time',
                'var_attrs': {
                    'long_name': 'telegram field two',
                    'standard_name': 'field_2'
                }
            }
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
            },
            'field_1': {
                'does_it_exist_check': 'TODO',
                'is_it_empty_check': 'TODO',
                'is_data_within_boundaries_check': {
                    'perform_check': 'TODO',
                    'lower_bound': 'TODO',
                    'upper_bound': 'TODO'
                }
            },
            'field_2': {
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

    qc_dict = create_config_dict_from_conf(path=Path('path'))

    assert qc_dict == expected_dict

def test_create_from_dict_with_arguments():
    test_dict = {
        'dims': {
            'dim1': 'value1',
            'dim2': 'value2'
        },
        'vars': {
            'var1': 'value1',
            'var2': 'value2'
        },
        'global_attrs': {
            'glattr1': 'value1'
        },
        'fields': {
            '01': {
                'dimensions': 'time',
                'attrs': {
                    'long_name': 'telegram field one',
                    'short_name': 'field_1'
                }
            },
            '02': {
                'dimensions': 'time',
                'attrs': {
                    'long_name': 'telegram field two',
                    'short_name': 'field_2'
                }
            }
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
            },
            'field_1': {
                'does_it_exist_check': 'TODO',
                'is_it_empty_check': 'TODO',
                'is_data_within_boundaries_check': {
                    'perform_check': 'TODO',
                    'lower_bound': 'TODO',
                    'upper_bound': 'TODO'
                }
            },
            'field_2': {
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
        'min_file_size': 1024
    }

    qc_dict = create_config_dict_from_dict(input_dict=test_dict,
                                           dimensions_name='dims',
                                           variables_name='vars',
                                           global_attributes_name='global_attrs',
                                           field_names=['fields', 'attrs', 'short_name'],
                                           min_file_size=1024)

    assert qc_dict == expected_dict

def test_create_from_dict_list_one_item():
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
        },
        'telegram_fields': {
            '01': {
                'dimensions': 'time',
                'var_attrs': {
                    'long_name': 'telegram field one',
                    'standard_name': 'field_1'
                }
            },
            '02': {
                'dimensions': 'time',
                'var_attrs': {
                    'long_name': 'telegram field two',
                    'standard_name': 'field_2'
                }
            }
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

    qc_dict = create_config_dict_from_dict(input_dict=test_dict, variables_name="none", field_names=["variables"])

    assert qc_dict == expected_dict
