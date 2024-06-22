"""
Test module for the create_report method from the QualityControl class
"""
from pathlib import Path
from unittest.mock import patch, Mock

from ncqc.QCnetCDF import QualityControl

data_dir = Path(__file__).parent.parent / 'sample_data'


@patch('ncqc.log.date')
@patch('ncqc.log.datetime')
@patch('ncqc.QCnetCDF.Path.stat', return_value=Mock(st_size=15000))
def test_create_report(mock_path_stat, mock_datetime, mock_date):
    """
    Test for the create_report method from the QualityControl class
    :param mock_path_stat: Mock object for the Path.stat call
    :param mock_datetime: Mock object for the datetime call
    :param mock_date: Mock object fot the date call
    """
    mock_date_today = Mock()
    mock_date_today.strftime.return_value = "24-05-1914"
    mock_date.today.return_value = mock_date_today

    mock_datetime_now = Mock()
    mock_datetime_now.strftime.return_value = "19:14:00"
    mock_datetime.now.return_value = mock_datetime_now

    qc_obj = QualityControl()
    qc_obj.add_qc_checks_conf(data_dir / 'example_config.yaml')
    mock_nc = Mock()
    mock_nc.filepath.return_value = 'dummy/path'
    qc_obj.nc = mock_nc

    first_report = qc_obj.file_size_check().create_report()

    mock_path_stat.return_value = Mock(st_size=9000)

    second_report = qc_obj.file_size_check().create_report()

    mock_path_stat.return_value = Mock(st_size=15000)

    all_reports = qc_obj.file_size_check().create_report(get_all_reports=True)

    expected_first_report = {
        'report_date': "24-05-1914",
        'report_time': "19:14:00",
        'errors': [],
        'warnings': [],
        'info': ['file size check: SUCCESS']
    }

    expected_second_report = {
        'report_date': "24-05-1914",
        'report_time': "19:14:00",
        'errors': ['file size check error: size of loaded file (9000 bytes)'
                   'is out of bounds for bounds: [10000,20000]'],
        'warnings': [],
        'info': ['file size check: FAIL']
    }

    assert first_report == expected_first_report
    assert second_report == expected_second_report
    assert all_reports == [expected_first_report, expected_second_report, expected_first_report]
