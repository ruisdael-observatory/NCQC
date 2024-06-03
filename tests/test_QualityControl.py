import unittest
from unittest.mock import patch

from netcdfqc.QCnetCDF import QualityControl


class TestQualityControl(unittest.TestCase):

    @patch('netcdfqc.QCnetCDF.yaml2dict')
    def test_add_qc_checks_conf(self, mock_yaml2dict):
        qc_obj = QualityControl()
        qc_obj.qc_checks = {
            'v1': {
                'l': 1,
                'r': 2
            }
        }

        def my_side_effect(arg):
            if arg == 'path':
                new_checks_dict = {
                    'v2': {
                        'l': 2,
                        'r': 3
                    }
                }
                return new_checks_dict
            else:
                return {}

        mock_yaml2dict.side_effect = my_side_effect

        expected_result = {
            'v1': {
                'l': 1,
                'r': 2
            },
            'v2': {
                'l': 2,
                'r': 3
            }
        }

        qc_obj.add_qc_checks_conf('path')
        assert qc_obj.qc_checks == expected_result

        qc_obj.qc_checks = {
            'v1': {
                'l': 1,
                'r': 2
            }
        }
        qc_obj.add_qc_checks_conf('wrong_path')
        assert qc_obj.qc_checks == {
            'v1': {
                'l': 1,
                'r': 2
            }
        }

    def test_add_qc_checks_dict(self):
        qc_obj = QualityControl()
        qc_obj.qc_checks = {
            'v1': {
                'l': 1,
                'r': 2
            }
        }
        new_checks = {
            'v2': {
                'l': 2,
                'r': 3
            }
        }

        expected_result = {
            'v1': {
                'l': 1,
                'r': 2
            },
            'v2': {
                'l': 2,
                'r': 3
            }
        }

        qc_obj.add_qc_checks_dict(new_checks)

        assert qc_obj.qc_checks == expected_result
