FROM python:3.8

WORKDIR /app

COPY ["file_compare.py", "flask_file_compare.py", "requirements.txt","/app/"]

RUN pip3 install -r ./requirements.txt

EXPOSE 5000

ENTRYPOINT ["python3"]

CMD ["flask_file_compare.py"]
