FROM python:3.10-buster

# pip install -r requirements.txt
WORKDIR /app
COPY . .

# install requirements
RUN pip install -r requirements.txt

# install wkhtmltopdf
RUN apt-get update && apt-get install -y \
    wkhtmltopdf

# run
CMD ["python", "bot.py"]
