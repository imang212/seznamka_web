FROM python:alpine
WORKDIR /code
RUN pip install --upgrade pip
COPY requirements.txt /code
RUN pip install -r requirements.txt --no-cache-dir
COPY ./code /code
CMD python app.py
