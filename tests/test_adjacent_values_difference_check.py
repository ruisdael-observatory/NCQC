"""
Module for testing the functionality of the value_change_rate_check method

Functions:
- test_adjacent_values_difference_check_no_nc: Test for
  adjacent_values_difference_check when no netCDF file is loaded.
- test_adjacent_values_difference_check_success: Test for when
  adjacent_values_difference_check succeeds.
- test_adjacent_values_difference_check_fail: Test for when
  adjacent_values_difference_check fails.
- test_adjacent_values_difference_check_var_not_in_file: Test
  adjacent_values_difference_check when variable is not in file.
"""

import os
from pathlib import Path
import pytest

from ncqc.QCnetCDF import QualityControl

data_dir = Path(__file__).parent.parent / 'sample_data'

adjacent_values_difference_check_dict_success = {
    'dimensions': {
    },
    'variables': {
        'test_pass': {
            'adjacent_values_difference_check': {'over_which_dimension':[0], 'maximum_difference': [1]}
        },
    },
    'global attributes': {
    },
    'file size': {
    }
}

adjacent_values_difference_check_dict_fail = {
    'dimensions': {
    },
    'variables': {
        'test_fail': {
            'adjacent_values_difference_check': {'over_which_dimension':[0], 'maximum_difference': [1]}
        },
    },
    'global attributes': {
    },
    'file size': {
    }
}

adjacent_values_difference_check_var_not_in_nc_dict = {
    'dimensions': {
    },
    'variables': {
        'test_not_in_nc': {
            'adjacent_values_difference_check': {'over_which_dimension':[0], 'maximum_difference': [1]}
        },
    },
    'global attributes': {
    },
    'file size': {
    }
}

def test_adjacent_values_difference_check_no_nc():
    """
    Test for adjacent_values_difference_check when no netCDF file is loaded.
    """
    qc_obj = QualityControl()
    qc_obj.add_qc_checks_dict(adjacent_values_difference_check_dict_success)
    qc_obj.adjacent_values_difference_check()
    assert not qc_obj.logger.info
    assert qc_obj.logger.errors == ['adjacent_values_difference_check error: no nc file loaded']
    assert not qc_obj.logger.warnings


@pytest.mark.usefixtures("create_nc_adjacent_values_difference_check")
def test_adjacent_values_max_allowed_difference_success():
    """
    Test for when adjacent_values_difference_check succeeds.
    """
    qc_obj = QualityControl()

    nc_path = data_dir / 'test_adjacent_values_difference_check.nc'
    qc_obj.load_netcdf(nc_path)

    qc_obj.add_qc_checks_dict(adjacent_values_difference_check_dict_success)

    qc_obj.adjacent_values_difference_check()

    assert qc_obj.logger.info == ["adjacent_values_difference_check for variable 'test_pass'"
                                  " and dimension '0': SUCCESS"]
    assert not qc_obj.logger.errors
    assert not qc_obj.logger.warnings

    if os.path.exists(nc_path):
        os.remove(nc_path)

@pytest.mark.usefixtures("create_nc_adjacent_values_difference_check")
def test_adjacent_values_difference_check_fail():
    """
    Test for when adjacent_values_difference_check fails.
    """
    qc_obj = QualityControl()

    nc_path = data_dir / 'test_adjacent_values_difference_check.nc'
    qc_obj.load_netcdf(nc_path)

    qc_obj.add_qc_checks_dict(adjacent_values_difference_check_dict_fail)

    qc_obj.adjacent_values_difference_check()

    assert qc_obj.logger.info == ["adjacent_values_difference_check for variable 'test_fail' and "
                                  "dimension '0': FAIL"]
    assert len(qc_obj.logger.errors) == 19
    assert not qc_obj.logger.warnings

    if os.path.exists(nc_path):
        os.remove(nc_path)


@pytest.mark.usefixtures("create_nc_adjacent_values_difference_check")
def test_adjacent_values_max_allowed_difference_var_not_in_file():
    """
    Test adjacent_values_difference_check when variable is not in file.
    """
    qc_obj = QualityControl()

    nc_path = data_dir / 'test_adjacent_values_difference_check.nc'
    qc_obj.load_netcdf(nc_path)

    qc_obj.add_qc_checks_dict(adjacent_values_difference_check_var_not_in_nc_dict)

    qc_obj.adjacent_values_difference_check()

    assert not qc_obj.logger.errors
    assert qc_obj.logger.warnings == ['variable \'test_not_in_nc\' not in nc file']

    if os.path.exists(nc_path):
        os.remove(nc_path)





