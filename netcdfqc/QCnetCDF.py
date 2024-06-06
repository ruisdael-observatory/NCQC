"""
Module dedicated to the main logic of the netCDF quality control library
"""
from pathlib import Path

import netCDF4
import yaml

from netcdfqc.log import LoggerQC


class QualityControl:
    """
    Class dedicated to reading desired checks from config files
    and performing the quality control checks to netCDF files

    Attributes:
    - qc_checks_dims: checks for the dimensions of a netCDF file
    - qc_checks_vars: checks for the variables (and data) of a netCDF file
    - qc_checks_gl_attr: checks for the global attributes of a netCDF file
    - nc: netCDF file to be checked
    - logger: logger for errors, warnings, info, and creation of reports

    Methods:
    - add_qc_checks_conf: add checks via a config file
    - add_qc_checks_dict: add checks via a dictionary
    - replace_qc_checks_conf: replace checks via a config file
    - replace_qc_checks_dict: replace checks via a dictionary
    - load_netcdf: load the netcdf file to be checked
    """
    def __init__(self):
        """
        Constructor for the QualityControl objects
        """
        self.qc_checks_dims: dict = {}
        self.qc_checks_vars: dict = {}
        self.qc_checks_gl_attrs: dict = {}
        self.nc = None
        self.logger = LoggerQC()

    def add_qc_checks_conf(self, path_qc_checks_file: Path):
        """
        Method dedicated to adding quality control checks via a provided config file
        :param path_qc_checks_file: path to the config file
        """
        new_checks_dict = yaml2dict(path_qc_checks_file)
        self.add_qc_checks_dict(dict_qc_checks=new_checks_dict)

    def add_qc_checks_dict(self, dict_qc_checks: dict):
        """
        Method dedicated to adding quality control checks via a provided dictionary
        :param dict_qc_checks: the dictionary containing the checks
        """
        if 'dimensions' not in list(dict_qc_checks.keys()):
            self.logger.add_error(error="missing dimensions checks in provided config_file/dict")
        if 'variables' not in list(dict_qc_checks.keys()):
            self.logger.add_error(error="missing variables checks in provided config_file/dict")
        if 'global attributes' not in list(dict_qc_checks.keys()):
            self.logger.add_error(error="missing global attributes checks in provided config_file/dict")
        new_checks_dims_dict = dict_qc_checks['dimensions']
        new_checks_vars_dict = dict_qc_checks['variables']
        new_checks_gl_attrs_dict = dict_qc_checks['global attributes']
        self.qc_checks_dims.update(new_checks_dims_dict)
        self.qc_checks_vars.update(new_checks_vars_dict)
        self.qc_checks_gl_attrs.update(new_checks_gl_attrs_dict)

    def replace_qc_checks_conf(self, path_qc_checks_file: Path):
        """
        Method dedicated to replacing the current checks with the ones from a config file
        :param path_qc_checks_file: path to the config file
        """
        self.qc_checks_dims = {}
        self.qc_checks_vars = {}
        self.qc_checks_gl_attrs = {}
        new_checks_dict = yaml2dict(path_qc_checks_file)
        self.add_qc_checks_dict(dict_qc_checks=new_checks_dict)

    def replace_qc_checks_dict(self, dict_qc_checks: dict):
        """
        Method dedicated to replacing the current checks with the ones from a provided dictionary
        :param dict_qc_checks: the dictionary containing the checks
        """
        self.qc_checks_dims = {}
        self.qc_checks_vars = {}
        self.qc_checks_gl_attrs = {}
        self.add_qc_checks_dict(dict_qc_checks=dict_qc_checks)

    def load_netcdf(self, nc_file_path: Path):
        """
        Method dedicated to loading a netCDF file to be checked with quality control
        :param nc_file_path: path to the netCDF file
        """
        self.nc = netCDF4.Dataset(nc_file_path)  # pylint: disable=no-member

    def boundary_check(self, nc_file_path: Path):  # pylint: disable=missing-function-docstring
        # nc_file_dict = netCDF4.Dataset(nc_file_path)
        #
        # vars_to_check = list(self.qc_checks.keys())
        # vars_nc_file = list(nc_file_dict.variables.keys())
        #
        # for var_name in vars_to_check:
        #     if var_name not in vars_nc_file:
        #         print(var_name, " not in netCDF file")
        #         continue
        #
        #     lower_bound = self.qc_checks[var_name]['lower']
        #     upper_bound = self.qc_checks[var_name]['upper']
        #
        #     var_values = nc_file_dict[var_name][:]
        #
        #     for val in var_values:
        #         if val < lower_bound or val > upper_bound:
        #             print("fail - ", var_name, " out of bounds")
        #             return
        #
        # print("success")
        pass

    def existence_check(self, nc_file_path: Path):
        nc_file_dict = netCDF4.Dataset(nc_file_path, 'r', format="NETCDF4")

        # Dimensions, variables, and global attributes from the netCDF dict
        nc_dimensions = nc_file_dict.dimensions.keys()
        nc_variables = nc_file_dict.variables.keys()
        nc_global_attributes = nc_file_dict.ncattrs()

         # Dimensions, variables, and global attributes with 'does_it_exist_check' True in the config file
        dims_to_check = [dim for dim in self.qc_checks_dims if self.qc_checks_dims[dim]['does_it_exist_check'] is True]
        vars_to_check = [var for var in self.qc_checks_vars if self.qc_checks_vars[var]['does_it_exist_check'] is True]
        attrs_to_check = [attr for attr in self.qc_checks_gl_attrs if self.qc_checks_gl_attrs[attr]['does_it_exist_check'] is True]

        checked = 0
        exist = 0

        # Loop over all dimension in the config file, log error if it should exist but does not
        for dim in dims_to_check:
            checked += 1
            if dim not in nc_dimensions:
                self.logger.add_error(error=f'dimension "{dim}" should exist but it does not')
            else:
                exist += 1

        if checked != 0:
            self.logger.add_info(msg=f'{exist}/{checked} checked dimensions exist')
        else:
            self.logger.add_info(msg=f'no dimensions were checked')

        checked = 0
        exist = 0

        # Loop over all variables in the config file, log error if it should exist but does not
        for var in vars_to_check:
            checked += 1
            if var not in nc_variables:
                self.logger.add_error(error=f'variable "{var}" should exist but it does not')
            else:
                exist += 1

        if checked != 0:
            self.logger.add_info(msg=f'{exist}/{checked} checked variables exist')
        else:
            self.logger.add_info(msg=f'no variables were checked')

        checked = 0
        exist = 0

        # Loop over all global attributes in the config file, log error if it should exist but does not
        for attr in attrs_to_check:
            checked += 1
            if attr not in nc_global_attributes:
                self.logger.add_error(error=f'global attribute "{attr}" should exist but it does not')
            else:
                exist += 1

        if checked != 0:
            self.logger.add_info(msg=f'{exist}/{checked} checked global attributes exist')
        else:
            self.logger.add_info(msg=f'no global attributes were checked')

def yaml2dict(path: Path) -> dict:
    """
    This function reads a yaml file and returns a dictionary with all the field and values.
    :param path: the path to the yaml file
    :return: dictionary with all the field and values
    """
    with open(path, 'r') as yaml_f:  # pylint: disable=unspecified-encoding
        yaml_content = yaml_f.read()
        yaml_dict = yaml.safe_load(yaml_content)
    return yaml_dict
