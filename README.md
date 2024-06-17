# NetCDF Quality Control Library

[[_TOC_]]

ncqc is a Python library for performing quality control on netCDF files. It was developed by TU Delft, within the framework of the Ruisdael observatory for atmospheric science. This library is focused around the `QualityControl` class, to which a netCDF file and configuration can be added to then perform quality control checks.

## Installation
(add something about installing the library)

## Usage
There are a couple steps to perform quality control checks. These are:
* Creating a configuration file or dictionary
* Setting up a QualityControl object
* Runnings checks with a QualityControl object
* Getting the report from a QualityControl object

### Creating a configuration file or dictionary
To remove the manual labor from setting up the configuration for the `QualityControl` object, there are two methods: `create_config_dict_from_yaml` and `create_config_dict_from_dict` to create the base for a configuration dictionary by parsing an existing .yaml file or dictionary respectively. By specifying the names of the groups containing the dimensions, variables and global attributes via the paramaters `dimensions_name`, `variables_name`, and `global_attributes_name`, these fields get added to the output dictionary with the structure for specifying what checks to perform already set up. Below is an example of how this can be used.

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

Example yaml file:
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

Example config dictionary:
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
            'dim1': {'does_it_exist_check': 'TODO'},
            'dim2': {'does_it_exist_check': 'TODO'}
        },
        'variables': {
            'var1': {
                'does_it_exist_check': 'TODO',
                'is_it_empty_check': 'TODO',
                'is_data_within_boundaries_check': {
                    'perform_check': 'TODO',
                    'lower_bound': 'TODO',
                    'upper_bound': 'TODO'
                },
                'are_there_enough_data_points_check': {
                    'perform_check': 'TODO',
                    'threshold': 'TODO',
                    'dimension': 'TODO'
                },
                'do_values_change_at_acceptable_rate_check': {
                    'perform_check': 'TODO',
                    'acceptable_difference': 'TODO'
                },
                'is_value_constant_for_too_long_check': {
                    'perform_check': 'TODO',
                    'threshold': 'TODO'
                }
            }
        },
        'global_attributes': {
            'glattr1': {
                'does_it_exist_check': 'TODO',
                'is_it_empty_check': 'TODO'
            },
            'glattr2': {
                'does_it_exist_check': 'TODO',
                'is_it_empty_check': 'TODO'
            }
        },
        'file_size': {
            'perform_check': 'TODO',
            'lower_bound': 'TODO',
            'upper_bound': 'TODO'
        }
    }
```

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
        'does_it_exist_check': 'TODO',
        'is_it_empty_check': 'TODO',
        'is_data_within_boundaries_check': {
            'perform_check': 'TODO',
            'lower_bound': 'TODO',
            'upper_bound': 'TODO'
        },
        'are_there_enough_data_points_check': {
            'perform_check': 'TODO',
            'threshold': 'TODO',
            'dimension': 'TODO'
        },
        'do_values_change_at_acceptable_rate_check': {
            'perform_check': 'TODO',
            'acceptable_difference': 'TODO'
        },
        'is_value_constant_for_too_long_check': {
            'perform_check': 'TODO',
            'threshold': 'TODO'
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

### Runnings checks with a QualityControl object
These are the quality control checks that can be performed on a `QualityControl` object with a set up configuration and loaded netCDF file:
* `boundary_check`: logs an error for each data point which falls outside of the variable bounds, which are specified in the configuration
* `existence_check`: logs an error for each dimension, variable, or global attribute which according to the configuration should be present in the netCDF file but is not, and logs info for each category how many of the checked fields exist
* `emptiness_check`: logs an error for each variable or global attribute which has (a) missing value(s), in the case of variables also specifying how many data poins are empty, and logs info for each category how many of the checked fields are fully populated
* `data_points_amount_check`: TODO
* `values_change_rate_check`: TODO
* `constant_values_check`: TODO
* `file_size_check`: TODO

Code example:

```python
# Separately
qc_obj.boundary_check()
qc_obj.file_size_check()

# Chained
qc_obj.existence_check().emptiness_check()
```

### Getting a report from a QualityControl object
Once quality control checks have been performed, it is possible to get a report by accessing the `LoggerQC` object of the `QualityControl` object:
* `create_report`: creates a dictionary containing the logged errors, warnings, and info, in addition to the date and time. This dictionary gets stored in the logger's list of repotrs. This method also automatically clears the logger's errors, warnings, and info.
* `get_latest_report`: returns the most recently created report
* `get_all_reports`: returns the full list of reports created so far

Code example:

```python
qc_obj.create_report()
report = qc_obj.get_latest_report()
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

## License
GPLv3. See [LICENSE](LICENSE)
