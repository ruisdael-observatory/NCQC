"""
Test module for the Quality Control object

Functions:
- test_yaml2dict: Test for the yaml2dict function
"""

import unittest
from pathlib import Path
from unittest.mock import patch

from netcdfqc.QCnetCDF import QualityControl, yaml2dict

data_dir = Path(__file__).parent.parent / 'sample_data'

class TestQualityControl(unittest.TestCase):
    """
    Class for testing the QualityControl object.

    Functions:
    - test_add_qc_checks_conf: Test for adding the required checks by using a config file
    - test_add_qc_checks_dict: Test for adding the required checks by using a dictionary
    - test_add_qc_checks_dict_errors: Test for adding qc checks with an empty dictionary
    - test_replace_qc_checks_conf: Test for replacing the required checks by using a config file
    - test_replace_qc_checks_dict: Test for replacing the required checks by using a dictionary
    - test_load_netcdf: Test for using load_netcdf to set the netCDF attribute
    - test_yaml2dict: Test for loading a yaml file into a dictionary
    """

    @patch('netcdfqc.QCnetCDF.yaml2dict')
    def test_add_qc_checks_conf(self, mock_yaml2dict):
        """
        Test for adding the required checks by using a config file
        :param mock_yaml2dict: mock object for returning a mocked dict with checks
        """
        qc_obj = QualityControl()
        qc_obj.qc_checks_dims = {
            'example_dimension': {'existence': True}
        }
        qc_obj.qc_checks_vars = {
            'example_variable': {
                'existence': True,
                'boundaries': {'do': True, 'lower': 1, 'upper': 2}
            }
        }
        qc_obj.qc_checks_gl_attrs = {'existence': True, 'emptiness': True}

        def my_side_effect(arg):
            if arg == Path('path'):
                new_checks_dict = {
                    'dimensions': {
                        'example_dimension_2': {'existence': False}
                    },
                    'variables': {
                        'example_variable_2': {
                            'existence': False,
                            'boundaries': {'do': True, 'lower': 3, 'upper': 4}
                        }
                    },
                    'global attributes': {
                        'existence': True, 'emptiness': True
                    },
                    'file size': {
                        'perform_check': True,
                        'lower_bound': 0,
                        'upper_bound': 1
                    }
                }
                return new_checks_dict
            return {}

        mock_yaml2dict.side_effect = my_side_effect

        expected_result = {
            'dimensions': {
                'example_dimension': {'existence': True},
                'example_dimension_2': {'existence': False}
            },
            'variables': {
                'example_variable': {
                    'existence': True,
                    'boundaries': {'do': True, 'lower': 1, 'upper': 2}
                },
                'example_variable_2': {
                    'existence': False,
                    'boundaries': {'do': True, 'lower': 3, 'upper': 4}
                }
            },
            'global attributes': {
                'existence': True, 'emptiness': True
            },
            'file size': {
                'perform_check': True,
                'lower_bound': 0,
                'upper_bound': 1
            }
        }

        qc_obj.add_qc_checks_conf(Path('path'))
        assert qc_obj.qc_checks_dims == expected_result['dimensions']
        assert qc_obj.qc_checks_vars == expected_result['variables']
        assert qc_obj.qc_checks_gl_attrs == expected_result['global attributes']
        assert qc_obj.qc_check_file_size == expected_result['file size']

    def test_add_qc_checks_dict(self):
        """
        Test for adding the required checks by using a dictionary
        """
        qc_obj = QualityControl()
        qc_obj.qc_checks_dims = {
            'example_dimension': {'existence': True}
        }
        qc_obj.qc_checks_vars = {
            'example_variable': {
                'existence': True,
                'boundaries': {'do': True, 'lower': 1, 'upper': 2}
            }
        }
        qc_obj.qc_checks_gl_attrs = {'existence': True, 'emptiness': True}

        new_checks = {
            'dimensions': {
                'example_dimension_2': {'existence': False}
            },
            'variables': {
                'example_variable_2': {
                    'existence': False,
                    'boundaries': {'do': True, 'lower': 3, 'upper': 4}
                }
            },
            'global attributes': {
                'existence': True, 'emptiness': True
            },
            'file size': {
                'perform_check': True,
                'lower_bound': 0,
                'upper_bound': 1
            }
        }

        expected_result = {
            'dimensions': {
                'example_dimension': {'existence': True},
                'example_dimension_2': {'existence': False}
            },
            'variables': {
                'example_variable': {
                    'existence': True,
                    'boundaries': {'do': True, 'lower': 1, 'upper': 2}
                },
                'example_variable_2': {
                    'existence': False,
                    'boundaries': {'do': True, 'lower': 3, 'upper': 4}
                }
            },
            'global attributes': {
                'existence': True, 'emptiness': True
            },
            'file size': {
                'perform_check': True,
                'lower_bound': 0,
                'upper_bound': 1
            }
        }

        qc_obj.add_qc_checks_dict(new_checks)

        assert qc_obj.qc_checks_dims == expected_result['dimensions']
        assert qc_obj.qc_checks_vars == expected_result['variables']
        assert qc_obj.qc_checks_gl_attrs == expected_result['global attributes']
        assert qc_obj.qc_check_file_size == expected_result['file size']

    def test_add_qc_checks_dict_errors(self):
        """
        Test for adding qc checks with an empty dictionary
        """
        qc_obj = QualityControl()
        qc_obj.add_qc_checks_dict({})
        assert qc_obj.logger.errors == ['missing dimensions checks in provided config_file/dict'
            , 'missing variables checks in provided config_file/dict'
            , 'missing global attributes checks in provided config_file/dict'
            , 'missing file size check in provided config_file/dict']

    @patch('netcdfqc.QCnetCDF.yaml2dict')
    def test_replace_qc_checks_conf(self, mock_yaml2dict):
        """
        Test for replacing the required checks by using a config file
        :param mock_yaml2dict: mock object for returning a mocked dict with checks
        """
        qc_obj = QualityControl()
        qc_obj.qc_checks_dims = {
            'example_dimension': {'existence': True}
        }
        qc_obj.qc_checks_vars = {
            'example_variable': {
                'existence': True,
                'boundaries': {'do': True, 'lower': 1, 'upper': 2}
            }
        }
        qc_obj.qc_checks_gl_attrs = {'existence': True, 'emptiness': True}
        qc_obj.qc_check_file_size = {
            'file size': {
                'perform_check': True,
                'lower_bound': 0,
                'upper_bound': 1
            }
        }

        new_checks_dict = {
            'dimensions': {
                'example_dimension_2': {'existence': False}
            },
            'variables': {
                'example_variable_2': {
                    'existence': False,
                    'boundaries': {'do': True, 'lower': 3, 'upper': 4}
                }
            },
            'global attributes': {
                'existence': True, 'emptiness': True
            },
            'file size': {
                'perform_check': False,
                'lower_bound': 1,
                'upper_bound': 2
            }
        }

        def my_side_effect(arg):
            if arg == Path('path'):
                return new_checks_dict
            return {}

        mock_yaml2dict.side_effect = my_side_effect

        qc_obj.replace_qc_checks_conf(Path('path'))
        assert qc_obj.qc_checks_dims == new_checks_dict['dimensions']
        assert qc_obj.qc_checks_vars == new_checks_dict['variables']
        assert qc_obj.qc_checks_gl_attrs == new_checks_dict['global attributes']
        assert qc_obj.qc_check_file_size == new_checks_dict['file size']

    def test_replace_qc_checks_dict(self):
        """
        Test for replacing the required checks by using a dictionary
        """
        qc_obj = QualityControl()
        qc_obj.qc_checks_dims = {
            'example_dimension': {'existence': True}
        }
        qc_obj.qc_checks_vars = {
            'example_variable': {
                'existence': True,
                'boundaries': {'do': True, 'lower': 1, 'upper': 2}
            }
        }

        new_checks_dict = {
            'dimensions': {
                'example_dimension_2': {'existence': False}
            },
            'variables': {
                'example_variable_2': {
                    'existence': False,
                    'boundaries': {'do': True, 'lower': 3, 'upper': 4}
                }
            },
            'global attributes': {
                'existence': True, 'emptiness': True
            },
            'file size': {
                'perform_check': True,
                'lower_bound': 0,
                'upper_bound': 1
            }
        }

        qc_obj.replace_qc_checks_dict(new_checks_dict)
        assert qc_obj.qc_checks_dims == new_checks_dict['dimensions']
        assert qc_obj.qc_checks_vars == new_checks_dict['variables']
        assert qc_obj.qc_checks_gl_attrs == new_checks_dict['global attributes']
        assert qc_obj.qc_check_file_size == new_checks_dict['file size']

    @patch('netcdfqc.QCnetCDF.netCDF4.Dataset')
    def test_load_netcdf(self, mock_dataset):
        """
        Test for using load_netcdf to set the netCDF attribute
        :param mock_dataset: mock object for the Dataset function
        """
        qc_obj = QualityControl()
        qc_obj.load_netcdf('path')
        mock_dataset.assert_called_once_with('path')


def test_yaml2dict():
    """
    Test for the yaml2dict function
    """
    res = yaml2dict(Path(__file__).parent.parent / 'sample_data/example_config.yaml')
    assert res == {
        'dimensions': {'example_dimension': {'does_it_exist_check': True}},
        'variables': {
            'example_variable': {
                'does_it_exist_check': True,
                'is_data_within_boundaries_check': {
                    'perform_check': True,
                    'lower_bound': 0,
                    'upper_bound': 1
                },
                'are_there_enough_data_points_check': {'perform_check': True, 'threshold': 100},
                'do_values_change_at_acceptable_rate_check': {
                    'perform_check': True,
                    'acceptable_difference': 1
                },
                'is_value_constant_for_too_long_check': {
                    'perform_check': True,
                    'threshold': 10,
                    'over_which_dimensions': [0, 1, 2]
                }
            }
        },
        'global attributes': {'example_gl_attr': {
            'does_it_exist_check': True,
            'is_it_empty_check': True
        }},
        'file size': {
            'perform_check': True,
            'lower_bound': 0,
            'upper_bound': 1
        }
    }
