FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9

ENV PYTHONPATH "${PYTHONPATH}:/"
ENV PORT=8000

WORKDIR /src

RUN pip install --upgrade pip
COPY ./requirements.txt /src/
RUN pip install -r requirements.txt

COPY . /src

CMD ["uvicorn", "src.web:app", "--host", "0.0.0.0"]