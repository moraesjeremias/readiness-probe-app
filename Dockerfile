FROM python:3.10.9-alpine

WORKDIR /app
ADD *.py /app/
RUN apk update && apk add curl && pip install --no-cache-dir .
ENTRYPOINT ["python", "main.py"]
EXPOSE 8081