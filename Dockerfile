FROM python:3.10-buster


# install requirements
RUN pip install -r requirements.txt

# install wkhtmltopdf
RUN apt-get update && apt-get install -y \
    wkhtmltopdf

# pip install -r requirements.txt
WORKDIR /app
COPY . .

# run
CMD ["python", "bot.py"]
