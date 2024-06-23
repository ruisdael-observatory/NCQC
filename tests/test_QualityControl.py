"""
Test module for the Quality Control object

 Functions:
- test_yaml2dict: Test for the yaml2dict function
"""

import unittest
from pathlib import Path
from unittest.mock import patch, Mock

from ncqc.QCnetCDF import QualityControl, yaml2dict

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

    @patch('ncqc.QCnetCDF.yaml2dict')
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

    @patch('ncqc.QCnetCDF.yaml2dict')
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

    @patch('ncqc.QCnetCDF.netCDF4.Dataset')
    def test_load_netcdf(self, mock_dataset):
        """
        Test for using load_netcdf to set the netCDF attribute
        :param mock_dataset: mock object for the Dataset function
        """
        qc_obj = QualityControl()
        qc_obj.load_netcdf('path')
        mock_dataset.assert_called_once_with('path')

    @patch('ncqc.log.date')
    @patch('ncqc.log.datetime')
    @patch('ncqc.QCnetCDF.Path.stat', return_value=Mock(st_size=15000))
    def test_create_report(self, mock_path_stat, mock_datetime, mock_date):
        """
        Test for the create_report method from the QualityControl class
        :param mock_path_stat: Mock object for the Path.stat call
        :param mock_datetime: Mock object for the datetime call
        :param mock_date: Mock object fot the date call
        """
        mock_date_today = Mock()
        mock_date_today.strftime.return_value = "24-05-1914"
        mock_date.today.return_value = mock_date_today

        mock_datetime_now = Mock()
        mock_datetime_now.strftime.return_value = "19:14:00"
        mock_datetime.now.return_value = mock_datetime_now

        qc_obj = QualityControl()
        qc_obj.add_qc_checks_conf(data_dir / 'example_config.yaml')
        mock_nc = Mock()
        mock_nc.filepath.return_value = 'dummy/path'
        qc_obj.nc = mock_nc

        first_report = qc_obj.file_size_check().create_report()

        mock_path_stat.return_value = Mock(st_size=9000)

        second_report = qc_obj.file_size_check().create_report()

        mock_path_stat.return_value = Mock(st_size=15000)

        all_reports = qc_obj.file_size_check().create_report(get_all_reports=True)

        expected_first_report = {
            'report_date': "24-05-1914",
            'report_time': "19:14:00",
            'errors': [],
            'warnings': [],
            'info': ['file size check: SUCCESS']
        }

        expected_second_report = {
            'report_date': "24-05-1914",
            'report_time': "19:14:00",
            'errors': ['file size check error: size of loaded file (9000 bytes)'
                       'is out of bounds for bounds: [10000,20000]'],
            'warnings': [],
            'info': ['file size check: FAIL']
        }

        assert first_report == expected_first_report
        assert second_report == expected_second_report
        assert all_reports == [expected_first_report, expected_second_report, expected_first_report]


def test_yaml2dict():
    """
    Test for the yaml2dict function
    """
    res = yaml2dict(Path(__file__).parent.parent / 'sample_data/example_config.yaml')
    assert res == {
        'dimensions': {'example_dimension': {'existence_check': True}},
        'variables': {
            'example_variable': {
                'existence_check': True,
                'emptiness_check': True,
                'data_boundaries_check': {
                    'lower_bound': 0,
                    'upper_bound': 1
                },
                'data_points_amount_check': {'minimum': 100},
                'adjacent_values_difference_check': {
                    'over_which_dimension': [0],
                    'maximum_difference': [1]
                },
                'consecutive_identical_values_check': {
                    'maximum': 25
                },
                'expected_dimensions_check': {
                    'expected_dimensions': ['time', 'velocity_classes']
                }
            }
        },
        'global attributes': {'example_gl_attr': {
            'existence_check': True,
            'emptiness_check': True
        }},
        'file size': {
            'lower_bound': 10000,
            'upper_bound': 20000
        }
    }
