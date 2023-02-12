FROM python:3.8-slim-buster
ADD ./requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install -r requirements.txt
COPY . .
CMD ["python3", "-m" , "flask", "run", "--host", "0.0.0.0", "--port", "6000"]