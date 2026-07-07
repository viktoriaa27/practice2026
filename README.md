# Учёт художественных материалов
Приложение для введения учёта художественных материалов с возможностью отслеживания количества материала
## Запуск проекта
1 Создайте виртуальное окружение: `python -m venv venv`

2 Активируйте:
- Windows: `venv\Scripts\activate`
- macOS/Linux: `source venv/bin/activate`
  
3 Установите зависимости: `pip install -r requirements.txt`
  
4 Запустите: `python main.py`
## Структура проекта
- `main.py` → Точка входа, настройка `QApplication`
- `ui_main.py` → Интерфейс, сигналы, обработка событий
- `database.py` → Работа с SQLite (CRUD)
- `images/` → Ресурсы (изображения, иконки)
