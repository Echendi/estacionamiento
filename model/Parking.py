from datetime import datetime
from datetime import timedelta


def convert_time(time_millis):
    return datetime.now() - timedelta(seconds=time_millis / 1000)


class Record:
    start_time: datetime
    end_time: datetime

    def __init__(self, duration):
        self.start_time = convert_time(duration)
        self.end_time = datetime.now()

    def time_in_seconds(self) -> int:
        return int((self.end_time - self.start_time).total_seconds())

    def __str__(self) -> str:
        return "Start time " + self.start_time


class Parking:
    id: int

    # Constructor
    def __init__(self, parking_id: int):
        self.id = parking_id
        self.records = []

    def add_record(self, record):
        self.records.append(record)

    def avg_time(self) -> float:
        return sum(record.time_in_seconds() for record in self.records) / len(self.records) if len(
            self.records) > 0 else 0

    def records_per_hour(self) -> {}:
        records_per_hour = {}

        for record in self.records:
            hour = record.start_time.minute
            if hour not in records_per_hour:
                records_per_hour[hour] = 1
            else:
                records_per_hour[hour] += 1
        return records_per_hour
