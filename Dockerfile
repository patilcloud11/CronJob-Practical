FROM python:3.10-slim

WORKDIR /app

COPY main.py /app/

RUN pip install requests boto3

CMD ["python", "main.py"]