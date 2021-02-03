import datetime as dt


class Record:
    def __init__(self, amount, comment, date=None):
        self.amount = amount
        self.comment = comment
        if date is None:
            self.date = dt.datetime.now().date()
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
            if record.date == dt.datetime.now().date()
        ]
        return sum(today_amount_list)

    def get_week_stats(self):
        today = dt.datetime.now().date()
        max_day_last_week = today - dt.timedelta(days=7)
        today_week_list = [
            record.amount
            for record in self.records
            if record.date > max_day_last_week and record.date <= today
        ]
        return sum(today_week_list)


class CaloriesCalculator(Calculator):
    def get_calories_remained(self):
        today_stats = self.get_today_stats()
        dif = self.limit - today_stats
        if today_stats < self.limit:
            return ('Сегодня можно съесть что-нибудь ещё, ' +
                    f'но с общей калорийностью не более {dif} кКал')
        else:
            return 'Хватит есть!'


class CashCalculator(Calculator):
    USD_RATE = 60.0
    EURO_RATE = 70.0

    def get_today_cash_remained(self, currency):
        today_stats = self.get_today_stats()
        dif = abs(self.limit - today_stats)
        if currency == "usd":
            exchange = f"{round(dif / self.USD_RATE, 2)} USD"
        elif currency == "eur":
            exchange = f"{round(dif / self.EURO_RATE, 2)} Euro"
        else:
            exchange = f"{dif} руб"

        if today_stats < self.limit:
            return f"На сегодня осталось {exchange}"
        elif today_stats == self.limit:
            return "Денег нет, держись"
        else:
            return f"Денег нет, держись: твой долг - {exchange}"
