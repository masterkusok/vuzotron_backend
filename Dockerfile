FROM python:3.11-bullseye
LABEL authors="Фёдор"

WORKDIR /app/
COPY ./requirements.txt  /app
RUN pip3 install -r requirements.txt
COPY ./ /app

ENTRYPOINT ["python3"]
CMD ["-m", "uvicorn", "backend.asgi:application", "--host", "0.0.0.0"]
