FROM python:3.8

WORKDIR /app

COPY ["file_compare.py", "flask_file_compare.py", "requirements.txt", "/app/"]

RUN pip3 install -r ./requirements.txt

RUN mkdir -p /app/input

RUN mkdir -p /app/output

RUN mkdir -p /app/output/logs

RUN mkdir -p /app/number_of_lines

#RUN touch /app/number_of_lines/number_of_lines.txt

EXPOSE 5000

ENTRYPOINT ["python3"]

CMD ["flask_file_compare.py"]
