FROM ubuntu:20.04

# Обновление пакетов и установка Python и pip
RUN apt-get update && \
    apt-get install -y python3 && \
    apt-get install -y python3-pip

WORKDIR /app

# Копирование исходных файлов в контейнер
COPY . /app

# Установка зависимостей Python
RUN pip3 install --no-cache-dir -r /app/requirements.txt

RUN chmod +x main.py test.sh

EXPOSE 8080

CMD ["uvicorn", "main:app", "--reload"]
