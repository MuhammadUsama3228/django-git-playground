FROM python:3.12-alpine

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONNUMBUFFERED=1

WORKDIR /app/

COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

# container port
EXPOSE 8000

COPY devops/entrypoint.sh /app/

RUN chmod +x /app/entrypoint.sh

CMD ["./entrypoint.sh"]
