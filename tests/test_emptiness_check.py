"""
Module for testing the functionality of the emptiness check.

Functions:
- test_emptiness_check_no_nc: Test for the emptiness check when no netCDF file is loaded.
- test_emptiness_check_full: Test for the emptiness check when everything is fully populated.
- test_emptiness_check_mixed: Test for the emptiness check with mixed emptiness.
- test_emptiness_check_empty: Test for the emptiness check when nothing is populated.
- test_emptiness_check_all_false: Test for the emptiness check with nothing to be checked.
"""

import os
from pathlib import Path
import pytest

from netcdfqc.QCnetCDF import QualityControl

data_dir = Path(__file__).parent.parent / 'sample_data'


def test_emptiness_check_no_nc():
    """
    Test for the emptiness check when no netCDF file is loaded.
    """
    qc_obj = QualityControl()
    qc_obj.emptiness_check()

    assert qc_obj.logger.errors == ['emptiness check error: no nc file loaded']
    assert not qc_obj.logger.warnings
    assert not qc_obj.logger.info


@pytest.mark.usefixtures("create_nc_emptiness_check_full")
def test_emptiness_check_full():
    """
    Test for the emptiness check with some variables and global attributes to be checked,
    of which all are fully populated, and some that should not be checked at all.
    """
    qc_obj = QualityControl()

    nc_path = data_dir / 'test_emptiness_full.nc'
    qc_obj.load_netcdf(nc_path)

    qc_obj.qc_checks_vars = {
        'temperature': {'is_it_empty_check': True},
        'wind_speed': {'is_it_empty_check': True},
        'wind_direction': {'is_it_empty_check': True},
        'altitude': {'is_it_empty_check': False}
    }
    qc_obj.qc_checks_gl_attrs = {
        'title': {'is_it_empty_check': True},
        'source': {'is_it_empty_check': False},
        'contributors': {'is_it_empty_check': True}
    }

    qc_obj.emptiness_check()

    expected_errors = []

    expected_warnings = []

    expected_info = ['3/3 checked variables are fully populated',
                     '2/2 checked global attributes have values assigned']

    print(qc_obj.logger.errors)

    assert qc_obj.logger.errors == expected_errors
    assert qc_obj.logger.warnings == expected_warnings
    assert qc_obj.logger.info == expected_info

    if os.path.exists(nc_path):
        os.remove(nc_path)


@pytest.mark.usefixtures("create_nc_emptiness_check_mixed")
def test_emptiness_check_mixed():
    """
    Test for the emptiness check with some variables and global attributes which are not (fully) populated.
    """
    qc_obj = QualityControl()

    nc_path = data_dir / 'test_emptiness_mixed.nc'
    qc_obj.load_netcdf(nc_path)

    qc_obj.qc_checks_vars = {
        'temperature': {'is_it_empty_check': True},
        'wind_speed': {'is_it_empty_check': True},
        'wind_direction': {'is_it_empty_check': True},
        'longitude': {'is_it_empty_check': True},
        'latitude': {'is_it_empty_check': True},
        'altitude': {'is_it_empty_check': True}
    }
    qc_obj.qc_checks_gl_attrs = {
        'title': {'is_it_empty_check': True},
        'source': {'is_it_empty_check': False},
        'contributors': {'is_it_empty_check': True}
    }

    qc_obj.emptiness_check()

    expected_errors = ['variable "wind_speed" has 50/100 empty data points',
                       'variable "wind_direction" has 50/100 NaN data points',
                       'scalar variable "longitude" is empty',
                       'scalar variable "latitude" is NaN',
                       'global attribute "contributors" is empty']

    expected_warnings = []

    expected_info = ['2/6 checked variables are fully populated',
                     '1/2 checked global attributes have values assigned']

    print(qc_obj.logger.errors)

    assert qc_obj.logger.errors == expected_errors
    assert qc_obj.logger.warnings == expected_warnings
    assert qc_obj.logger.info == expected_info

    if os.path.exists(nc_path):
        os.remove(nc_path)


@pytest.mark.usefixtures("create_nc_emptiness_check_empty")
def test_emptiness_check_all_empty():
    """
    Test for the emptiness check with only variables and global attributes which are empty.
    """
    qc_obj = QualityControl()

    nc_path = data_dir / 'test_emptiness_empty.nc'
    qc_obj.load_netcdf(nc_path)

    qc_obj.qc_checks_vars = {
        'temperature': {'is_it_empty_check': True},
        'wind_speed': {'is_it_empty_check': True},
        'wind_direction': {'is_it_empty_check': True}
    }
    qc_obj.qc_checks_gl_attrs = {
        'title': {'is_it_empty_check': True},
        'source': {'is_it_empty_check': False},
        'contributors': {'is_it_empty_check': True}
    }

    qc_obj.emptiness_check()

    expected_errors = ['variable "temperature" has 100/100 empty data points',
                       'variable "wind_speed" has 100/100 empty data points',
                       'variable "wind_direction" has 100/100 NaN data points',
                       'global attribute "title" is empty',
                       'global attribute "contributors" is empty']

    expected_warnings = []

    expected_info = ['0/3 checked variables are fully populated',
                     '0/2 checked global attributes have values assigned']

    print(qc_obj.logger.errors)

    assert qc_obj.logger.errors == expected_errors
    assert qc_obj.logger.warnings == expected_warnings
    assert qc_obj.logger.info == expected_info

    if os.path.exists(nc_path):
        os.remove(nc_path)


@pytest.mark.usefixtures("create_nc_emptiness_check_full")
def test_emptiness_check_all_false():
    """
    Test for the emptiness check with nothing to be checked.
    """
    qc_obj = QualityControl()

    nc_path = data_dir / 'test_emptiness_full.nc'
    qc_obj.load_netcdf(nc_path)

    qc_obj.qc_checks_vars = {
        'example_variable': {'is_it_empty_check': False}
    }
    qc_obj.qc_checks_gl_attrs = {
        'example_attribute': {'is_it_empty_check': False}
    }

    qc_obj.emptiness_check()

    expected_errors = []

    expected_warnings = []

    expected_info = ['no variables were checked for emptiness',
                     'no global attributes were checked for emptiness']

    assert qc_obj.logger.errors == expected_errors
    assert qc_obj.logger.warnings == expected_warnings
    assert qc_obj.logger.info == expected_info

    if os.path.exists(nc_path):
        os.remove(nc_path)
