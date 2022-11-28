FROM python:3.11-alpine
RUN apk update
RUN apk add make

COPY . /sparkling_snakes
WORKDIR /sparkling_snakes

RUN pip install -r requirements-venv.txt

RUN make build
RUN make install

EXPOSE 8000

CMD ["make", "run"]