import unittest
from pathlib import Path
from unittest.mock import patch

from netcdfqc.QCnetCDF import QualityControl, yaml2dict

class TestQualityControl(unittest.TestCase):

    @patch('netcdfqc.QCnetCDF.yaml2dict')
    def test_add_qc_checks_conf(self, mock_yaml2dict):
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
            }
        }

        qc_obj.add_qc_checks_conf(Path('path'))
        assert qc_obj.qc_checks_dims == expected_result['dimensions']
        assert qc_obj.qc_checks_vars == expected_result['variables']
        assert qc_obj.qc_checks_gl_attrs == expected_result['global attributes']

    def test_add_qc_checks_dict(self):
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
            }
        }

        qc_obj.add_qc_checks_dict(new_checks)

        assert qc_obj.qc_checks_dims == expected_result['dimensions']
        assert qc_obj.qc_checks_vars == expected_result['variables']
        assert qc_obj.qc_checks_gl_attrs == expected_result['global attributes']

    @patch('netcdfqc.QCnetCDF.yaml2dict')
    def test_replace_qc_checks_conf(self, mock_yaml2dict):
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

    def test_replace_qc_checks_dict(self):
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
            }
        }

        qc_obj.replace_qc_checks_dict(new_checks_dict)
        assert qc_obj.qc_checks_dims == new_checks_dict['dimensions']
        assert qc_obj.qc_checks_vars == new_checks_dict['variables']
        assert qc_obj.qc_checks_gl_attrs == new_checks_dict['global attributes']

    @patch('netcdfqc.QCnetCDF.netCDF4.Dataset')
    def test_load_netcdf(self, mock_dataset):
        qc_obj = QualityControl()
        qc_obj.load_netcdf('path')
        mock_dataset.assert_called_once_with('path')

    def test_yaml2dict(self):
        res = yaml2dict(Path(__file__).parent.parent / 'sample_data' / 'example_config.yaml')
        assert res == {
            'dimensions': {'example_dimension': {'does_it_exist': True}},
            'variables': {
                'example_variable': {
                    'does_it_exist_check': True,
                    'is_data_within_boundaries_check': {
                        'perform_check': True,
                        'lower_bound': 0,
                        'upper_bound': 1
                    }
                }
            },
            'global attributes': {'example_gl_attr': {
                'does_it_exist_check': True,
                'is_it_empty_check': True
            }}
        }

class TestExistenceCheck(unittest.TestCase):

    def test_existence_check(self):
        qc_obj = QualityControl()
        qc_obj.add_qc_checks_conf(Path(__file__).parent.parent / 'sample_data' / 'example_config_existence.yaml')
        qc_obj.existence_check(Path(__file__).parent.parent / 'sample_data' / '20240530_Green_Village-GV_PAR008.nc')

        expected_errors = ['dimension "bad_dimension" should exist but it does not',
                           'variable "bad_variable" should exist but it does not',
                           'global attribute "bad_attribute" should exist but it does not']

        expected_warnings = []

        expected_info = ['2/3 checked dimensions exist',
                         '3/4 checked variables exist',
                         '2/3 checked global attributes exist']

        assert qc_obj.logger.errors == expected_errors
        assert qc_obj.logger.warnings == expected_warnings
        assert qc_obj.logger.info == expected_info

    def test_existence_check_all_false(self):
        qc_obj = QualityControl()

        qc_obj.qc_checks_dims = {
            'example_dimension': {'does_it_exist_check': False}
        }
        qc_obj.qc_checks_vars = {
            'example_variable': {'does_it_exist_check': False}
        }
        qc_obj.qc_checks_gl_attrs = {
            'example_attribute': {'does_it_exist_check': False}
        }

        qc_obj.existence_check(Path(__file__).parent.parent / 'sample_data' / '20240530_Green_Village-GV_PAR008.nc')

        expected_errors = []

        expected_warnings = []

        expected_info = ['no dimensions were checked',
                         'no variables were checked',
                         'no global attributes were checked']

        assert qc_obj.logger.errors == expected_errors
        assert qc_obj.logger.warnings == expected_warnings
        assert qc_obj.logger.info == expected_info
