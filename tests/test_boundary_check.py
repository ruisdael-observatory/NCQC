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
import unittest
from pathlib import Path
from unittest.mock import patch
import pytest

import netCDF4

from netcdfqc.QCnetCDF import QualityControl

data_dir = Path(__file__).parent.parent / 'sample_data'

boundary_check_test_dict = {
    'dimensions': {
        'example_dimension_2': {'existence': False}
    },
    'variables': {
        'velocity_spread': {
            'existence': False,
            'is_data_within_boundaries_check': {'perform_check': True, 'lower_bound': 0, 'upper_bound': 3.3}
        },
        'kinetic_energy': {
            'existence': True,
            'is_data_within_boundaries_check': {'perform_check': True, 'lower_bound': 0, 'upper_bound': 1.91}
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
    qc_obj.add_qc_checks_dict(boundary_check_test_dict)
    qc_obj.boundary_check()
    assert not qc_obj.logger.info
    assert qc_obj.logger.errors == ['boundary check error: no nc file loaded']
    assert not qc_obj.logger.warnings

@pytest.mark.usefixtures("create_nc_boundary_check_success")
def test_boundary_check_success():
    """
    Test for the boundaries check when all checks are successful
    """
    qc_obj = QualityControl()

    nc_path = data_dir / 'test_boundary_success.nc'
    qc_obj.load_netcdf(nc_path)

    qc_obj.add_qc_checks_dict(boundary_check_test_dict)

    qc_obj.boundary_check()

    assert qc_obj.logger.info == ['boundary check for variable \'velocity_spread\': success'
        , 'boundary check for variable \'kinetic_energy\': success']
    assert not qc_obj.logger.errors
    assert not qc_obj.logger.warnings

    if os.path.exists(nc_path):
        os.remove(nc_path)

@pytest.mark.usefixtures("create_nc_boundary_check_fail")
def test_boundary_check_fail():
    """
    Test for the boundaries check when a check fails
    """
    qc_obj = QualityControl()

    nc_path = data_dir / 'test_boundary_fail.nc'
    qc_obj.load_netcdf(nc_path)

    qc_obj.add_qc_checks_dict({
        'dimensions': {
            'example_dimension_2': {'existence': False}
        },
        'variables': {
            'velocity_spread': {
                'existence': False,
                'is_data_within_boundaries_check': {'perform_check': True, 'lower_bound': 0, 'upper_bound': 3.3}
            },
            'kinetic_energy': {
                'existence': True,
                'is_data_within_boundaries_check': {'perform_check': True, 'lower_bound': 0, 'upper_bound': 1.8}
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
    })

    qc_obj.boundary_check()

    assert qc_obj.logger.info == ['boundary check for variable \'velocity_spread\': success'
        , 'boundary check for variable \'kinetic_energy\': fail']
    assert qc_obj.logger.errors == ['boundary check error: \'1.909999966621399\' out of bounds'
                                    ' for variable'' \'kinetic_energy\' with bounds [0,1.8]']
    assert not qc_obj.logger.warnings

    if os.path.exists(nc_path):
        os.remove(nc_path)

@pytest.mark.usefixtures("create_nc_boundary_check_success")
def test_boundary_check_wrong_var_name():
    """
    Test for the boundaries check when a variable to be checked is not in the loaded netCDF file
    """
    qc_obj = QualityControl()

    nc_path = data_dir / 'test_boundary_success.nc'
    qc_obj.load_netcdf(nc_path)

    qc_obj.add_qc_checks_dict(boundary_check_test_dict)

    qc_obj.add_qc_checks_dict({
        'dimensions': {},
        'variables': {
            'no_such_var': {
                'existence': False,
                'is_data_within_boundaries_check': {'perform_check': True, 'lower_bound': 0, 'upper_bound': 1}
            }
        },
        'global attributes': {},
        'file size': {}
    })

    qc_obj.boundary_check()

    assert qc_obj.logger.info == ['boundary check for variable \'velocity_spread\': success'
        , 'boundary check for variable \'kinetic_energy\': success']
    assert not qc_obj.logger.errors
    assert qc_obj.logger.warnings == ['variable \'no_such_var\' not in nc file']

    if os.path.exists(nc_path):
        os.remove(nc_path)

@pytest.mark.usefixtures("create_nc_boundary_check_success")
def test_boundary_check_omit_a_var():
    """
    Test for the boundaries check when a variable has to be omitted
    """
    qc_obj = QualityControl()

    nc_path = data_dir / 'test_boundary_success.nc'
    qc_obj.load_netcdf(nc_path)

    boundary_check_test_dict_omit_var = {
        'dimensions': {
            'example_dimension_2': {'existence': False}
        },
        'variables': {
            'velocity_spread': {
                'existence': False,
                'is_data_within_boundaries_check': {'perform_check': False, 'lower_bound': 0, 'upper_bound': 3.3}
            },
            'kinetic_energy': {
                'existence': True,
                'is_data_within_boundaries_check': {'perform_check': True, 'lower_bound': 0, 'upper_bound': 1.91}
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
    qc_obj.add_qc_checks_dict(boundary_check_test_dict_omit_var)

    qc_obj.boundary_check()

    assert qc_obj.logger.info == ['boundary check for variable \'kinetic_energy\': success']
    assert not qc_obj.logger.warnings
    assert not qc_obj.logger.errors

    if os.path.exists(nc_path):
        os.remove(nc_path)
