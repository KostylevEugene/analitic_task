FROM python

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .

RUN python models.py

RUN python parser.py

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]