from abc import ABC, abstractmethod
from typing import Optional

class IPaymentStrategy(ABC):
    """
    Абстрактный базовый класс, определяющий интерфейс для всех стратегий оплаты.
    """

    @abstractmethod
    def pay(self, amount: float):
        """Метод для выполнения платежа."""
        pass


class CreditCardPaymentStrategy(IPaymentStrategy):
    """Стратегия для оплаты банковской картой."""

    def __init__(self, card_number: str, owner_name: str):
        self.card_number = card_number
        self.owner_name = owner_name

    def pay(self, amount: float):
        # Имитация процесса оплаты картой
        masked_card = "*" * (len(self.card_number) - 4) + self.card_number[-4:]
        print(f"Оплата {amount:.2f} руб. с помощью банковской карты {masked_card}.")
        print("Проверка данных владельца и отправка запроса в банк...")
        print("Платеж успешно выполнен.")


class PayPalPaymentStrategy(IPaymentStrategy):
    """Стратегия для оплаты через PayPal."""

    def __init__(self, email: str):
        self.email = email

    def pay(self, amount: float):
        # Имитация процесса оплаты через PayPal
        print(f"Оплата {amount:.2f} руб. через PayPal.")
        print(f"Перенаправление на страницу входа PayPal для пользователя {self.email}...")
        print("Подтверждение платежа...")
        print("Платеж успешно выполнен.")


class CryptoPaymentStrategy(IPaymentStrategy):
    """Стратегия для оплаты криптовалютой."""

    def __init__(self, wallet_address: str):
        self.wallet_address = wallet_address

    def pay(self, amount: float):
        # Имитация процесса оплаты криптовалютой
        print(f"Оплата {amount:.2f} руб. с помощью криптовалюты.")
        print(f"Создание транзакции для кошелька {self.wallet_address[:10]}...")
        print("Ожидание подтверждения в блокчейне...")
        print("Платеж успешно выполнен.")


class PaymentContext:
    """
    Контекст, который использует объект-стратегию для выполнения оплаты.
    """

    def __init__(self):
        self._strategy: Optional[IPaymentStrategy] = None

    def set_strategy(self, strategy: IPaymentStrategy):
        """Метод для установки стратегии оплаты."""
        self._strategy = strategy

    def execute_payment(self, amount: float):
        """Метод для выполнения оплаты с использованием выбранной стратегии."""
        if self._strategy is None:
            raise ValueError("Стратегия оплаты не выбрана.")

        print("-" * 30)
        self._strategy.pay(amount)
        print("-" * 30)


if __name__ == "__main__":
    payment_context = PaymentContext()

    amount_str = input("Введите сумму для оплаты: ").replace(',', '.')
    try:
        amount_to_pay = float(amount_str)
        if amount_to_pay <= 0:
            print("Сумма должна быть положительной.")
            exit()
    except ValueError:
        print("Неверный формат суммы.")
        exit()

    print("\nВыберите способ оплаты:")
    print("1 - Банковская карта")
    print("2 - PayPal")
    print("3 - Криптовалюта")

    choice = input("Ваш выбор: ")

    if choice == "1":
        card = input("Введите номер карты: ")
        name = input("Введите имя владельца: ")
        payment_context.set_strategy(CreditCardPaymentStrategy(card, name))
    elif choice == "2":
        email = input("Введите ваш PayPal email: ")
        payment_context.set_strategy(PayPalPaymentStrategy(email))
    elif choice == "3":
        wallet = input("Введите адрес вашего крипто-кошелька: ")
        payment_context.set_strategy(CryptoPaymentStrategy(wallet))
    else:
        print("Неверный выбор.")
        exit()

    # Выполнение оплаты
    try:
        payment_context.execute_payment(amount_to_pay)
    except ValueError as e:
        print(f"Ошибка: {e}")