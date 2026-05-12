

import datetime as dt

overdue_amount = 8_554_625

from_date = dt.date(2013, 9, 14)
to_date = dt.date(2023, 10, 31)

days = to_date - from_date


late_fee = overdue_amount * 0.05
interest_amount = overdue_amount * (0.3 / 365) * days.days

total_pay = overdue_amount + late_fee + interest_amount

print("Total payment: ", total_pay / 1e6, "in million VND")
