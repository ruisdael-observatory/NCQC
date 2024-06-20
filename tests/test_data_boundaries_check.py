"""
Module for testing the functionality of the boundaries check

Functions:
- test_data_boundaries_check_no_nc: Test for the boundaries check when no netCDF file is loaded
- test_data_boundaries_check_success: Test for the boundaries check when all checks are successful
- test_data_boundaries_check_fail: Test for the boundaries check when a check fails
- test_data_boundaries_check_wrong_var_name: Test for the boundaries check when a variable to be
checked is not in the loaded netCDF file
- test_data_boundaries_check_omit_a_var: Test for the boundaries check when a variable has to be omitted
- test_data_boundaries_check_property_based_success: Property based test for the boundaries check
    when all values are within the specified boundaries
- test_data_boundaries_check_property_based_fail: Property based test for the boundaries check
    when at least one value is outside of the specified boundaries
- test_data_boundaries_check_multidim_var_success: Test for the boundaries check when a variable is multidimensional
with expected success
- test_data_boundaries_check_multidim_var_fail: Test for the boundaries check when a variable is multidimensional
with expected failure
"""

import os
from pathlib import Path
from hypothesis import given, strategies as st
import pytest

from ncqc.QCnetCDF import QualityControl
from conftest import create_nc_data_boundaries_check_property_based

data_dir = Path(__file__).parent.parent / 'sample_data'

