"""
Module dedicated to the implementation of the logger for the netCDF quality control library
"""
from datetime import date, datetime


class LoggerQC:
    """
    Class dedicated to logging errors, warnings, info, and creating
    reports for the netCDF quality control library

     Attributes:
    - reports: list of created reports
    - errors: list of logged errors for the report being created
    - warnings: list of logged warnings for the report being created
    - info: list of messages for the report being created

     Methods:
    - add_error: method to add an error
    - add_warning: method to add info
    - add_info: method to add a message
    - create_report: method to create a report
    - get_latest_report: method to get the latest report
    - get_all_reports: method to get all reports
    """

    def __init__(self):
        """
        Constructor for the logger object
        """
        self.reports: list[dict] = []
        self.errors = []
        self.warnings = []
        self.info = []

    def add_error(self, error: str):
        """
        Method dedicated to adding an error to the report being made
        :param error: error to be added
        """
        self.errors.append(error)

    def add_warning(self, warning: str):
        """
        Method dedicated to adding a warning to the report being made
        :param warning: warning to be added
        """
        self.warnings.append(warning)

    def add_info(self, msg: str):
        """
        Method dedicated to adding a message to the report being made
        :param msg: message to be added
        """
        self.info.append(msg)

    def create_report(self):
        """
        Method dedicated to creating a report and adding it to the list of reports

        - the method creates a report in the form of a dictionary, adds it to the
          list of reports, and resets the objects attributes
        """
        report_dict = {
            'report_date': date.today().strftime("%d-%m-%Y"),
            'report_time': datetime.now().strftime("%H:%M:%S"),
            'errors': self.errors,
            'warnings': self.warnings,
            'info': self.info
        }
        self.reports.append(report_dict)
        self.errors = []
        self.warnings = []
        self.info = []

    def get_latest_report(self) -> dict:
        """
        Method dedicated to getting the latest report made
        :return: the latest report
        """
        if len(self.reports) == 0:
            return {}
        return self.reports[len(self.reports) - 1]

    def get_all_reports(self) -> list[dict]:
        """
        Method dedicated to getting all reports made
        :return: all reports
        """
        return self.reports
