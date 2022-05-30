
FROM python:3

WORKDIR /usr/src/app

COPY ./requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY ./main.py main.py


EXPOSE 8000
CMD ["uvicorn","main:app","--host=0.0.0.0", "--port=8000"]