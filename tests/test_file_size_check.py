import unittest
from pathlib import Path
from unittest.mock import patch, Mock

from netcdfqc.QCnetCDF import QualityControl

data_dir = Path(__file__).parent.parent / 'sample_data'


class TestFileSizeCheck(unittest.TestCase):
    @patch('netcdfqc.QCnetCDF.Path.stat', return_value=Mock(st_size=15000))
    def test_file_size_check_success(self, mock_path_stat):
        qc_obj = QualityControl()
        qc_obj.add_qc_checks_conf(data_dir / 'example_config.yaml')
        mock_nc = Mock()
        mock_nc.filepath.return_value = 'dummy/path'
        qc_obj.nc = mock_nc
        res = qc_obj.file_size_check()
        assert res == qc_obj
        assert qc_obj.logger.info == ['file size check: SUCCESS']

    @patch('netcdfqc.QCnetCDF.Path.stat', return_value=Mock(st_size=9000))
    def test_file_size_check_fail(self, mock_path_stat):
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

    @patch('netcdfqc.QCnetCDF.Path.stat', return_value=Mock(st_size=10000))
    def test_file_size_check_lower_boundaries(self, mock_path_stat):
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

    @patch('netcdfqc.QCnetCDF.Path.stat', return_value=Mock(st_size=20000))
    def test_file_size_check_upper_boundaries(self, mock_path_stat):
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

    def test_file_size_check(self):
        qc_obj = QualityControl()
        qc_obj.add_qc_checks_conf(data_dir / 'example_config.yaml')
        qc_obj.qc_check_file_size.update({
            'perform_check': False,
            'lower_bound': 10000,
            'upper_bound': 20000
        })
        res = qc_obj.file_size_check()
        assert res == qc_obj
        assert not qc_obj.logger.errors
        assert not qc_obj.logger.warnings
        assert not qc_obj.logger.info
