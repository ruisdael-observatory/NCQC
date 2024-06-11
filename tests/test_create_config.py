"""
Module for testing the automatic creation of config files for specifying checks.

Functions:
- test_create_from_yaml: Test for create_config_dict_from_yaml with default arguments and a mocked yaml2dict function.
- test_create_from_dict_with_arguments: Test for create_config_dict_from_dict with custom arguments.
- test_create_from_dict_fields_list_one_item: Test for create_config_dict_from_dict
    with only one string in the field_name list argument.
- test_create_from_dict_empty: Test for create_config_dict_from_dict with an empty input dictionary.
"""

from pathlib import Path
from unittest.mock import patch

from netcdfqc.create_config import create_config_dict_from_yaml, create_config_dict_from_dict

@patch('netcdfqc.create_config.yaml2dict')
def test_create_from_yaml(mock_yaml2dict):
    """
    Test for create_config_dict_from_yaml with default arguments and a mocked yaml2dict function.
    :param mock_yaml2dict: mock object for yaml2dict to return a specific dictionary
    """
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
            },
            'var2': {
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
            },
            'field_1': {
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
            },
            'field_2': {
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
        },
        'global_attributes': {
            'glattr1': {
                'does_it_exist_check': 'TODO',
                'is_it_empty_check': 'TODO'
            }
        },
        'file_size': {
            'perform_check': 'TODO',
            'lower_bound': 'TODO',
            'upper_bound': 'TODO'
        }
    }

    qc_dict = create_config_dict_from_yaml(path=Path('path'))

    assert qc_dict == expected_dict

def test_create_from_dict_with_arguments():
    """
    Test for create_config_dict_from_dict with custom arguments.
    """
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
        },
        'file_size': {
            'perform_check': 'TODO',
            'lower_bound': 'TODO',
            'upper_bound': 'TODO'
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
            },
            'var2': {
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
            },
            'field_1': {
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
            },
            'field_2': {
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
        },
        'global_attributes': {
            'glattr1': {
                'does_it_exist_check': 'TODO',
                'is_it_empty_check': 'TODO'
            }
        },
        'file_size': {
            'perform_check': 'TODO',
            'lower_bound': 'TODO',
            'upper_bound': 'TODO'
        }
    }

    qc_dict = create_config_dict_from_dict(input_dict=test_dict,
                                           dimensions_name='dims',
                                           variables_name='vars',
                                           global_attributes_name='global_attrs',
                                           field_names=['fields', 'attrs', 'short_name'])

    assert qc_dict == expected_dict

def test_create_from_dict_field_list_one_item():
    """
    Test for create_config_dict_from_dict with only one string in the field_name list argument.
    """
    test_dict = {
        'fields': {
            'field1': 'value1',
            'field2': 'value2'
        }
    }

    expected_dict = {
        'dimensions': {},
        'variables': {
            'field1': {
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
            },
            'field2': {
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
        },
        'global_attributes': {},
        'file_size': {
            'perform_check': 'TODO',
            'lower_bound': 'TODO',
            'upper_bound': 'TODO'
        }
    }

    qc_dict = create_config_dict_from_dict(input_dict=test_dict, field_names=["fields"])

    assert qc_dict == expected_dict

def test_create_from_dict_empty():
    """
    Test for create_config_dict_from_dict with an empty input dictionary.
    """
    test_dict = {}

    expected_dict = {
        'dimensions': {},
        'variables': {},
        'global_attributes': {},
        'file_size': {
            'perform_check': 'TODO',
            'lower_bound': 'TODO',
            'upper_bound': 'TODO'
        }
    }

    qc_dict = create_config_dict_from_dict(input_dict=test_dict)

    assert qc_dict == expected_dict
