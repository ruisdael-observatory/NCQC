"""
Module dedicated to the main logic of the netCDF quality control library

Functions:
- yaml2dict: reads a yaml file and returns a dictionary with all the field and values
"""

from pathlib import Path
import netCDF4
import yaml
import numpy as np

from netcdfqc.log import LoggerQC


class QualityControl:
    """
    Class dedicated to reading desired checks from config files
    and performing the quality control checks to netCDF files

    Attributes:
    - qc_checks_dims: checks for the dimensions of a netCDF file
    - qc_checks_vars: checks for the variables (and data) of a netCDF file
    - qc_checks_gl_attr: checks for the global attributes of a netCDF file
    - qc_check_file_size: check for the file size of a netCDF file
    - nc: netCDF file to be checked
    - logger: logger for errors, warnings, info, and creation of reports

    Methods:
    - add_qc_checks_conf: add checks via a config file
    - add_qc_checks_dict: add checks via a dictionary
    - replace_qc_checks_conf: replace checks via a config file
    - replace_qc_checks_dict: replace checks via a dictionary
    - load_netcdf: load the netcdf file to be checked
    - boundary_check: perform a boundary check on the variables of the loaded netCDF file
    - existence_check: perform existence checks on dimensions, variables and global attributes
    - file_size_check:
    - data_points_amount_check:
    - values_change_rate_check:
    - constant_values_check:
    - expected_dimensions_vars_check: Method dedicated to checking whether each variable has the expected dimensions
    """

    def __init__(self):
        """
        Constructor for the QualityControl objects
        """
        self.qc_checks_dims: dict = {}
        self.qc_checks_vars: dict = {}
        self.qc_checks_gl_attrs: dict = {}
        self.qc_check_file_size: dict = {}
        self.nc = None
        self.logger = LoggerQC()

    def add_qc_checks_conf(self, path_qc_checks_file: Path):
        """
        Method dedicated to adding quality control checks via a provided config file
        :param path_qc_checks_file: path to the config file
        :return: self
        """
        new_checks_dict = yaml2dict(path_qc_checks_file)
        self.add_qc_checks_dict(dict_qc_checks=new_checks_dict)
        return self

    def add_qc_checks_dict(self, dict_qc_checks: dict):
        """
        Method dedicated to adding quality control checks via a provided dictionary
        :param dict_qc_checks: the dictionary containing the checks
        :return: self
        """
        if 'dimensions' not in list(dict_qc_checks.keys()):
            self.logger.add_error(error="missing dimensions checks in provided config_file/dict")
        else:
            new_checks_dims_dict = dict_qc_checks['dimensions']
            self.qc_checks_dims.update(new_checks_dims_dict)
        if 'variables' not in list(dict_qc_checks.keys()):
            self.logger.add_error(error="missing variables checks in provided config_file/dict")
        else:
            new_checks_vars_dict = dict_qc_checks['variables']
            self.qc_checks_vars.update(new_checks_vars_dict)
        if 'global attributes' not in list(dict_qc_checks.keys()):
            self.logger.add_error(error="missing global attributes checks in provided config_file/dict")
        else:
            new_checks_gl_attrs_dict = dict_qc_checks['global attributes']
            self.qc_checks_gl_attrs.update(new_checks_gl_attrs_dict)
        if 'file size' not in list(dict_qc_checks.keys()):
            self.logger.add_error(error="missing file size check in provided config_file/dict")
        else:
            new_check_file_size = dict_qc_checks['file size']
            self.qc_check_file_size.update(new_check_file_size)
        return self

    def replace_qc_checks_conf(self, path_qc_checks_file: Path):
        """
        Method dedicated to replacing the current checks with the ones from a config file
        :param path_qc_checks_file: path to the config file
        :return: self
        """
        self.qc_checks_dims = {}
        self.qc_checks_vars = {}
        self.qc_checks_gl_attrs = {}
        self.qc_check_file_size = {}
        new_checks_dict = yaml2dict(path_qc_checks_file)
        self.add_qc_checks_dict(dict_qc_checks=new_checks_dict)
        return self

    def replace_qc_checks_dict(self, dict_qc_checks: dict):
        """
        Method dedicated to replacing the current checks with the ones from a provided dictionary
        :param dict_qc_checks: the dictionary containing the checks
        :return: self
        """
        self.qc_checks_dims = {}
        self.qc_checks_vars = {}
        self.qc_checks_gl_attrs = {}
        self.qc_check_file_size = {}
        self.add_qc_checks_dict(dict_qc_checks=dict_qc_checks)
        return self

    def load_netcdf(self, nc_file_path: Path):
        """
        Method dedicated to loading a netCDF file to be checked with quality control
        :param nc_file_path: path to the netCDF file
        :return: self
        """
        self.nc = netCDF4.Dataset(nc_file_path)  # pylint: disable=no-member
        return self

    def boundary_check(self):
        """
        Method dedicated to checking whether the data for each variable in
        the loaded netCDF file is within the specified bounds.

        - logs an error to the logger if no netCDF file is loaded
        - logs a warning to the logger if a variable specified to be checked does
        not exist in the netCDF file
        - logs an error to the logger if a value is out of the specified bounds
        - writes a message to the logger whether a boundary check for a variable
        succeeded or failed
        :return: self
        """
        if self.nc is None:
            self.logger.add_error("boundary check error: no nc file loaded")
            return self

        vars_to_check = [
            var_name for var_name, properties in self.qc_checks_vars.items()
            if properties['is_data_within_boundaries_check']['perform_check']
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

            self.logger.add_info(f"boundary check for variable '{var_name}': {'success' if success else 'fail'}")
        return self

    def existence_check(self): # pylint: disable=too-many-branches
        """
        Method to perform existence checks on dimensions, variables and global attributes.

        - Logs an error if there is no netCDF loaded
        - Logs errors for each field which should exist but does not.
        - Logs info for each category how many of the checked fields exist.

        :return: self to make chaining calls possible
        """
        # Log an error if there is no netCDF loaded
        if self.nc is None:
            self.logger.add_error("existence check error: no nc file loaded")
            return self

        # Dimensions, variables, and global attributes from the netCDF dict
        nc_dimensions = self.nc.dimensions.keys()
        nc_variables = self.nc.variables.keys()
        nc_global_attributes = self.nc.ncattrs()

        # Dimensions, variables, and global attributes with 'does_it_exist_check' True in the config file
        dims_to_check = [dim for dim, properties in self.qc_checks_dims.items()
            if properties['does_it_exist_check'] is True]
        vars_to_check = [var for var, properties in self.qc_checks_vars.items()
            if properties['does_it_exist_check'] is True]
        attrs_to_check = [attr for attr, properties in self.qc_checks_gl_attrs.items()
            if properties['does_it_exist_check'] is True]

        checked = 0
        exist = 0

        # Loop over all dimension in the config file, log error if it should exist but does not
        for dim in dims_to_check:
            checked += 1
            if dim not in nc_dimensions:
                self.logger.add_error(error=f'dimension "{dim}" should exist but it does not')
            else:
                exist += 1

        # Log info about how many of the checked dimensions exist
        if checked != 0:
            self.logger.add_info(msg=f'{exist}/{checked} checked dimensions exist')
        else:
            self.logger.add_info(msg='no dimensions were checked')

        checked = 0
        exist = 0

        # Loop over all variables in the config file, log error if it should exist but does not
        for var in vars_to_check:
            checked += 1
            if var not in nc_variables:
                self.logger.add_error(error=f'variable "{var}" should exist but it does not')
            else:
                exist += 1

        # Log info about how many of the checked variables exist
        if checked != 0:
            self.logger.add_info(msg=f'{exist}/{checked} checked variables exist')
        else:
            self.logger.add_info(msg='no variables were checked')

        checked = 0
        exist = 0

        # Loop over all global attributes in the config file, log error if it should exist but does not
        for attr in attrs_to_check:
            checked += 1
            if attr not in nc_global_attributes:
                self.logger.add_error(error=f'global attribute "{attr}" should exist but it does not')
            else:
                exist += 1

        # Log info about how many of the checked global attributes exist
        if checked != 0:
            self.logger.add_info(msg=f'{exist}/{checked} checked global attributes exist')
        else:
            self.logger.add_info(msg='no global attributes were checked')

        return self

    def emptiness_check(self): # pylint: disable=too-many-branches, disable=too-many-statements
        """
        Method to perform emptiness checks on variables and global attributes.

        - Logs an error if there is no netCDF loaded
        - Logs errors for each variable and global attribute which should be fully populated but is not.
        - Logs info for each category how many of the checked fields are fully populated.

        :return: self to make chaining calls possible
        """
        # Log an error if there is no netCDF loaded
        if self.nc is None:
            self.logger.add_error("emptiness check error: no nc file loaded")
            return self

        # Variables and global attributes with 'is_it_empty_check' True in the config file
        vars_to_check = [var for var, properties in self.qc_checks_vars.items()
            if properties['is_it_empty_check'] is True]
        attrs_to_check = [attr for attr, properties in self.qc_checks_gl_attrs.items()
            if properties['is_it_empty_check'] is True]

        checked_vars = 0
        non_empty_vars = 0

        # Loop over all variables in the config file
        for var in vars_to_check:
            checked_vars += 1
            var_data = self.nc[var][:]

            checked_vals = 0
            empty_vals = 0
            nan_vals = 0

            # Check scalar values (e.g., longitude which just has one value assigned)
            if var_data.ndim == 0:
                val = var_data.item()
                if not val:
                    self.logger.add_error(error=f'scalar variable "{var}" is empty')
                elif np.isnan(val):
                    self.logger.add_error(error=f'scalar variable "{var}" is NaN')
                else:
                    non_empty_vars += 1
            # Loop over all data points for a variable
            else:
                for val in var_data:
                    checked_vals += 1

                    if not val:
                        empty_vals += 1
                    elif np.isnan(val):
                        nan_vals += 1

                # Log error if there are empty values
                if empty_vals > 0:
                    self.logger.add_error(error=f'variable "{var}" has {empty_vals}/{checked_vals} empty data points')

                # Log error if there are NaN values
                if nan_vals > 0:
                    self.logger.add_error(error=f'variable "{var}" has {nan_vals}/{checked_vals} NaN data points')

                if empty_vals == 0 and nan_vals == 0:
                    non_empty_vars += 1

        # Log info about how many of the checked variables exist
        if checked_vars != 0:
            self.logger.add_info(msg=f'{non_empty_vars}/{checked_vars} checked variables are fully populated')
        else:
            self.logger.add_info(msg='no variables were checked for emptiness')

        checked_attrs = 0
        non_empty_attrs = 0

        # Loop over all global attributes in the config file, log error if it should exist but does not
        for attr in attrs_to_check:
            checked_attrs += 1
            if not self.nc.getncattr(attr):
                self.logger.add_error(error=f'global attribute "{attr}" is empty')
            else:
                non_empty_attrs += 1

        # Log info about how many of the checked global attributes have values assigned
        if checked_attrs != 0:
            self.logger.add_info(
                msg=f'{non_empty_attrs}/{checked_attrs} checked global attributes have values assigned')
        else:
            self.logger.add_info(msg='no global attributes were checked for emptiness')

        return self

    def file_size_check(self):
        """
        Method to perform file size checks on the loaded netCDF file
        """

    def data_points_amount_check(self):
        """
        Method to perform amount of data points for each variable check. Method
        checks if the amount of data points is above a given threshold
        """

    def values_change_rate_check(self):
        """
        Method checks if values in variables data change at an acceptable rate
        """
        # Log an error if there is no NetCDF loaded
        if self.nc is None:
            self.logger.add_error("values change rate check error: no nc file loaded")
            return self

        # Variables with 'do_values_change_at_acceptable_rate_check' True in the config file
        vars_to_check = [var for var, properties in self.qc_checks_vars.items()
                         if properties["do_values_change_at_acceptable_rate_check"]['perform_check'] is True]

        vars_nc_file = list(self.nc.variables.keys())

        for var_name in vars_to_check:
            if var_name not in vars_nc_file:
                self.logger.add_warning(f"variable '{var_name}' not in nc file")
                continue

            var_values = self.nc[var_name][:]

            dimensions = self.qc_checks_vars[var_name]['do_values_change_at_acceptable_rate_check']['over_which_dimension']
            dimensions_acceptable_diff = self.qc_checks_vars[var_name]['do_values_change_at_acceptable_rate_check']['acceptable_difference']

            if not dimensions:
                self.logger.add_error(f"dimension/s to check not specified")
                continue
            if not dimensions_acceptable_diff:
                self.logger.add_error(f"acceptable differences to check not specified")
                continue

            if len(var_values.shape) < len(dimensions):
                self.logger.add_error(f"variable {var_name} doesn't have {len(dimensions)} dimensions")
                continue


            for d in dimensions:
                success = True
                difference_array = np.diff(var_values,axis=d)
                flat_difference_array = difference_array.flatten()

                try:
                    acceptable_difference = dimensions_acceptable_diff[d]
                except IndexError:
                    self.logger.add_error(f"threshold to check not specified")
                    success = False
                    continue
                for i in flat_difference_array:
                    difference = abs(i)
                    if difference > acceptable_difference:
                        success = False

                self.logger.add_info(f"value change rate check for variable '{var_name}' and dimension '{d}': {'success' if success else 'fail'}")

        return self


    def constant_values_check(self):
        """
        Method checks if values in variables data are constant for a suspicious amount of time
        """
        "'temperature': {'check_persistence': {'perform_check': True, 'dimension': time, 'data_points': 100}}"
        # Log an error if there is no NetCDF loaded
        if self.nc is None:
            self.logger.add_error("value persistence check error: no nc file loaded")
            return self

        # Variables with 'do_values_change_at_acceptable_rate_check' True in the config file
        vars_to_check = [var for var, properties in self.qc_checks_vars.items()
                         if properties["is_value_constant_for_too_long_check"]['perform_check'] is True]

        vars_nc_file = list(self.nc.variables.keys())

        for var_name in vars_to_check:
            if var_name not in vars_nc_file:
                self.logger.add_warning(f"variable '{var_name}' not in nc file")
                continue

            var_values = self.nc[var_name][:50]
            dimensions = self.qc_checks_vars[var_name]['is_value_constant_for_too_long_check']['over_which_dimensions']
            dimensions_thresholds = self.qc_checks_vars[var_name]['is_value_constant_for_too_long_check']['threshold_for_each_dimension']

            if not dimensions:
                self.logger.add_error(f"dimension/s to check not specified")
                continue
            if not dimensions_thresholds:
                self.logger.add_error(f"threshold/s to check not specified")
                continue
            if len(var_values.shape) < len(dimensions):
                self.logger.add_error(f"variable {var_name} doesn't have {len(dimensions)} dimensions")
                continue

            success = True
            for i in dimensions:
                var_values_data = np.rollaxis(var_values[:], i)
                data_size = var_values_data.shape[0]
                print(data_size)
                var_values_dimension = np.ravel(var_values_data)
                try:
                    threshold = dimensions_thresholds[i]
                except IndexError:
                    self.logger.add_error(f"threshold to check not specified")
                    success = False
                    continue

                if len(var_values_dimension) < threshold:
                    self.logger.add_info(f"length of variables values is smaller than threshold")
                    continue

                consecutive_value_counts = {}
                print(var_values_dimension[:50])

                if(len(dimensions)==1):

                    value_to_check_against = var_values_dimension[0]
                    count_consecutive = 1
                    for j in range(1, len(var_values_dimension)):
                        if var_values_dimension[j] == value_to_check_against:
                            count_consecutive += 1
                            if count_consecutive > threshold:
                                consecutive_value_counts[value_to_check_against] = count_consecutive
                                success = False
                        else:
                            value_to_check_against = var_values_dimension[z]
                            count_consecutive = 1
                    for value in consecutive_value_counts:
                        self.logger.add_info(
                            f"{var_name} has {consecutive_value_counts[value]} consecutive values {value}")

                    self.logger.add_info(
                        f"value persistence check for variable '{var_name}': {'success' if success else 'fail'}")

                    return self


                for j in range(0, len(var_values_dimension)-data_size,data_size):
                    value_to_check_against = var_values_dimension[j]
                    count_consecutive = 1
                    for z in range(j, data_size):
                        if var_values_dimension[z] == value_to_check_against:
                            count_consecutive += 1
                            if count_consecutive > threshold:
                                consecutive_value_counts[value_to_check_against] = count_consecutive
                                success = False
                        else:
                            value_to_check_against = var_values_dimension[z]
                            count_consecutive = 1

                self.logger.add_info(f"value persistence check for variable '{var_name}' and dimension '{i}': {'success' if success else 'fail'}")

        return self

    def expected_dimensions_vars_check(self):
        """
        Method dedicated to checking whether each variable has the expected dimensions
        """

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


if __name__ == '__main__':
    qc = QualityControl()
    nc_path = Path(__file__).parent.parent / 'sample_data' / '2024526_Green_Village-GV_THIES006.nc'
    yml_path =  Path(__file__).parent.parent / 'sample_data' / 'example_config.yaml'
    qc.add_qc_checks_dict(yaml2dict(yml_path))
    qc.load_netcdf(nc_path)
    qc.constant_values_check()
    print(qc.logger.info)
    print(qc.logger.errors)
