FROM python:3
ENV PYTHONUNBUFFERED=1
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000