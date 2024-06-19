"""
Module for testing the functionality of the max_number_of_consecutive_same_values_check method

Functions:
- test_max_number_of_consecutive_same_values_check_no_nc: Test for max_number_of_consecutive_same_values when no netCDF file is loaded
- test_max_number_of_consecutive_same_values_check_success: Test for when there aren't to many consecutive same values
- test_max_number_of_consecutive_same_values_check_fail: Test for when a variable has to many consecutive same values
- test_max_number_of_consecutive_same_values_var_check_not_in_file: Test checking the max number of consecutive same values of variables
    when variable is not in file

"""

import os
from pathlib import Path
import pytest

from netcdfqc.QCnetCDF import QualityControl

data_dir = Path(__file__).parent.parent / 'sample_data'

max_number_of_consecutive_same_values_check_dict_success = {
    'dimensions': {
    },
    'variables': {
        'test_pass': {
            'max_number_of_consecutive_same_values_check': {'maximum': 50}
        },
    },
    'global attributes': {
    },
    'file size': {
    }
}

max_number_of_consecutive_same_values_check_dict_fail = {
    'dimensions': {
    },
    'variables': {
        'test_fail': {
            'max_number_of_consecutive_same_values_check': {'maximum': 50}
        },
    },
    'global attributes': {
    },
    'file size': {
    }
}

max_number_of_consecutive_same_values_check_var_not_in_nc_dict = {
    'dimensions': {
    },
    'variables': {
        'test_not_in_nc': {
            'max_number_of_consecutive_same_values_check': {'maximum': 50}
        },
    },
    'global attributes': {
    },
    'file size': {
    }
}

def test_max_number_of_consecutive_same_values_check_no_nc():
    """
    Test for max_number_of_consecutive_same_values_check when no netCDF file is loaded.
    """
    qc_obj = QualityControl()
    qc_obj.add_qc_checks_dict(max_number_of_consecutive_same_values_check_dict_success)
    qc_obj.max_number_of_consecutive_same_values_check()
    assert not qc_obj.logger.info
    assert qc_obj.logger.errors == ['max_number_of_consecutive_same_values_check error: no nc file loaded']
    assert not qc_obj.logger.warnings


@pytest.mark.usefixtures("create_nc_max_number_of_consecutive_same_values_check")
def test_max_number_of_consecutive_same_values_check_success():
    """
    Test for when there aren't to many consecutive same values.
    """
    qc_obj = QualityControl()

    nc_path = data_dir / 'test_max_number_of_consecutive_same_values_check.nc'
    qc_obj.load_netcdf(nc_path)

    qc_obj.add_qc_checks_dict(max_number_of_consecutive_same_values_check_dict_success)

    qc_obj.max_number_of_consecutive_same_values_check()

    assert qc_obj.logger.info == ["max_number_of_consecutive_same_values_check for variable 'test_pass': "
    'success']
    assert not qc_obj.logger.errors
    assert not qc_obj.logger.warnings

    if os.path.exists(nc_path):
        os.remove(nc_path)

@pytest.mark.usefixtures("create_nc_max_number_of_consecutive_same_values_check")
def test_max_number_of_consecutive_same_values_check_fail():
    """
    Test for when a variable has to many consecutive same values.
    """
    qc_obj = QualityControl()

    nc_path = data_dir / 'test_max_number_of_consecutive_same_values_check.nc'
    qc_obj.load_netcdf(nc_path)

    qc_obj.add_qc_checks_dict(max_number_of_consecutive_same_values_check_dict_fail)

    qc_obj.max_number_of_consecutive_same_values_check()

    assert qc_obj.logger.info == ["max_number_of_consecutive_same_values_check for variable 'test_fail': fail"]
    assert qc_obj.logger.errors == ["test_fail has 100 consecutive same values 1.0, which is higher than the threshold 50"]
    assert not qc_obj.logger.warnings

    if os.path.exists(nc_path):
        os.remove(nc_path)


@pytest.mark.usefixtures("create_nc_max_number_of_consecutive_same_values_check")
def test_max_number_of_consecutive_same_values_check_var_not_in_file():
    """
    Test checking the max number of consecutive same values of variables
    when variable is not in file.
    """
    qc_obj = QualityControl()

    nc_path = data_dir / 'test_max_number_of_consecutive_same_values_check.nc'
    qc_obj.load_netcdf(nc_path)

    qc_obj.add_qc_checks_dict(max_number_of_consecutive_same_values_check_var_not_in_nc_dict)

    qc_obj.max_number_of_consecutive_same_values_check()

    assert not qc_obj.logger.errors
    assert qc_obj.logger.warnings == ['variable \'test_not_in_nc\' not in nc file']

    if os.path.exists(nc_path):
        os.remove(nc_path)
