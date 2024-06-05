from datetime import date, datetime


class LoggerQC:
    def __init__(self):
        self.reports: list[dict] = list()
        self.errors = list()
        self.warnings = list()
        self.info = list()

    def add_error(self, error: str):
        self.errors.append(error)

    def add_warning(self, warning: str):
        self.warnings.append(warning)

    def add_info(self, msg: str):
        self.info.append(msg)

    def create_report(self):
        report_dict = {
            'report_date': date.today().strftime("%d-%m-%Y"),
            'report_time': datetime.now().strftime("%H:%M:%S"),
            'errors': self.errors,
            'warnings': self.warnings,
            'info': self.info
        }
        self.reports.append(report_dict)
        self.errors = list()
        self.warnings = list()
        self.info = list()

    def get_latest_report(self) -> dict:
        if len(self.reports) == 0:
            return {}
        return self.reports[len(self.reports) - 1]

    def get_all_reports(self) -> list[dict]:
        return self.reports


if __name__ == '__main__':
    logger = LoggerQC()
    logger.add_error("maika ti e mazh")
    logger.create_report()
    report = logger.get_latest_report()
    print(report)
