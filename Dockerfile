FROM python:3.8

RUN pip install --upgrade pip

WORKDIR /app

COPY requirements.txt  requirements.txt

RUN pip3 install -r requirements.txt

COPY . .

CMD ["python3", "./main.py"]

# Path: DockerFile
