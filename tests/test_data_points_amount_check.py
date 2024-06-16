import os
import unittest
from pathlib import Path

import pytest

from netcdfqc.QCnetCDF import QualityControl

data_dir = Path(__file__).parent.parent / 'sample_data'
nc_path = data_dir / 'test_data_points_amount.nc'


class TestDataPointsAmountCheck(unittest.TestCase):
    @pytest.mark.usefixtures("create_nc_data_points_amount_check")
    def test_data_points_amount_check_success(self):
        qc_obj = QualityControl()
        qc_obj.load_netcdf(nc_path)
        qc_obj.add_qc_checks_dict({
            'dimensions': {},
            'variables': {
                'var_1d': {
                    'are_there_enough_data_points_check': {
                        'perform_check': True,
                        'threshold': 10
                    }
                },
                'var_2d': {
                    'are_there_enough_data_points_check': {
                        'perform_check': True,
                        'threshold': 200
                    }
                }
            },
            'global attributes': {},
            'file size': {}
        })
        qc_obj.data_points_amount_check()
        assert qc_obj.logger.info == ["data points amount check for variable 'var_1d': SUCCESS",
                                      "data points amount check for variable 'var_2d': SUCCESS"]
        if os.path.exists(nc_path):
            os.remove(nc_path)

    @pytest.mark.usefixtures("create_nc_data_points_amount_check")
    def test_data_points_amount_check_fail(self):
        qc_obj = QualityControl()
        qc_obj.load_netcdf(nc_path)
        qc_obj.add_qc_checks_dict({
            'dimensions': {},
            'variables': {
                'var_1d': {
                    'are_there_enough_data_points_check': {
                        'perform_check': True,
                        'threshold': 10
                    }
                },
                'var_2d': {
                    'are_there_enough_data_points_check': {
                        'perform_check': True,
                        'threshold': 201
                    }
                }
            },
            'global attributes': {},
            'file size': {}
        })
        qc_obj.data_points_amount_check()
        assert qc_obj.logger.info == ["data points amount check for variable 'var_1d': SUCCESS",
                                      "data points amount check for variable 'var_2d': FAIL"]
        assert qc_obj.logger.errors == [f"data points amount check error: number of data points (200)"
                                        f" for variable 'var_2d' is below the specified threshold (201)"]
        if os.path.exists(nc_path):
            os.remove(nc_path)

    @pytest.mark.usefixtures("create_nc_data_points_amount_check")
    def test_data_points_amount_check_no_such_var(self):
        qc_obj = QualityControl()
        qc_obj.load_netcdf(nc_path)
        qc_obj.add_qc_checks_dict({
            'dimensions': {},
            'variables': {
                'var_3d': {
                    'are_there_enough_data_points_check': {
                        'perform_check': True,
                        'threshold': 1000
                    }
                }
            },
            'global attributes': {},
            'file size': {}
        })
        qc_obj.data_points_amount_check()
        assert not qc_obj.logger.info
        assert not qc_obj.logger.errors
        assert qc_obj.logger.warnings == ["variable 'var_3d' not in nc file"]
        if os.path.exists(nc_path):
            os.remove(nc_path)

    def test_data_points_amount_check_no_nc(self):
        qc_obj = QualityControl()
        qc_obj.add_qc_checks_dict({
            'dimensions': {}, 'variables': {}, 'global attributes': {}, 'file size': {}
        })
        qc_obj.data_points_amount_check()
        assert not qc_obj.logger.info
        assert not qc_obj.logger.warnings
        assert qc_obj.logger.errors == ['data points amount check error: no nc file loaded']
