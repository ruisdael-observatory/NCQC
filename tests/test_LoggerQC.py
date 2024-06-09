"""
Module for testing the LoggerQC class from log.py
"""
import unittest
from unittest.mock import patch, Mock

from netcdfqc.log import LoggerQC


class TestLoggerQC(unittest.TestCase):
    """
    Class for testing the LoggerQC class

    Methods:
    - test_constructor_not_none: Test whether the constructor method creates an object
    - test_constructor: Test for the constructor method
    - test_add_error: Test for the add_error method
    - test_add_warning: Test for the add_warning method
    - test_add_info: Test for the add_info method
    - test_create_report: Test for the create_report method with a single report creation
    - test_create_report_mult_reports: Test for the create_report method with 2 report creations
    - test_get_latest_report_empty: Test for the get_latest_report method with no existing reports
    - test_get_latest_report: Test for the get_latest_report method with 2 existing reports
    - test_get_all_reports_empty: Test for the get_all_reports method with no existing reports
    - test_get_all_reports: Test for the get_all_reports method with 2 existing reports
    """
    def test_constructor_not_none(self):
        """
        Test whether the constructor method creates an object
        """
        assert LoggerQC() is not None

    def test_constructor(self):
        """
        Test for the constructor method
        """
        logger_obj = LoggerQC()
        assert not logger_obj.reports
        assert not logger_obj.info
        assert not logger_obj.errors
        assert not logger_obj.warnings

    def test_add_error(self):
        """
        Test for the add_error method
        """
        logger_obj = LoggerQC()
        logger_obj.add_error("example error")
        assert logger_obj.errors == ['example error']
        logger_obj.add_error("example error 2")
        assert logger_obj.errors == ['example error', 'example error 2']

    def test_add_warning(self):
        """
        Test for the add_warning method
        """
        logger_obj = LoggerQC()
        logger_obj.add_warning("example warning")
        assert logger_obj.warnings == ['example warning']
        logger_obj.add_warning("example warning 2")
        assert logger_obj.warnings == ['example warning', 'example warning 2']

    def test_add_info(self):
        """
        Test for the add_info method
        """
        logger_obj = LoggerQC()
        logger_obj.add_info("example message")
        assert logger_obj.info == ['example message']
        logger_obj.add_info("example message 2")
        assert logger_obj.info == ['example message', 'example message 2']

    @patch('netcdfqc.log.date')
    @patch('netcdfqc.log.datetime')
    def test_create_report(self, mock_datetime, mock_date):
        """
        Test for the create_report method with a single report creation
        :param mock_datetime: Mock object for the datetime call
        :param mock_date: Mock object fot the date call
        """
        mock_date_today = Mock()
        mock_date_today.strftime.return_value = "24-05-1914"
        mock_date.today.return_value = mock_date_today

        mock_datetime_now = Mock()
        mock_datetime_now.strftime.return_value = "19:14:00"
        mock_datetime.now.return_value = mock_datetime_now

        logger_obj = LoggerQC()
        logger_obj.info = ['info_1', 'info_2']
        logger_obj.errors = ['error_1']
        logger_obj.warnings = ['warning_1', 'warning_2']
        logger_obj.create_report()
        assert logger_obj.reports[0] == {
            'report_date': "24-05-1914",
            'report_time': "19:14:00",
            'errors': ['error_1'],
            'warnings': ['warning_1', 'warning_2'],
            'info': ['info_1', 'info_2']
        }
        assert not logger_obj.info
        assert not logger_obj.errors
        assert not logger_obj.warnings

    @patch('netcdfqc.log.date')
    @patch('netcdfqc.log.datetime')
    def test_create_report_mult_reports(self, mock_datetime, mock_date):
        """
        Test for the create_report method with 2 report creations
        :param mock_datetime: Mock object for the datetime call
        :param mock_date: Mock object for the date call
        """
        mock_date_today = Mock()
        mock_date_today.strftime.return_value = "24-05-1914"
        mock_date.today.return_value = mock_date_today

        mock_datetime_now = Mock()
        mock_datetime_now.strftime.return_value = "19:14:00"
        mock_datetime.now.return_value = mock_datetime_now

        logger_obj = LoggerQC()
        logger_obj.info = ['info_1', 'info_2']
        logger_obj.errors = ['error_1']
        logger_obj.warnings = ['warning_1', 'warning_2']
        logger_obj.create_report()
        logger_obj.info = ['info_3']
        logger_obj.warnings = []
        logger_obj.errors = ['error_3', 'error_4']
        logger_obj.create_report()
        assert logger_obj.reports[0] == {
            'report_date': "24-05-1914",
            'report_time': "19:14:00",
            'errors': ['error_1'],
            'warnings': ['warning_1', 'warning_2'],
            'info': ['info_1', 'info_2']
        }
        assert logger_obj.reports[1] == {
            'report_date': "24-05-1914",
            'report_time': "19:14:00",
            'errors': ['error_3', 'error_4'],
            'warnings': [],
            'info': ['info_3']
        }

    def test_get_latest_report_empty(self):
        """
        Test for the get_latest_report method with no existing reports
        """
        logger_obj = LoggerQC()
        assert logger_obj.get_latest_report() == {}

    def test_get_latest_report(self):
        """
        Test for the get_latest_report method with 2 existing reports
        """
        logger_obj = LoggerQC()
        logger_obj.reports = [{'test_report_1': 1}, {'test_report_2': 2}]
        assert logger_obj.get_latest_report() == {'test_report_2': 2}

    def test_get_all_reports_empty(self):
        """
        Test for the get_all_reports method with no existing reports
        """
        logger_obj = LoggerQC()
        assert not logger_obj.get_all_reports()

    def test_get_all_reports(self):
        """
        Test for the get_all_reports method with 2 existing reports
        """
        logger_obj = LoggerQC()
        logger_obj.reports = [{'test_report_1': 1}, {'test_report_2': 2}]
        assert logger_obj.get_all_reports() == [{'test_report_1': 1}, {'test_report_2': 2}]
