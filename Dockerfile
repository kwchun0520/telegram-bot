FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt requirements.txt
COPY src src
COPY config config
COPY main.py main.py
RUN pip install -r requirements.txt
CMD ["python", "-u", "main.py"]
