"""
Module for testing the check method from the QualityControl class
"""
import os
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

import pytest

from ncqc.QCnetCDF import QualityControl

data_dir = Path(__file__).parent.parent / 'sample_data'


class TestCheck(unittest.TestCase):
    """
    Test class for the check method from the QualityControl class

     Methods:
    - test_check_no_nc: Test method for when there is no netCDF file loaded
    - test_check_no_such_var: Test method for when a variable specified in the config
      file does not exist in the netCDF file
    - test_check_all_success: Test method for when all checks succeed
    - test_check_all_fail: Test method for when most checks fail
    """

    def test_check_no_nc(self):
        """
        Test method for when there is no netCDF file loaded
        """
        qc_obj = QualityControl()
        qc_obj.check()
        assert not qc_obj.logger.info
        assert not qc_obj.logger.warnings
        assert qc_obj.logger.errors == ['check error: no nc file loaded']

    @pytest.mark.usefixtures("create_nc_data_points_amount_check")
    def test_check_no_such_var(self):
        """
        Test method for when a variable specified in the config file does not exist in the netCDF file
        """
        nc_path = data_dir / 'test_data_points_amount.nc'
        qc_obj = QualityControl()
        qc_obj.load_netcdf(nc_path)
        qc_obj.add_qc_checks_conf(data_dir / 'example_config.yaml')
        qc_obj.check()
        assert qc_obj.logger.warnings == ["variable 'example_variable' not in nc file"]

        if os.path.exists(nc_path):
            os.remove(nc_path)

    @pytest.mark.usefixtures("create_nc_all_checks")
    @patch('ncqc.QCnetCDF.Path.stat', return_value=Mock(st_size=150))
    def test_check_all_success(self, mock_path_stat):
        """
        Test method for when all checks succeed
        :param mock_path_stat: Mock object for the Path.stat call
        """
        nc_path = data_dir / 'test_all_checks.nc'
        qc_obj = QualityControl()
        qc_obj.load_netcdf(nc_path)
        qc_obj.add_qc_checks_dict({
            'dimensions': {'dim_1': {'existence_check': True}},
            'variables': {
                'var_1': {
                    'existence_check': True,
                    'emptiness_check': True,
                    'data_boundaries_check': {'lower_bound': 1, 'upper_bound': 10},
                    'data_points_amount_check': {'minimum': 40},
                    'adjacent_values_difference_check': {
                        'over_which_dimension': [0],
                        'maximum_difference': [9]
                    },
                    'consecutive_identical_values_check': {'maximum': 40}
                },
                'var_2': {
                    'existence_check': True,
                    'emptiness_check': True,
                    'data_boundaries_check': {'lower_bound': 10, 'upper_bound': 19},
                    'data_points_amount_check': {'minimum': 40},
                    'adjacent_values_difference_check': {
                        'over_which_dimension': [0],
                        'maximum_difference': [9]
                    },
                    'consecutive_identical_values_check': {'maximum': 40}
                }
            },
            'global attributes': {
                'attr_1': {
                    'existence_check': True, 'emptiness_check': True
                }
            },
            'file size': {'lower_bound': 100, 'upper_bound': 200}
        })
        qc_obj.check()

        assert qc_obj.logger.info == [
            "file size check: SUCCESS",
            "1/1 checked dimensions exist",
            "2/2 checked variables exist",
            "1/1 checked global attributes exist",
            "2/2 checked variables are fully populated",
            "1/1 checked global attributes have values assigned",
            "data points amount check for variable 'var_1': SUCCESS",
            "data points amount check for variable 'var_2': SUCCESS",
            "boundary check for variable 'var_1': SUCCESS",
            "boundary check for variable 'var_2': SUCCESS",
            "consecutive_identical_values_check for variable 'var_1': SUCCESS",
            "consecutive_identical_values_check for variable 'var_2': SUCCESS",
            "adjacent_values_difference_check for variable 'var_1' and dimension '0': SUCCESS",
            "adjacent_values_difference_check for variable 'var_2' and dimension '0': SUCCESS"
        ]

        if os.path.exists(nc_path):
            os.remove(nc_path)

    @pytest.mark.usefixtures("create_nc_all_checks")
    @patch('ncqc.QCnetCDF.Path.stat', return_value=Mock(st_size=150))
    def test_check_all_fail(self, mock_path_stat):
        """
        Test method for when most checks fail
        :param mock_path_stat: Mock object for the Path.stat call
        """
        nc_path = data_dir / 'test_all_checks.nc'
        qc_obj = QualityControl()
        qc_obj.load_netcdf(nc_path)
        qc_obj.add_qc_checks_dict({
            'dimensions': {'dim_no_such': {'existence_check': True}},
            'variables': {
                'var_1': {
                    'existence_check': True,
                    'emptiness_check': True,
                    'data_boundaries_check': {'lower_bound': 11, 'upper_bound': 21},
                    'data_points_amount_check': {'minimum': 51},
                    'adjacent_values_difference_check': {
                        'over_which_dimension': [0],
                        'maximum_difference': [0]
                    },
                    'consecutive_identical_values_check': {'maximum': 0}
                },
                'var_2': {
                    'existence_check': True,
                    'emptiness_check': True,
                    'data_boundaries_check': {'lower_bound': 1, 'upper_bound': 8},
                    'data_points_amount_check': {'minimum': 51},
                    'adjacent_values_difference_check': {
                        'over_which_dimension': [0],
                        'maximum_difference': [0]
                    },
                    'consecutive_identical_values_check': {'maximum': 0}
                }
            },
            'global attributes': {
                'attr_no_such': {
                    'existence_check': True, 'emptiness_check': True
                }
            },
            'file size': {'lower_bound': 200, 'upper_bound': 300}
        })
        qc_obj.check()

        print(qc_obj.logger.info)

        assert qc_obj.logger.info == [
            "file size check: FAIL",
            "0/1 checked dimensions exist",
            "2/2 checked variables exist",
            "0/1 checked global attributes exist",
            "2/2 checked variables are fully populated",
            "no global attributes were checked for emptiness",
            "data points amount check for variable 'var_1': FAIL",
            "data points amount check for variable 'var_2': FAIL",
            "boundary check for variable 'var_1': FAIL",
            "boundary check for variable 'var_2': FAIL",
            "consecutive_identical_values_check for variable 'var_1': FAIL",
            "consecutive_identical_values_check for variable 'var_2': FAIL",
            "adjacent_values_difference_check for variable 'var_1' and dimension '0': FAIL",
            "adjacent_values_difference_check for variable 'var_2' and dimension '0': FAIL"
        ]

        if os.path.exists(nc_path):
            os.remove(nc_path)
