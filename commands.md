# Выполняемые действия

@BotFather - создание бота, копирование токена в .env
@mar27_25bot

python -m venv venv
. venv/scripts/activate

pip install --upgrade pip
pip install -r requirements.txt

Для создания тестовой базы данных
cd database
python create_database.py
