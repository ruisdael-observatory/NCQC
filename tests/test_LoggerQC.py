import unittest

from netcdfqc.log import LoggerQC


class TestLoggerQC(unittest.TestCase):
    def test_constructor(self):
        assert LoggerQC() is not None

    def test_add_error(self):
        logger_obj = LoggerQC()
        logger_obj.add_error("example error")
        assert logger_obj.errors == ['example error']
        logger_obj.add_error("example error 2")
        assert logger_obj.errors == ['example error', 'example error 2']

    def test_add_warning(self):
        logger_obj = LoggerQC()
        logger_obj.add_warning("example warning")
        assert logger_obj.warnings == ['example warning']
        logger_obj.add_warning("example warning 2")
        assert logger_obj.warnings == ['example warning', 'example warning 2']

    def test_add_info(self):
        logger_obj = LoggerQC()
        logger_obj.add_info("example message")
        assert logger_obj.info == ['example message']
        logger_obj.add_info("example message 2")
        assert logger_obj.info == ['example message', 'example message 2']

