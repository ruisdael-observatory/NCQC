"""
Module for testing the functionality of the boundaries check

Functions:
- test_boundary_check_no_nc: Test for the boundaries check when no netCDF file is loaded
- test_boundary_check_success: Test for the boundaries check when all checks are successful
- test_boundary_check_fail: Test for the boundaries check when a check fails
- test_boundary_check_wrong_var_name: Test for the boundaries check when a variable to be
checked is not in the loaded netCDF file
- test_boundary_check_omit_a_var: Test for the boundaries check when a variable has to be omitted
"""

import os
from pathlib import Path
import pytest

from netcdfqc.QCnetCDF import QualityControl

data_dir = Path(__file__).parent.parent / 'sample_data'

change_rate_check_test_dict = {
    'dimensions': {
        'example_dimension_2': {'existence': False}
    },
    'variables': {
        'test_pass': {
            'existence': True,
            'do_values_change_at_acceptable_rate_check': {'perform_check': True, 'acceptable_difference': 1}
        },
        'test_fail': {
            'existence': True,
            'do_values_change_at_acceptable_rate_check': {'perform_check': True, 'acceptable_difference': 1}
        },
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


def test_boundary_check_no_nc():
    """
    Test for the boundaries check when no netCDF file is loaded
    """
    qc_obj = QualityControl()
    qc_obj.add_qc_checks_dict(change_rate_check_test_dict)
    qc_obj.values_change_rate_check()
    assert not qc_obj.logger.info
    assert qc_obj.logger.errors == ['values change rate check error: no nc file loaded']
    assert not qc_obj.logger.warnings


@pytest.mark.usefixtures("create_nc_change_rate_check")
def test_change_rate():
    """
    Test for the change rate of variables.
    """
    qc_obj = QualityControl()

    nc_path = data_dir / 'test_change_rate.nc'
    qc_obj.load_netcdf(nc_path)

    qc_obj.add_qc_checks_dict(change_rate_check_test_dict)

    qc_obj.values_change_rate_check()

    assert qc_obj.logger.info == ["value change rate check for variable 'test_pass': success",
                                  "value change rate check for variable 'test_fail': fail"]
    assert not qc_obj.logger.errors
    assert not qc_obj.logger.warnings

