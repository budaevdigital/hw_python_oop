"""Калькулятор 2 в 1. Помогает с расчётами финансов и подсчетом каллорий."""

import datetime as dt
from datetime import timedelta
from typing import Union

FORMAT = "%d.%m.%Y"


class Calculator:
    """
    Основной класс, который создаёт записи для объектов
    и производит основные расчёты
    """
    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, some_record):
        self.records.append(some_record)

    def get_today_stats(self) -> float:
        spending_today = 0
        for item in self.records:
            if item.date == (dt.datetime.now()).date():
                spending_today += item.amount
        return spending_today

    def get_week_stats(self) -> float:
        spending_week = 0
        date_7days_ago = dt.datetime.now().date() - timedelta(days=7)
        for item in self.records:
            if (item.date <= (dt.datetime.now()).date()
                    and item.date >= date_7days_ago):
                spending_week += item.amount
        return spending_week


class Record:
    """
    Отдельный класс для создания записей под объекты
    """
    def __init__(self, amount: Union[int, float], comment,
                 date: str = (dt.datetime.now()).date()):
        self.amount = amount
        self.comment = comment
        if date is str:
            self.date = (dt.datetime.strptime(date, FORMAT)).date()
        else:
            self.date = date
        # if date is None:
        #     self.date = (dt.datetime.now()).date()
        # else:
        #     self.date = (dt.datetime.strptime(date, FORMAT)).date()

    # def __str__(self):
    #     return f'{self.amount}, {self.comment}, {self.date}'

    def __repr__(self):
        return self.amount, self.comment, self.date


class CaloriesCalculator(Calculator):
    """
    Калькулятор калорий
    """
    def __init__(self, limit):
        super().__init__(limit)

    def get_calories_remained(self):
        calories_today = Calculator.get_today_stats(self)
        print(calories_today)
        left_calories_today = self.limit - calories_today
        if self.limit > left_calories_today and left_calories_today > 0:
            return (f'Сегодня можно съесть что-нибудь ещё, '
                    f'но с общей калорийностью не более '
                    f'{left_calories_today} кКал')
        elif self.limit < left_calories_today or left_calories_today <= 0:
            return 'Хватит есть!'

    def get_today_stats(self):
        calories_today = Calculator.get_today_stats(self)
        return f'Съедено сегодня {calories_today} калорий'

    def get_week_stats(self):
        calories_week = Calculator.get_week_stats(self)
        return f'Съедено за неделю {calories_week} калорий'


class CashCalculator(Calculator):
    """
    Калькулятор денег
    """
    def __init__(self, limit):
        super().__init__(limit)

    def get_today_cash_remained(self, currency: str = 'rub') -> str:
        USD_RATE = 75
        EURO_RATE = 88
        currency = currency.lower()

        spending_today = Calculator.get_today_stats(self)

        print(spending_today)
        cash_left_today = self.limit - spending_today
        print(type(cash_left_today))

        if self.limit == int(spending_today):
            return 'Денег нет, держись'

        elif self.limit > spending_today:
            if currency == 'usd':
                cash_left_today = cash_left_today / USD_RATE
                return f'На сегодня осталось {cash_left_today:.2f} USD'
            elif currency == 'eur':
                cash_left_today = cash_left_today / EURO_RATE
                return f'На сегодня осталось {cash_left_today:.2f} Euro'
            else:
                return f'На сегодня осталось {cash_left_today:.2f} Руб'

        elif self.limit < spending_today:
            if currency == 'usd':
                cash_left_today = cash_left_today / USD_RATE
                return (f'Денег нет, держись: твой долг '
                        f'- {abs(cash_left_today):.2f} USD')
            elif currency == 'eur':
                cash_left_today = cash_left_today / EURO_RATE
                return (f'Денег нет, держись: твой долг '
                        f'- {abs(cash_left_today):.2f} Euro')
            else:
                return (f'Денег нет, держись: твой долг '
                        f'- {abs(cash_left_today):.2f} Руб')

    def get_today_stats(self):
        spending_today = Calculator.get_today_stats(self)
        return f'Потрачено сегодня {spending_today:.2f} Руб'

    def get_week_stats(self):
        spending_week = Calculator.get_week_stats(self)
        return f'Потрачено за неделю {spending_week:.2f} Руб'


cash_calculator = CashCalculator(1000)

cash_calculator.add_record(Record(amount=300, comment='Серёге за обед'))
cash_calculator.add_record(Record(amount=150, comment='Серёге'))
cash_calculator.add_record(Record(amount=800.70, comment='за обед'))
cash_calculator.add_record(Record(amount=145,
                                  comment='Безудержный шопинг',
                                  date='22.04.2022'))
cash_calculator.add_record(Record(amount=329,
                                  comment='Безудержный шопинг',
                                  date='18.04.2022'))
cash_calculator.add_record(Record(amount=478.23,
                                  comment='Безудержный шопинг',
                                  date='16.04.2022'))
cash_calculator.add_record(Record(amount=145,
                                  comment='Безудержный шопинг',
                                  date='11.04.2022'))

print(cash_calculator.get_today_cash_remained(currency='RUB'))
print(cash_calculator.get_week_stats())
print(cash_calculator.get_today_stats())

calories_calculator = CaloriesCalculator(300)

calories_calculator.add_record(Record(amount=800.30, comment='Обед'))
calories_calculator.add_record(Record(amount=395,
                                      comment='пироженка',
                                      date='18.04.2022'))

print(calories_calculator.get_calories_remained())
print(calories_calculator.get_week_stats())
print(calories_calculator.get_today_stats())
