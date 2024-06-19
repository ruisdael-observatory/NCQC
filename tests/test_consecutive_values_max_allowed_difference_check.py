"""
Module for testing the functionality of the value_change_rate_check method

Functions:
- test_consecutive_values_max_allowed_difference_check_no_nc: Test for
  consecutive_values_max_allowed_difference_check when no netCDF file is loaded.
- test_consecutive_values_max_allowed_difference_check_success: Test for when
  consecutive_values_max_allowed_difference_check succeeds.
- test_consecutive_values_max_allowed_difference_check_fail: Test for when
  consecutive_values_max_allowed_difference_check fails.
- test_consecutive_values_max_allowed_difference_check_var_not_in_file: Test
  consecutive_values_max_allowed_difference_check when variable is not in file.
"""

import os
from pathlib import Path
import pytest

from netcdfqc.QCnetCDF import QualityControl

data_dir = Path(__file__).parent.parent / 'sample_data'

consecutive_values_max_allowed_difference_check_dict_success = {
    'dimensions': {
    },
    'variables': {
        'test_pass': {
            'consecutive_values_max_allowed_difference_check': {'over_which_dimension':[0], 'maximum_difference': [1]}
        },
    },
    'global attributes': {
    },
    'file size': {
    }
}

consecutive_values_max_allowed_difference_check_dict_fail = {
    'dimensions': {
    },
    'variables': {
        'test_fail': {
            'consecutive_values_max_allowed_difference_check': {'over_which_dimension':[0], 'maximum_difference': [1]}
        },
    },
    'global attributes': {
    },
    'file size': {
    }
}

consecutive_values_max_allowed_difference_check_var_not_in_nc_dict = {
    'dimensions': {
    },
    'variables': {
        'test_not_in_nc': {
            'consecutive_values_max_allowed_difference_check': {'over_which_dimension':[0], 'maximum_difference': [1]}
        },
    },
    'global attributes': {
    },
    'file size': {
    }
}

def test_consecutive_values_max_allowed_difference_check_no_nc():
    """
    Test for consecutive_values_max_allowed_difference_check when no netCDF file is loaded.
    """
    qc_obj = QualityControl()
    qc_obj.add_qc_checks_dict(consecutive_values_max_allowed_difference_check_dict_success)
    qc_obj.consecutive_values_max_allowed_difference_check()
    assert not qc_obj.logger.info
    assert qc_obj.logger.errors == ['consecutive_values_max_allowed_difference_check error: no nc file loaded']
    assert not qc_obj.logger.warnings


@pytest.mark.usefixtures("create_nc_consecutive_values_max_allowed_difference_check")
def test_consecutive_values_max_allowed_difference_success():
    """
    Test for when consecutive_values_max_allowed_difference_check succeeds.
    """
    qc_obj = QualityControl()

    nc_path = data_dir / 'test_consecutive_values_max_allowed_difference_check.nc'
    qc_obj.load_netcdf(nc_path)

    qc_obj.add_qc_checks_dict(consecutive_values_max_allowed_difference_check_dict_success)

    qc_obj.consecutive_values_max_allowed_difference_check()

    assert qc_obj.logger.info == ["consecutive_values_max_allowed_difference_check for variable 'test_pass'"
                                  " and dimension '0': success"]
    assert not qc_obj.logger.errors
    assert not qc_obj.logger.warnings

    if os.path.exists(nc_path):
        os.remove(nc_path)

@pytest.mark.usefixtures("create_nc_consecutive_values_max_allowed_difference_check")
def test_consecutive_values_max_allowed_difference_check_fail():
    """
    Test for when consecutive_values_max_allowed_difference_check fails.
    """
    qc_obj = QualityControl()

    nc_path = data_dir / 'test_consecutive_values_max_allowed_difference_check.nc'
    qc_obj.load_netcdf(nc_path)

    qc_obj.add_qc_checks_dict(consecutive_values_max_allowed_difference_check_dict_fail)

    qc_obj.consecutive_values_max_allowed_difference_check()

    assert qc_obj.logger.info == ["consecutive_values_max_allowed_difference_check for variable 'test_fail' and "
                                  "dimension '0': fail"]
    assert not qc_obj.logger.errors
    assert not qc_obj.logger.warnings

    if os.path.exists(nc_path):
        os.remove(nc_path)


@pytest.mark.usefixtures("create_nc_consecutive_values_max_allowed_difference_check")
def test_consecutive_values_max_allowed_difference_var_not_in_file():
    """
    Test consecutive_values_max_allowed_difference_check when variable is not in file.
    """
    qc_obj = QualityControl()

    nc_path = data_dir / 'test_consecutive_values_max_allowed_difference_check.nc'
    qc_obj.load_netcdf(nc_path)

    qc_obj.add_qc_checks_dict(consecutive_values_max_allowed_difference_check_var_not_in_nc_dict)

    qc_obj.consecutive_values_max_allowed_difference_check()

    assert not qc_obj.logger.errors
    assert qc_obj.logger.warnings == ['variable \'test_not_in_nc\' not in nc file']

    if os.path.exists(nc_path):
        os.remove(nc_path)





