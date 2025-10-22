# Dezhurstvo
ТГ бот для определения людей на дежурство
Создай репозиторий с 4 файлами: main.py, requirements.txt, Procfile, README.md.

В main.py вставь токен бота (или используй переменную окружения BOT_TOKEN).

Локально (опционально): python -m venv venv && source venv/bin/activate && pip install -r requirements.txt && python main.py.

Деплой на Render:

Создай аккаунт → New → Background Worker → подключи репозиторий.

Environment: PYTHON_VERSION=3.11, BOT_TOKEN=....

Start command возьмётся из Procfile (worker: python main.py).

Deploy. Бот запустится и будет работать на long polling.

Добавь бота в нужную группу, дай право отправлять сообщения, напиши в группе /start.

Проверь /month, /today. До 20:00 можно принудительно вызвать планирование командой /override Имя1 Имя2 YYYY-MM-DD или отметить отсутствие /absent Имя YYYY-MM-DD.

Примечания

Объявление в 20:00 публикует pair на следующую календарную дату (ночь 02–08).

31-го числа логика позволяет перешагнуть лимит при дефиците людей.

Команды и имена чувствительны к точному написанию (как в списке USERS в main.py).

Для вебхуков ничего не нужно — long polling надёжно работает на Render Worker.
