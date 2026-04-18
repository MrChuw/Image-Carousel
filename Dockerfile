FROM python:3.12

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

ENV ANALYTICS_URL=""
ENV ANALYTICS_UUID=""

CMD ["python", "main.py"]