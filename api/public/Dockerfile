FROM python:3.11.0-slim-bullseye

WORKDIR /app

COPY . ./

RUN pip3 install --upgrade pip

RUN pip3 install pipenv

RUN pipenv install --deploy --system

CMD ["python3", "main.py"]
