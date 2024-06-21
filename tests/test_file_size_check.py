"""
Test module for the file size check
"""
import unittest
from pathlib import Path
from unittest.mock import patch, Mock

from ncqc.QCnetCDF import QualityControl

data_dir = Path(__file__).parent.parent / 'sample_data'


class TestFileSizeCheck(unittest.TestCase):
    """
    Class dedicated to testing the file_size_check method from QCnetCDF.py

     Methods:
    - test_file_size_check_success: Testing the file_size_check method
      from QCnetCDF.py with expected success
    - test_file_size_check_fail: Testing the file_size_check method from
      QCnetCDF.py with expected failure
    - test_file_size_check_lower_boundaries: Testing the file_size_check
      method from QCnetCDF.py with lower boundary value
    - test_file_size_check_upper_boundaries Testing the file_size_check
      method from QCnetCDF.py with upper boundary value
    - test_file_size_check_not_perform: Testing the file_size_check method
      from QCnetCDF.py with perform_check=False
    - test_no_nc_file: Testing the file_size_check method from QCnetCDF.py
      when there is no netCDF file loaded
    """

    @patch('ncqc.QCnetCDF.Path.stat', return_value=Mock(st_size=15000))
    def test_file_size_check_success(self, mock_path_stat):  # pylint: disable=unused-argument
        """
        Testing the file_size_check method from QCnetCDF.py with expected success
        :param mock_path_stat: Mock object for the Path.stat call
        """
        qc_obj = QualityControl()
        qc_obj.add_qc_checks_conf(data_dir / 'example_config.yaml')
        mock_nc = Mock()
        mock_nc.filepath.return_value = 'dummy/path'
        qc_obj.nc = mock_nc
        res = qc_obj.file_size_check()
        assert res == qc_obj
        assert qc_obj.logger.info == ['file size check: SUCCESS']

    @patch('ncqc.QCnetCDF.Path.stat', return_value=Mock(st_size=9000))
    def test_file_size_check_fail(self, mock_path_stat):  # pylint: disable=unused-argument
        """
        Testing the file_size_check method from QCnetCDF.py with expected failure
        :param mock_path_stat: Mock object for the Path.stat call
        """
        qc_obj = QualityControl()
        qc_obj.add_qc_checks_conf(data_dir / 'example_config.yaml')
        mock_nc = Mock()
        mock_nc.filepath.return_value = 'dummy/path'
        qc_obj.nc = mock_nc
        res = qc_obj.file_size_check()
        assert res == qc_obj
        assert qc_obj.logger.info == ['file size check: FAIL']
        assert qc_obj.logger.errors == ['file size check error: size of loaded file (9000 bytes)'
                                        'is out of bounds for bounds: [10000,20000]']

    @patch('ncqc.QCnetCDF.Path.stat', return_value=Mock(st_size=10000))
    def test_file_size_check_lower_boundaries(self, mock_path_stat):
        """
        Testing the file_size_check method from QCnetCDF.py with lower boundary value
        :param mock_path_stat: Mock object for the Path.stat call
        """
        qc_obj = QualityControl()
        qc_obj.add_qc_checks_conf(data_dir / 'example_config.yaml')
        mock_nc = Mock()
        mock_nc.filepath.return_value = 'dummy/path'
        qc_obj.nc = mock_nc
        res = qc_obj.file_size_check()
        assert res == qc_obj
        assert qc_obj.logger.info == ['file size check: SUCCESS']
        qc_obj.logger.info = []
        qc_obj.logger.errors = []
        qc_obj.logger.warnings = []
        mock_path_stat.return_value = Mock(st_size=9999)
        res = qc_obj.file_size_check()
        assert res == qc_obj
        assert qc_obj.logger.info == ['file size check: FAIL']
        assert qc_obj.logger.errors == ['file size check error: size of loaded file (9999 bytes)'
                                        'is out of bounds for bounds: [10000,20000]']

    @patch('ncqc.QCnetCDF.Path.stat', return_value=Mock(st_size=20000))
    def test_file_size_check_upper_boundaries(self, mock_path_stat):
        """
        Testing the file_size_check method from QCnetCDF.py with upper boundary value
        :param mock_path_stat: Mock object for the Path.stat call
        """
        qc_obj = QualityControl()
        qc_obj.add_qc_checks_conf(data_dir / 'example_config.yaml')
        mock_nc = Mock()
        mock_nc.filepath.return_value = 'dummy/path'
        qc_obj.nc = mock_nc
        res = qc_obj.file_size_check()
        assert res == qc_obj
        assert qc_obj.logger.info == ['file size check: SUCCESS']
        qc_obj.logger.info = []
        qc_obj.logger.errors = []
        qc_obj.logger.warnings = []
        mock_path_stat.return_value = Mock(st_size=20001)
        res = qc_obj.file_size_check()
        assert res == qc_obj
        assert qc_obj.logger.info == ['file size check: FAIL']
        assert qc_obj.logger.errors == ['file size check error: size of loaded file (20001 bytes)'
                                        'is out of bounds for bounds: [10000,20000]']

    def test_file_size_check_not_perform(self):
        """
        Testing the file_size_check method from QCnetCDF.py with perform_check=False
        """
        qc_obj = QualityControl()
        qc_obj.nc = Mock()
        qc_obj.add_qc_checks_conf(data_dir / 'example_config.yaml')
        qc_obj.qc_check_file_size = {}
        res = qc_obj.file_size_check()
        assert res == qc_obj
        assert not qc_obj.logger.errors
        assert not qc_obj.logger.warnings
        assert not qc_obj.logger.info

    def test_no_nc_file(self):
        """
        Testing the file_size_check method from QCnetCDF.py when there is no netCDF file loaded
        """
        qc_obj = QualityControl()
        res = qc_obj.file_size_check()
        assert res == qc_obj
        assert qc_obj.logger.errors == ['file_size_check error: no nc file loaded']
