"""
Module with all test fixtures.
When a test fixtures is set as argument for a test function, it automatically runs at the start of the test.
"""

from pathlib import Path

from netCDF4 import Dataset
import yaml
import math
import numpy as np
import pytest

@pytest.fixture()
def create_nc_emptiness():

    # Create a new netCDF file
    nc_file = Dataset(Path(__file__).parent / 'sample_data/test.nc', 'w', format='NETCDF4')

    # Define the dimensions
    nc_file.createDimension('time', 100)
    nc_file.createDimension('diameter_classes', 32)
    nc_file.createDimension('velocity_classes', 32)

    # Create the variables with the specified _FillValue where needed
    temperature = nc_file.createVariable('temperature', 'f4', ('time',), fill_value=-999.0)
    wind_speed = nc_file.createVariable('wind_speed', 'f4', ('time',), fill_value=-999.0)
    wind_direction = nc_file.createVariable('wind_direction', 'f4', ('time',), fill_value=-999.0)
    longitude = nc_file.createVariable('longitude', 'f4', fill_value=-999.0)
    latitude = nc_file.createVariable('latitude', 'f4', fill_value=-999.0)
    altitude = nc_file.createVariable('altitude', 'f4', fill_value=-999.0)

    # Fill the temperature variable with 20 degrees celsius
    temperature[:] = 20.0

    # Fill wind_speed with a max of actual values -999.0 as _FillValue
    wind_speed[:50] = np.random.uniform(0, 30, size=50)
    wind_speed[50:] = wind_speed.getncattr('_FillValue')

    # Fill wind_direction with a mix of actual values and NaN
    wind_direction[:50] = np.random.uniform(0, 360, size=50)
    wind_direction[50:] = np.nan

    # Set scalar values for longitude, latitude, and altitude
    longitude.assignValue(longitude.getncattr('_FillValue'))
    latitude.assignValue(np.nan)
    altitude.assignValue(1.0)

    # Set global attributes
    nc_file.title = "Test NetCDF File"
    nc_file.source = "confest.py"
    nc_file.contributors = ""

    # Close the netCDF file
    nc_file.close()
