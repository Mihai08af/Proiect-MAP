FROM python:3.11-slim
WORKDIR /app
COPY cod_full.py .
CMD ["python", "cod_full.py"]
