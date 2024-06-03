from pathlib import Path

import netCDF4
import yaml


class QualityControl:
    def __init__(self):
        self.qc_checks: dict = {}

    def add_qc_checks_conf(self, path_qc_checks_file: Path):
        new_checks_dict = yaml2dict(path_qc_checks_file)
        self.qc_checks.update(new_checks_dict)

    def add_qc_checks_dict(self, dict_qc_checks: dict):
        self.qc_checks.update(dict_qc_checks)

    def boundary_check(self, nc_file_path: Path):
        nc_file_dict = netCDF4.Dataset(nc_file_path)

        vars_to_check = list(self.qc_checks.keys())
        vars_nc_file = list(nc_file_dict.variables.keys())

        for var_name in vars_to_check:
            if var_name not in vars_nc_file:
                print(var_name, " not in netCDF file")
                continue

            lower_bound = self.qc_checks[var_name]['lower']
            upper_bound = self.qc_checks[var_name]['upper']

            var_values = nc_file_dict[var_name][:]

            for val in var_values:
                if val < lower_bound or val > upper_bound:
                    print("fail - ", var_name, " out of bounds")
                    return

        print("success")


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
    test_dict = {
        'velocity_spread': {
            'lower': 0.08,
            'upper': 3.3
        }
    }

    qc = QualityControl()
    qc.add_qc_checks_dict(test_dict)
    qc.boundary_check('20240430_Green_Village-GV_PAR008.nc')
