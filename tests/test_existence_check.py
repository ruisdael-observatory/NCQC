"""
Module for testing the functionality of the existence check.

Functions:
- test_existence_check_no_nc: Test for the existence check when no netCDF file is loaded.
- test_existence_check_all_exist: Test for the existence check when everything exists.
- test_existence_check_mixed: Test for the existence check with mixed existence.
- test_existence_check_none_exist: Test for the existence check when nothing exists.
- test_existence_check_all_false: Test for the existence check with nothing to be checked.
"""

import os
from pathlib import Path
import pytest

from netcdfqc.QCnetCDF import QualityControl

data_dir = Path(__file__).parent.parent / 'sample_data'


def test_existence_check_no_nc():
    """
    Test for the existence check when no netCDF file is loaded.
    """
    qc_obj = QualityControl()
    qc_obj.existence_check()

    assert qc_obj.logger.errors == ['existence_check error: no nc file loaded']
    assert not qc_obj.logger.warnings
    assert not qc_obj.logger.info


@pytest.mark.usefixtures("create_nc_existence_check")
def test_existence_check_all_exist():
    """
    Test for the existence check with some dimensions, variables, and global attributes to be checked,
    which all exist, and some that should not be checked at all.
    """
    qc_obj = QualityControl()

    nc_path = data_dir / 'test_existence.nc'
    qc_obj.load_netcdf(nc_path)

    qc_obj.qc_checks_dims = {
        'time': {'existence_check': True},
        'diameter_classes': {'existence_check': False},
        'velocity_classes': {'existence_check': True}
    }
    qc_obj.qc_checks_vars = {
        'longitude': {'existence_check': True},
        'latitude': {'existence_check': True},
        'altitude': {'existence_check': True}
    }
    qc_obj.qc_checks_gl_attrs = {
        'title': {'existence_check': True},
        'source': {'existence_check': True},
        'contributors': {'existence_check': False}
    }

    qc_obj.existence_check()

    expected_errors = []

    expected_warnings = []

    expected_info = ['2/2 checked dimensions exist',
                     '3/3 checked variables exist',
                     '2/2 checked global attributes exist']

    assert qc_obj.logger.errors == expected_errors
    assert qc_obj.logger.warnings == expected_warnings
    assert qc_obj.logger.info == expected_info

    if os.path.exists(nc_path):
        os.remove(nc_path)


@pytest.mark.usefixtures("create_nc_existence_check")
def test_existence_check_mixed():
    """
    Test for the existence check with some dimensions, variables, and global attributes to be checked,
    of which some do not exist, and some that should not be checked at all.
    """
    qc_obj = QualityControl()

    nc_path = data_dir / 'test_existence.nc'
    qc_obj.load_netcdf(nc_path)

    qc_obj.qc_checks_dims = {
        'time': {'existence_check': True},
        'diameter_classes': {'existence_check': False},
        'velocity_classes': {'existence_check': True},
        'bad_dimension': {'existence_check': True}
    }
    qc_obj.qc_checks_vars = {
        'longitude': {'existence_check': True},
        'latitude': {'existence_check': True},
        'altitude': {'existence_check': True},
        'bad_variable': {'existence_check': True}
    }
    qc_obj.qc_checks_gl_attrs = {
        'title': {'existence_check': True},
        'source': {'existence_check': True},
        'contributors': {'existence_check': False},
        'bad_attribute': {'existence_check': True}
    }

    qc_obj.existence_check()

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

    if os.path.exists(nc_path):
        os.remove(nc_path)


@pytest.mark.usefixtures("create_nc_existence_check")
def test_existence_check_none_exist():
    """
    Test for the existence check when nothing exists.
    """
    qc_obj = QualityControl()

    nc_path = data_dir / 'test_existence.nc'
    qc_obj.load_netcdf(nc_path)

    qc_obj.qc_checks_dims = {
        'bad_dimension': {'existence_check': True}
    }
    qc_obj.qc_checks_vars = {
        'bad_variable1': {'existence_check': True},
        'bad_variable2': {'existence_check': True}
    }
    qc_obj.qc_checks_gl_attrs = {
        'bad_attribute': {'existence_check': True}
    }

    qc_obj.existence_check()

    expected_errors = ['dimension "bad_dimension" should exist but it does not',
                       'variable "bad_variable1" should exist but it does not',
                       'variable "bad_variable2" should exist but it does not',
                       'global attribute "bad_attribute" should exist but it does not']

    expected_warnings = []

    expected_info = ['0/1 checked dimensions exist',
                     '0/2 checked variables exist',
                     '0/1 checked global attributes exist']

    assert qc_obj.logger.errors == expected_errors
    assert qc_obj.logger.warnings == expected_warnings
    assert qc_obj.logger.info == expected_info

    if os.path.exists(nc_path):
        os.remove(nc_path)


@pytest.mark.usefixtures("create_nc_existence_check")
def test_existence_check_all_false():
    """
    Test for the existence check with nothing to be checked.
    """
    qc_obj = QualityControl()

    nc_path = data_dir / 'test_existence.nc'
    qc_obj.load_netcdf(nc_path)

    qc_obj.qc_checks_dims = {
        'example_dimension': {'existence_check': False}
    }
    qc_obj.qc_checks_vars = {
        'example_variable': {'existence_check': False}
    }
    qc_obj.qc_checks_gl_attrs = {
        'example_attribute': {'existence_check': False}
    }

    qc_obj.existence_check()

    expected_errors = []

    expected_warnings = []

    expected_info = ['no dimensions were checked',
                     'no variables were checked',
                     'no global attributes were checked']

    assert qc_obj.logger.errors == expected_errors
    assert qc_obj.logger.warnings == expected_warnings
    assert qc_obj.logger.info == expected_info

    if os.path.exists(nc_path):
        os.remove(nc_path)
