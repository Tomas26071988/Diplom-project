
def send_sms(phone_number: str, message: str, api_key: str):
    try:
        # Демонстрируем отправку SMS
        print(f"Сообщение для отправки: '{message}' на номер: {phone_number}")
        return "SMS успешно 'отправлено'"
    except Exception as e:
        print(f"Не удалось отправить SMS: {e}")
        return "Ошибка при отправке SMS"
