FROM python:3.8

WORKDIR /app

COPY . /app

RUN pip install flask

EXPOSE 8080

ENTRYPOINT ["python3"]

CMD ["flask_file_compare.py"]