data_boundaries_check_test_dict = {
    'dimensions': {
        'example_dimension_2': {'existence': False}
    },
    'variables': {
        'velocity_spread': {
            'existence': False,
            'data_boundaries_check': {'perform_check': True, 'lower_bound': 0, 'upper_bound': 3.3}
        },
        'kinetic_energy': {
            'existence': True,
            'data_boundaries_check': {'perform_check': True, 'lower_bound': 0, 'upper_bound': 1.91}
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

data_boundaries_check_property_based_test_dict = {
    'dimensions': {
        'example_dimension_2': {'existence': False}
    },
    'variables': {
        'temperature': {
            'existence': True,
            'data_boundaries_check': {'perform_check': True, 'lower_bound': -10, 'upper_bound': 40}
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


def test_data_boundaries_check_no_nc():
    """
    Test for the boundaries check when no netCDF file is loaded
    """
    qc_obj = QualityControl()
    qc_obj.add_qc_checks_dict(data_boundaries_check_test_dict)
    qc_obj.data_boundaries_check()
    assert not qc_obj.logger.info
    assert qc_obj.logger.errors == ['data_boundaries_check error: no nc file loaded']
    assert not qc_obj.logger.warnings


@pytest.mark.usefixtures("create_nc_data_boundaries_check_success")
def test_data_boundaries_check_success():
    """
    Test for the boundaries check when all checks are successful
    """
    qc_obj = QualityControl()

    nc_path = data_dir / 'test_boundary_success.nc'
    qc_obj.load_netcdf(nc_path)

    qc_obj.add_qc_checks_dict(data_boundaries_check_test_dict)

    qc_obj.data_boundaries_check()

    assert qc_obj.logger.info == ['boundary check for variable \'velocity_spread\': SUCCESS'
        , 'boundary check for variable \'kinetic_energy\': SUCCESS']
    assert not qc_obj.logger.errors
    assert not qc_obj.logger.warnings

    if os.path.exists(nc_path):
        os.remove(nc_path)


@pytest.mark.usefixtures("create_nc_data_boundaries_check_fail")
def test_data_boundaries_check_fail():
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
                'data_boundaries_check': {'perform_check': True, 'lower_bound': 0, 'upper_bound': 3.3}
            },
            'kinetic_energy': {
                'existence': True,
                'data_boundaries_check': {'perform_check': True, 'lower_bound': 0, 'upper_bound': 1.8}
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

    qc_obj.data_boundaries_check()

    assert qc_obj.logger.info == ['boundary check for variable \'velocity_spread\': SUCCESS'
        , 'boundary check for variable \'kinetic_energy\': FAIL']
    assert qc_obj.logger.errors == ['boundary check error: \'1.909999966621399\' out of bounds'
                                    ' for variable'' \'kinetic_energy\' with bounds [0,1.8]']
    assert not qc_obj.logger.warnings

    if os.path.exists(nc_path):
        os.remove(nc_path)


@pytest.mark.usefixtures("create_nc_data_boundaries_check_success")
def test_data_boundaries_check_wrong_var_name():
    """
    Test for the boundaries check when a variable to be checked is not in the loaded netCDF file
    """
    qc_obj = QualityControl()

    nc_path = data_dir / 'test_boundary_success.nc'
    qc_obj.load_netcdf(nc_path)

    qc_obj.add_qc_checks_dict(data_boundaries_check_test_dict)

    qc_obj.add_qc_checks_dict({
        'dimensions': {},
        'variables': {
            'no_such_var': {
                'existence': False,
                'data_boundaries_check': {'perform_check': True, 'lower_bound': 0, 'upper_bound': 1}
            }
        },
        'global attributes': {},
        'file size': {}
    })

    qc_obj.data_boundaries_check()

    assert qc_obj.logger.info == ['boundary check for variable \'velocity_spread\': SUCCESS'
        , 'boundary check for variable \'kinetic_energy\': SUCCESS']
    assert not qc_obj.logger.errors
    assert qc_obj.logger.warnings == ['variable \'no_such_var\' not in nc file']

    if os.path.exists(nc_path):
        os.remove(nc_path)


@pytest.mark.usefixtures("create_nc_data_boundaries_check_success")
def test_data_boundaries_check_omit_a_var():
    """
    Test for the boundaries check when a variable has to be omitted
    """
    qc_obj = QualityControl()

    nc_path = data_dir / 'test_boundary_success.nc'
    qc_obj.load_netcdf(nc_path)

    data_boundaries_check_test_dict_omit_var = {
        'dimensions': {
            'example_dimension_2': {'existence': False}
        },
        'variables': {
            'velocity_spread': {
                'existence': False,
                'data_boundaries_check': {'perform_check': False, 'lower_bound': 0, 'upper_bound': 3.3}
            },
            'kinetic_energy': {
                'existence': True,
                'data_boundaries_check': {'perform_check': True, 'lower_bound': 0, 'upper_bound': 1.91}
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
    qc_obj.add_qc_checks_dict(data_boundaries_check_test_dict_omit_var)

    qc_obj.data_boundaries_check()

    assert qc_obj.logger.info == ['boundary check for variable \'kinetic_energy\': SUCCESS']
    assert not qc_obj.logger.warnings
    assert not qc_obj.logger.errors

    if os.path.exists(nc_path):
        os.remove(nc_path)


@given(data=st.lists(st.integers(min_value=-10, max_value=40), max_size=100))
def test_data_boundaries_check_property_based_success(data):
    """
    Property based test for the boundaries check when all values are within the specified boundaries
    :param data: all possible lists of integers where all values are inside of the range [-10, 40]
    """
    create_nc_data_boundaries_check_property_based(data=data)

    qc_obj = QualityControl()

    nc_path = data_dir / 'test_boundary_property.nc'
    qc_obj.load_netcdf(nc_path)

    qc_obj.add_qc_checks_dict(data_boundaries_check_property_based_test_dict)

    qc_obj.data_boundaries_check()

    assert qc_obj.logger.info == ['boundary check for variable \'temperature\': SUCCESS']
    assert not qc_obj.logger.errors
    assert not qc_obj.logger.warnings

    if os.path.exists(nc_path):
        os.remove(nc_path)


@given(data=st.lists(st.integers(), max_size=100)
       .filter(lambda lst: any(x < -10 or x > 40 for x in lst)))
def test_data_boundaries_check_property_based_fail(data):
    """
    Property based test for the boundaries check when at least one value is outside of the specified boundaries
    :param data: all possible lists of integers where at least value is outside of the range [-10, 40]
    """
    create_nc_data_boundaries_check_property_based(data=data)

    qc_obj = QualityControl()

    nc_path = data_dir / 'test_boundary_property.nc'
    qc_obj.load_netcdf(nc_path)

    qc_obj.add_qc_checks_dict(data_boundaries_check_property_based_test_dict)

    qc_obj.data_boundaries_check()

    expected_errors = 0

    for val in data:
        if val < -10 or val > 40:
            expected_errors += 1

    assert qc_obj.logger.info == ['boundary check for variable \'temperature\': FAIL']
    assert len(qc_obj.logger.errors) == expected_errors
    assert not qc_obj.logger.warnings

    if os.path.exists(nc_path):
        os.remove(nc_path)


@pytest.mark.usefixtures("create_nc_data_boundaries_check_multidim_var")
def test_data_boundaries_check_multidim_var_success():
    """
    Test for the boundaries check when a variable is multidimensional
    with expected success
    """
    qc_obj = QualityControl()

    nc_path = data_dir / 'test_boundary_multidim.nc'
    qc_obj.load_netcdf(nc_path)

    qc_obj.add_qc_checks_dict({
        'dimensions': {},
        'variables': {
            'var_2d': {
                'data_boundaries_check': {
                    'perform_check': True,
                    'lower_bound': 0,
                    'upper_bound': 1.01
                }
            }
        },
        'global attributes': {},
        'file size': {}
    })

    qc_obj.data_boundaries_check()

    assert qc_obj.logger.info == ["boundary check for variable 'var_2d': SUCCESS"]
    assert not qc_obj.logger.warnings
    assert not qc_obj.logger.errors

    if os.path.exists(nc_path):
        os.remove(nc_path)


@pytest.mark.usefixtures("create_nc_data_boundaries_check_multidim_var")
def test_data_boundaries_check_multidim_var_fail():
    """
    Test for the boundaries check when a variable is multidimensional
    with expected failure
    """
    qc_obj = QualityControl()

    nc_path = data_dir / 'test_boundary_multidim.nc'
    qc_obj.load_netcdf(nc_path)

    qc_obj.add_qc_checks_dict({
        'dimensions': {},
        'variables': {
            'var_2d': {
                'data_boundaries_check': {
                    'perform_check': True,
                    'lower_bound': 0,
                    'upper_bound': 1
                }
            }
        },
        'global attributes': {},
        'file size': {}
    })

    qc_obj.data_boundaries_check()

    assert qc_obj.logger.info == ["boundary check for variable 'var_2d': FAIL"]
    assert not qc_obj.logger.warnings
    assert qc_obj.logger.errors == ["boundary check error: '1.0099999904632568' out of"
                                    " bounds for variable 'var_2d' with bounds [0,1]"]

    if os.path.exists(nc_path):
        os.remove(nc_path)
