FROM python:3.10

RUN apt-get update -y
RUN apt-get install -y python3-pip
RUN mkdir /app/

COPY ./requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

COPY . /app/
WORKDIR /app/

ENV PRJPATH /app/

# Добавление команды для предоставления прав на выполнение файла
RUN chmod +x restart_build.sh
RUN chmod +x run_server.sh

EXPOSE 8000

# Запуск основного файла
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
