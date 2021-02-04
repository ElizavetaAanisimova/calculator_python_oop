import datetime as dt

TODAY = dt.date.today()


class Record:
    def __init__(self, amount, comment, date=None):
        self.amount = amount
        self.comment = comment
        if date is None:
            self.date = TODAY
        else:
            self.date = dt.datetime.strptime(date, "%d.%m.%Y").date()


class Calculator:
    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, record: Record):
        self.records.append(record)

    def get_today_stats(self):
        today_amount_list = [
            record.amount
            for record in self.records
            if record.date == TODAY
        ]
        return sum(today_amount_list)

    def get_week_stats(self):
        week_ago = TODAY - dt.timedelta(days=7)
        today_week_list = [
            record.amount
            for record in self.records
            if week_ago < record.date <= TODAY
        ]
        return sum(today_week_list)

    def calc_remained_difference(self):
        today_stats = self.get_today_stats()
        diff = self.limit - today_stats
        return diff


class CaloriesCalculator(Calculator):
    def get_calories_remained(self):
        diff = self.calc_remained_difference()
        if diff > 0:
            return ('Сегодня можно съесть что-нибудь ещё, '
                    f'но с общей калорийностью не более {diff} кКал')
        return 'Хватит есть!'


class CashCalculator(Calculator):
    EURO_RATE = 70.0
    USD_RATE = 60.0
    RUB_RATE = 1

    currency_name_rate = {
        'usd': (USD_RATE, 'USD'),
        'eur': (EURO_RATE, 'Euro'),
        'rub': (RUB_RATE, 'руб')
        }

    def get_today_cash_remained(self, currency):
        diff = self.calc_remained_difference()
        abs_diff = abs(diff)
        if diff == 0:
            return "Денег нет, держись"
        currency_rate, currency_name = self.currency_name_rate[currency]
        exchange = f'{round(abs_diff / currency_rate, 2)} {currency_name}'

        if diff > 0:
            return f"На сегодня осталось {exchange}"
        return f"Денег нет, держись: твой долг - {exchange}"
