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
import os

@pytest.fixture()
def create_nc_existence():

    nc_path = Path(__file__).parent / 'sample_data' / 'test_existence.nc'

    if os.path.exists(nc_path):
        os.remove(nc_path)

    # Create a new netCDF file
    nc_file = Dataset(nc_path, 'w', format='NETCDF4')

    # Create dimensions
    nc_file.createDimension('time', 100)
    nc_file.createDimension('diameter_classes', 32)
    nc_file.createDimension('velocity_classes', 32)

    # Create variables
    temperature = nc_file.createVariable('temperature', 'f4', ('time',), fill_value=-999.0)
    wind_speed = nc_file.createVariable('wind_speed', 'f4', ('time',), fill_value=-999.0)
    wind_direction = nc_file.createVariable('wind_direction', 'f4', ('time',), fill_value=-999.0)
    longitude = nc_file.createVariable('longitude', 'f4', fill_value=-999.0)
    latitude = nc_file.createVariable('latitude', 'f4', fill_value=-999.0)
    altitude = nc_file.createVariable('altitude', 'f4', fill_value=-999.0)

    # Create global attributes
    nc_file.title = "Test NetCDF File"
    nc_file.source = "confest.py"
    nc_file.contributors = "people"

    # Close the netCDF file
    nc_file.close()

@pytest.fixture()
def create_nc_emptiness_full():
    nc_path = Path(__file__).parent / 'sample_data' / 'test_emptiness_full.nc'

    if os.path.exists(nc_path):
        os.remove(nc_path)

    # Create a new netCDF file
    nc_file = Dataset(nc_path, 'w', format='NETCDF4')

    # Create dimensions
    nc_file.createDimension('time', 100)
    nc_file.createDimension('diameter_classes', 32)
    nc_file.createDimension('velocity_classes', 32)

    # Create variables
    temperature = nc_file.createVariable('temperature', 'f4', ('time',), fill_value=-999.0)
    wind_speed = nc_file.createVariable('wind_speed', 'f4', ('time',), fill_value=-999.0)
    wind_direction = nc_file.createVariable('wind_direction', 'f4', ('time',), fill_value=-999.0)

    # Set variables
    temperature[:] = np.random.uniform(-10, 30, size=100)
    wind_speed[:] = np.random.uniform(0, 30, size=100)
    wind_direction[:] = np.random.uniform(0, 360, size=100)

    # Create global attributes
    nc_file.title = "Test NetCDF File"
    nc_file.source = "confest.py"
    nc_file.contributors = "people"

    # Close the netCDF file
    nc_file.close()

@pytest.fixture()
def create_nc_emptiness_mixed():
    nc_path = Path(__file__).parent / 'sample_data' / 'test_emptiness_mixed.nc'

    if os.path.exists(nc_path):
        os.remove(nc_path)

    # Create a new netCDF file
    nc_file = Dataset(nc_path, 'w', format='NETCDF4')

    # Create dimensions
    nc_file.createDimension('time', 100)
    nc_file.createDimension('diameter_classes', 32)
    nc_file.createDimension('velocity_classes', 32)

    # Create variables
    temperature = nc_file.createVariable('temperature', 'f4', ('time',), fill_value=-999.0)
    wind_speed = nc_file.createVariable('wind_speed', 'f4', ('time',), fill_value=-999.0)
    wind_direction = nc_file.createVariable('wind_direction', 'f4', ('time',), fill_value=-999.0)
    longitude = nc_file.createVariable('longitude', 'f4', fill_value=-999.0)
    latitude = nc_file.createVariable('latitude', 'f4', fill_value=-999.0)
    altitude = nc_file.createVariable('altitude', 'f4', fill_value=-999.0)

    # Set variables
    temperature[:] = np.random.uniform(-10, 30, size=100)

    wind_speed[:50] = np.random.uniform(0, 30, size=50)
    wind_speed[50:] = wind_speed.getncattr('_FillValue')

    wind_direction[:50] = np.random.uniform(0, 360, size=50)
    wind_direction[50:] = np.nan

    longitude.assignValue(longitude.getncattr('_FillValue'))
    latitude.assignValue(np.nan)
    altitude.assignValue(1.0)

    # Create global attributes
    nc_file.title = "Test NetCDF File"
    nc_file.source = "confest.py"
    nc_file.contributors = ""

    # Close the netCDF file
    nc_file.close()

@pytest.fixture()
def create_nc_emptiness_empty():
    nc_path = Path(__file__).parent / 'sample_data' / 'test_emptiness_empty.nc'

    if os.path.exists(nc_path):
        os.remove(nc_path)

    # Create a new netCDF file
    nc_file = Dataset(nc_path, 'w', format='NETCDF4')

    # Create dimensions
    nc_file.createDimension('time', 100)
    nc_file.createDimension('diameter_classes', 32)
    nc_file.createDimension('velocity_classes', 32)

    # Create variables
    temperature = nc_file.createVariable('temperature', 'f4', ('time',), fill_value=-999.0)
    wind_speed = nc_file.createVariable('wind_speed', 'f4', ('time',), fill_value=-999.0)
    wind_direction = nc_file.createVariable('wind_direction', 'f4', ('time',), fill_value=-999.0)

    # Set variables
    wind_speed[:] = wind_speed.getncattr('_FillValue')
    wind_direction[:] = np.nan

    # Create global attributes
    nc_file.title = ""
    nc_file.source = ""
    nc_file.contributors = ""

    # Close the netCDF file
    nc_file.close()
