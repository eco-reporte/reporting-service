FROM python:3.12

WORKDIR /app

COPY requirements.txt ./

RUN pip install --upgrade pip
RUN pip install --upgrade --force-reinstall setuptools
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "app.py"]
