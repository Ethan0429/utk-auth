FROM python:3.10-buster



# install wkhtmltopdf
RUN apt-get update && apt-get install -y \
    wkhtmltopdf

# pip install -r requirements.txt
WORKDIR /app
COPY . .

# install requirements
RUN pip install -r requirements.txt

# run
CMD ["python", "bot.py"]
