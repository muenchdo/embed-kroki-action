FROM python:3

COPY convert.py ./script.py

CMD ["python", "/script.py"]
