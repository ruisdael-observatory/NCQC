# NetCDF Quality Control Library

[[_TOC_]]

ncqc is a Python library for performing quality control on netCDF files. It was developed by TU Delft, within the framework of the Ruisdael observatory for atmospheric science. This library is focused around the `QualityControl` class, to which a netCDF file and configuration can be added to then perform quality control checks.

## Installation
### Installing from source
Installing ncqc from source requires two steps: creating a wheel file, and using that to install the library. This is done by running the following commands:
```
pip install wheel
pip install setuptools
pip install twine

python setup.py bdist_wheel

pip install ./dist/ncqc-0.1.0-py3-none-any.whl
```

## Usage
There are a couple steps to perform quality control checks. These are:
* [Creating a configuration file or dictionary](#creating-a-configuration-file-or-dictionary)
* [Setting up a QualityControl object](#setting-up-a-qualitycontrol-object)
* [Running checks with a QualityControl object](#running-checks-with-a-qualitycontrol-object)
* [Getting a report from a QualityControl object](#getting-a-report-from-a-qualitycontrol-object)

### Creating a configuration file or dictionary
To remove the manual labor from setting up the configuration for the `QualityControl` object, there are two methods: `create_config_dict_from_yaml` and `create_config_dict_from_dict` to create the base for a configuration dictionary by parsing an existing .yaml file or dictionary respectively. By specifying the names of the groups containing the dimensions, variables and global attributes via the paramaters `dimensions_name`, `variables_name`, and `global_attributes_name`, these fields get added to the output dictionary with the structure for specifying what checks to perform already set up. The types for all the values are given, but the specific values will still need to be filled in. Below is an example of how this can be used and a link to the respective in- and outputs.

Method call:
```python
# with a yaml file
output_dict = create_config_dict_from_yaml(
    input_dict=path_to_yaml_file,
    dimensions_name="dims",
    variables_name="vars",
    global_attributes_name="gl_attrs"
)

# with a dictionary
output_dict = create_config_dict_from_dict(
    input_dict=config_dictionary,
    dimensions_name="dims",
    variables_name="vars",
    global_attributes_name="gl_attrs"
)
```
[Example in- and outputs](#example-for-creating-a-configuration-file-or-dictionary)

Some input dictionaries might have variables where the name is not at the top layer, for example with this structure:

```yaml
fields:
    '01':
        dimensions:
            - time                              
        attrs:
            units: 'mm/h'
            long_name: 'Rain intensity'
            short_name: 'rain_intensity'
```

`variables_name=fields` would result in `01` getting added as the name of the variable to check, so for names at a deeper layer there is `other_variable_name_paths`, which can take multiple lists which specify the path to a variable's name. `other_variable_name_paths=[['fields', 'attrs', 'short_name']]` will cause it to loop over all items in `fields` and then access the name by following the remainder of the path, so here this would be `input_dict['fields']['01']['attrs']['short_name']`, resulting the following output:

```python
'variables': {
    'field_1': {
        'existence_check': 'bool',
        'emptiness_check': 'bool',
        'data_boundaries_check': {
            'lower_bound': 'int',
            'upper_bound': 'int'
        },
        'data_points_amount_check': {
            'minimum': 'int'
        },
        'adjacent_values_difference_check': {
            'over_which_dimension': 'List[int]',
            'maximum_difference': 'List[int]'
        },
        'consecutive_identical_values_check': {
            'maximum': 'int'
        }
    }
}
```

### Setting up a QualityControl object
The following methods can be used with a `QualityControl` object to set up the quality control:
* `add_qc_checks_conf` / `add_qc_checks_dict`: adds what dimensions, variables, and global attriibutes should be checked for what checks by passing a .yaml file or a dictionary
* `replace_qc_checks_conf` / `replace_qc_checks_dict`: similar to the previous two functions, but removes any previously added checks
* `load_netcdf`: stores the netCDF file at the given path in the `QualityControl` object

Code example:

```python
qc_obj = QualityControl()

qc_obj.add_qc_checks_dict(config_dictionary)
qc_obj.replace_qc_check_dict(path_to_yaml_file)

qc_obj.load_netcdf(nc_path)
```

### Running checks with a QualityControl object
These are the quality control checks that can be performed on a `QualityControl` object with a set up configuration and loaded netCDF file:
* `file_size_check`: logs an error of the size of the provided netCDF file falls outside of the specified bounds
* `existence_check`: logs an error for each dimension, variable, or global attribute which according to the configuration should be present in the netCDF file but is not, and logs info for each category how many of the checked fields exist
* `emptiness_check`: logs an error for each variable or global attribute which has (a) missing value(s), in the case of variables also specifying how many data poins are empty, and logs info for each category how many of the checked fields are fully populated
* `data_points_amount_check`: logs an error for each variable which has less data points than the specified minimum data points for that variable
* `data_boundaries_check`: logs an error for each data point which falls outside of the specified variable bounds
* `consecutive_identical_values_check`: logs an error for each variable which has more consecutive identical than the specified maximum for that variable
* `adjacent_values_difference_check`: logs an error if the difference between two adjacent data points is greater than the specified maximum difference for that variable
Additionally, calling the method `perform_all_checks` will run all the previously mentioned checks in the order of that list.

Code example:

```python
# Separately
qc_obj.data_boundaries_check()
qc_obj.file_size_check()

# Chained
qc_obj.existence_check().emptiness_check()

# All checks
qc_obj.perform_all_checks()
```

### Getting a report from a QualityControl object
Once quality control checks have been performed, it is possible to get a report by accessing the `LoggerQC` object of the `QualityControl` object:
* `create_report`: creates a dictionary containing the logged errors, warnings, and info, in addition to the date and time. This dictionary gets stored in the logger's list of reports. This method also automatically clears the logger's errors, warnings, and info, so future reports won't contain old logs. `create_report` takes a boolean parameter `get_all_reports`, and if that is true it will return the list of all reports, otherwise it will return only most recently created report.

Code example:

```python
# Create a report and access it
latest_report = qc_obj.create_report(get_all_reports=false)

qc_obj.perform_all_checks()

# Create a new report and access all reports
all_reports = qc_obj.create_report(get_all_reports=true)
```

## Contributing
(add something about how to contribute)

## Authors and acknowledgment
ncqc is developed in the context of the [Ruisdael Observatory](https://ruisdael-observatory.nl/) by

* Vasil Chirov
* Mels Lutgerink
* Ella Milinovic
* Noky Soekarman
* Jesse Vleeschdraager

## Example for creating a configuration file or dictionary

Example yaml file (input):
```yaml
dims:
  dim1:
    # ...
  dim2:
    # ...

vars:
  var1:
    # ...

gl_attrs:
  glattr1: 'text1'
  glattr2: 'text2'
```

Example config dictionary (input):
```python
{
    'dims': {
        'dim1': 'value1',
        'dim2': 'value2'
    },
    'vars': {
        'var1': 'value1',
    },
    'gl_attrs': {
        'glattr1': 'value1'
        'glattr2': 'value2'
    }
}
```

Example output dictionary:
```python
{
        'dimensions': {
            'dim1': {'existence_check': 'bool'},
            'dim2': {'existence_check': 'bool'}
        },
        'variables': {
            'var1': {
                'existence_check': 'bool',
                'emptiness_check': 'bool',
                'data_boundaries_check': {
                    'lower_bound': 'int',
                    'upper_bound': 'int'
                },
                'data_points_amount_check': {
                    'minimum': 'int'
                },
                'adjacent_values_difference_check': {
                    'over_which_dimension': 'List[int]',
                    'maximum_difference': 'List[int]'
                },
                'consecutive_identical_values_check': {
                    'maximum': 'int'
                }
            }
        },
        'global_attributes': {
            'glattr1': {
                'existence_check': 'bool',
                'emptiness_check': 'bool'
            },
            'glattr2': {
                'existence_check': 'bool',
                'emptiness_check': 'bool'
            }
        },
        'file_size': {
            'lower_bound': 'int',
            'upper_bound': 'int'
        }
    }
```

## License
GPLv3. See [LICENSE](LICENSE)
