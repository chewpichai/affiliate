import datetime
import calendar


def add_months(sourcedate, months):
  month = sourcedate.month - 1 + months
  year = int(sourcedate.year + month / 12 )
  month = month % 12 + 1
  day = min(sourcedate.day, calendar.monthrange(year, month)[1])
  return datetime.date(year, month, day)


def get_end_of_month(date):
  return add_months(date, 1) - datetime.timedelta(days=1)
