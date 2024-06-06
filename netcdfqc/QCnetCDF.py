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
        return self

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
        return self

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
        return self

    def replace_qc_checks_dict(self, dict_qc_checks: dict):
        """
        Method dedicated to replacing the current checks with the ones from a provided dictionary
        :param dict_qc_checks: the dictionary containing the checks
        """
        self.qc_checks_dims = {}
        self.qc_checks_vars = {}
        self.qc_checks_gl_attrs = {}
        self.add_qc_checks_dict(dict_qc_checks=dict_qc_checks)
        return self

    def load_netcdf(self, nc_file_path: Path):
        """
        Method dedicated to loading a netCDF file to be checked with quality control
        :param nc_file_path: path to the netCDF file
        """
        self.nc = netCDF4.Dataset(nc_file_path)  # pylint: disable=no-member
        return self

    def boundary_check(self):
        if self.nc is None:
            self.logger.add_error("boundary check error: no nc file loaded")
            return

        vars_to_check = [
            var_name for var_name in self.qc_checks_vars.keys()
            if self.qc_checks_vars[var_name]['is_data_within_boundaries_check']
        ]

        vars_nc_file = list(self.nc.variables.keys())

        for var_name in vars_to_check:
            if var_name not in vars_nc_file:
                self.logger.add_warning(f"variable '{var_name}' not in nc file")
                continue

            lower_bound = self.qc_checks_vars[var_name]['is_data_within_boundaries_check']['lower_bound']
            upper_bound = self.qc_checks_vars[var_name]['is_data_within_boundaries_check']['upper_bound']

            var_values = self.nc[var_name][:]

            success = True
            for val in var_values:
                if val < lower_bound or val > upper_bound:
                    success = False
                    self.logger.add_error(f"boundary check error: '{val}' out of bounds for variable '"
                                          f"{var_name}' with bounds [{lower_bound},{upper_bound}]")

            self.logger.add_info(f"boundary check for variable {var_name}: {'success' if success else 'fail'}")
        return self


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
