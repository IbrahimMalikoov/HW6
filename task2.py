
from abc import ABC, abstractmethod
from typing import List, Dict


# "Интерфейс" для Наблюдателя
class IObserver(ABC):
    @abstractmethod
    def update(self, currency_data: Dict[str, float]):
        """Получает обновление от субъекта."""
        pass


#"Интерфейс" для Субъекта
class ISubject(ABC):
    @abstractmethod
    def register(self, observer: IObserver):
        """Регистрация наблюдателя."""
        pass

    @abstractmethod
    def remove(self, observer: IObserver):
        """Удаление наблюдателя."""
        pass

    @abstractmethod
    def notify(self):
        """Уведомление всех наблюдателей."""
        pass


# Класс-субъект CurrencyExchange
class CurrencyExchange(ISubject):
    def __init__(self):
        self._observers: List[IObserver] = []
        self._rates: Dict[str, float] = {}

    def register(self, observer: IObserver):
        if observer not in self._observers:
            self._observers.append(observer)
            print(f"[Биржа]: Подписчик {type(observer).__name__} добавлен.")

    def remove(self, observer: IObserver):
        if observer in self._observers:
            self._observers.remove(observer)
            print(f"[Биржа]: Подписчик {type(observer).__name__} удален.")

    def notify(self):
        print("[Биржа]: Уведомление всех подписчиков...")
        for observer in self._observers:
            observer.update(self._rates)

    def set_rate(self, currency: str, rate: float):
        print(f"\n[Биржа]: Курс {currency} изменился на {rate:.4f}")
        self._rates[currency] = rate
        self.notify()


#Создайте несколько классов-наблюдателей
class BankDisplay(IObserver):
    """Наблюдатель, который просто отображает курсы на табло банка."""

    def update(self, currency_data: Dict[str, float]):
        print("--- Табло в банке ---")
        for currency, rate in currency_data.items():
            print(f"  {currency}/RUB: {rate:.4f}")
        print("---------------------")


class SmsNotifier(IObserver):
    """Наблюдатель, который отправляет SMS при изменении конкретной валюты."""

    def __init__(self, target_currency: str):
        self._target_currency = target_currency
        self._last_known_rate = 0.0

    def update(self, currency_data: Dict[str, float]):
        if self._target_currency in currency_data:
            new_rate = currency_data[self._target_currency]
            if new_rate != self._last_known_rate:
                print(f"[SMS Уведомление]: Новый курс {self._target_currency} - {new_rate:.4f} RUB")
                self._last_known_rate = new_rate


class TradingBot(IObserver):
    """Наблюдатель, имитирующий торгового робота с простой логикой."""

    def update(self, currency_data: Dict[str, float]):
        print("[Торговый бот]: Получены новые данные...")
        # Простая логика: если доллар дешевле 90 - покупаем, если евро дороже 100 - продаем
        if "USD" in currency_data and currency_data["USD"] < 90.0:
            print("  -> Решение: Покупать USD.")
        if "EUR" in currency_data and currency_data["EUR"] > 100.0:
            print("  -> Решение: Продавать EUR.")



if __name__ == "__main__":
    # Создаем субъект
    exchange = CurrencyExchange()

    # Создаем наблюдателей
    bank_display = BankDisplay()
    sms_to_client = SmsNotifier(target_currency="USD")
    bot = TradingBot()

    # Регистрируем наблюдателей
    exchange.register(bank_display)
    exchange.register(sms_to_client)
    exchange.register(bot)

    # Имитируем изменения курсов
    exchange.set_rate("USD", 89.50)
    exchange.set_rate("EUR", 98.75)

    # Еще одно изменение, чтобы показать работу SMS-уведомителя
    exchange.set_rate("USD", 89.55)

    # Удаляем одного из наблюдателей
    exchange.remove(bank_display)

    # Имитируем еще одно изменение. Табло банка больше не получит уведомление.
    exchange.set_rate("EUR", 101.20)