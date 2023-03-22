FROM python:3.10-buster


WORKDIR /app
COPY requirements.txt .

RUN apt-get update && apt-get install -y \
    wkhtmltopdf
RUN pip install -r requirements.txt

COPY . .

# run
CMD ["python", "bot.py"]
