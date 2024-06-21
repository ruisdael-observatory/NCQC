"""
Module for testing the automatic creation of config dicts for specifying checks.

 Functions:
- test_create_from_yaml: Test for create_config_dict_from_yaml with default arguments and a mocked yaml2dict function.
- test_create_from_dict_with_arguments: Test for create_config_dict_from_dict with custom arguments.
- test_create_from_dict_multiple_other_variables: Test for create_config_dict_from_dict
    with multiple other variable names specified.
- test_create_from_dict_one_string_other_variables: Test for create_config_dict_from_dict
    with only one string in the other_variables_names list argument.
- test_create_from_dict_empty_other_variables: Test for create_config_dict_from_dict
    with an empty input dictionary and empty other_variable_name_paths list argument.
"""

from pathlib import Path
from unittest.mock import patch

from ncqc.create_config import create_config_dict_from_yaml, create_config_dict_from_dict


@patch('ncqc.create_config.yaml2dict')
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
        }
    }

    expected_dict = {
        'dimensions': {
            'dim1': {'existence_check': 'TODO'},
            'dim2': {'existence_check': 'TODO'}
        },
        'variables': {
            'var1': {
                'existence_check': 'TODO',
                'emptiness_check': 'TODO',
                'data_boundaries_check': {
                    'perform_check': 'TODO',
                    'lower_bound': 'TODO',
                    'upper_bound': 'TODO'
                },
                'data_points_amount_check': {
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
                'existence_check': 'TODO',
                'emptiness_check': 'TODO',
                'data_boundaries_check': {
                    'perform_check': 'TODO',
                    'lower_bound': 'TODO',
                    'upper_bound': 'TODO'
                },
                'data_points_amount_check': {
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
                'existence_check': 'TODO',
                'emptiness_check': 'TODO'
            }
        },
        'file_size': {
            'perform_check': 'TODO',
            'lower_bound': 'TODO',
            'upper_bound': 'TODO'
        }
    }

    qc_dict = create_config_dict_from_yaml(path=Path('path'), )

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
        }
    }

    expected_dict = {
        'dimensions': {
            'dim1': {'existence_check': 'TODO'},
            'dim2': {'existence_check': 'TODO'}
        },
        'variables': {
            'var1': {
                'existence_check': 'TODO',
                'emptiness_check': 'TODO',
                'data_boundaries_check': {
                    'perform_check': 'TODO',
                    'lower_bound': 'TODO',
                    'upper_bound': 'TODO'
                },
                'data_points_amount_check': {
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
                'existence_check': 'TODO',
                'emptiness_check': 'TODO',
                'data_boundaries_check': {
                    'perform_check': 'TODO',
                    'lower_bound': 'TODO',
                    'upper_bound': 'TODO'
                },
                'data_points_amount_check': {
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
                'existence_check': 'TODO',
                'emptiness_check': 'TODO',
                'data_boundaries_check': {
                    'perform_check': 'TODO',
                    'lower_bound': 'TODO',
                    'upper_bound': 'TODO'
                },
                'data_points_amount_check': {
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
                'existence_check': 'TODO',
                'emptiness_check': 'TODO',
                'data_boundaries_check': {
                    'perform_check': 'TODO',
                    'lower_bound': 'TODO',
                    'upper_bound': 'TODO'
                },
                'data_points_amount_check': {
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
                'existence_check': 'TODO',
                'emptiness_check': 'TODO'
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
                                           other_variable_name_paths=[['fields', 'attrs', 'short_name']])

    assert qc_dict == expected_dict


def test_create_from_dict_multiple_other_variables():
    """
    Test for create_config_dict_from_dict with multiple other variable names specified.
    """
    test_dict = {
        'vars': {
            'var1': 'value1',
            'var2': 'value2'
        },
        'fields': {
            'field1': 'value1',
            'field2': 'value2'
        }
    }

    expected_dict = {
        'dimensions': {},
        'variables': {
            'var1': {
                'existence_check': 'TODO',
                'emptiness_check': 'TODO',
                'data_boundaries_check': {
                    'perform_check': 'TODO',
                    'lower_bound': 'TODO',
                    'upper_bound': 'TODO'
                },
                'data_points_amount_check': {
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
                'existence_check': 'TODO',
                'emptiness_check': 'TODO',
                'data_boundaries_check': {
                    'perform_check': 'TODO',
                    'lower_bound': 'TODO',
                    'upper_bound': 'TODO'
                },
                'data_points_amount_check': {
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
            'field1': {
                'existence_check': 'TODO',
                'emptiness_check': 'TODO',
                'data_boundaries_check': {
                    'perform_check': 'TODO',
                    'lower_bound': 'TODO',
                    'upper_bound': 'TODO'
                },
                'data_points_amount_check': {
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
                'existence_check': 'TODO',
                'emptiness_check': 'TODO',
                'data_boundaries_check': {
                    'perform_check': 'TODO',
                    'lower_bound': 'TODO',
                    'upper_bound': 'TODO'
                },
                'data_points_amount_check': {
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

    qc_dict = create_config_dict_from_dict(input_dict=test_dict, variables_name="",
                                           other_variable_name_paths=[["vars"], ["fields"]])

    assert qc_dict == expected_dict


def test_create_from_dict_one_string_other_variables():
    """
    Test for create_config_dict_from_dict with only one string in the other_variables_names list argument.
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
                'existence_check': 'TODO',
                'emptiness_check': 'TODO',
                'data_boundaries_check': {
                    'perform_check': 'TODO',
                    'lower_bound': 'TODO',
                    'upper_bound': 'TODO'
                },
                'data_points_amount_check': {
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
                'existence_check': 'TODO',
                'emptiness_check': 'TODO',
                'data_boundaries_check': {
                    'perform_check': 'TODO',
                    'lower_bound': 'TODO',
                    'upper_bound': 'TODO'
                },
                'data_points_amount_check': {
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

    qc_dict = create_config_dict_from_dict(input_dict=test_dict, other_variable_name_paths=[["fields"]])

    assert qc_dict == expected_dict


def test_create_from_dict_empty_other_variables():
    """
    Test for create_config_dict_from_dict with an empty input dictionary
    and empty other_variable_name_paths list argument.
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

    qc_dict = create_config_dict_from_dict(input_dict=test_dict, other_variable_name_paths=[[]])

    assert qc_dict == expected_dict
