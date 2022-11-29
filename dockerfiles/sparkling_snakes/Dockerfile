FROM python:3.9

RUN apt update
RUN apt install -y openjdk-11-jdk-headless

COPY . /sparkling_snakes
WORKDIR /sparkling_snakes

RUN make install_env
RUN make build
RUN make install

EXPOSE 8000

CMD ["make", "run"]