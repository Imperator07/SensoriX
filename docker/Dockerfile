FROM python:3.12-alpine3.19

WORKDIR /app/webserver
COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY webserver.py .

CMD ["python", "webserver.py"]
