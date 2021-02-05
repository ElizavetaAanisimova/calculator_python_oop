import datetime as dt


class Record:
    def __init__(self, amount, comment, date=None):
        self.amount = amount
        self.comment = comment
        if date is None:
            self.date = dt.date.today()
        else:
            self.date = dt.datetime.strptime(date, "%d.%m.%Y").date()


class Calculator:
    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, record: Record):
        self.records.append(record)

    def get_today_stats(self):
        today = dt.date.today()
        today_amount_list = [
            record.amount
            for record in self.records
            if record.date == today
        ]
        return sum(today_amount_list)

    def get_week_stats(self):
        today = dt.date.today()
        week_ago = today - dt.timedelta(days=7)
        today_week_list = [
            record.amount
            for record in self.records
            if week_ago < record.date <= today
        ]
        return sum(today_week_list)

    def calc_remained_difference(self):
        return self.limit - self.get_today_stats()


class CaloriesCalculator(Calculator):
    def get_calories_remained(self):
        remain = self.calc_remained_difference()
        if remain > 0:
            return ('Сегодня можно съесть что-нибудь ещё, '
                    f'но с общей калорийностью не более {remain} кКал')
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
        remain = self.calc_remained_difference()
        abs_remain = abs(remain)
        if remain == 0:
            return "Денег нет, держись"
        if currency not in self.currency_name_rate:
            raise ValueError('Данная валюта пока не поддерживается')
        currency_rate, currency_name = self.currency_name_rate[currency]
        exchange = round(abs_remain / currency_rate, 2)
        result = f'{exchange} {currency_name}'
        if remain > 0:
            return f"На сегодня осталось {result}"
        return f"Денег нет, держись: твой долг - {result}"
