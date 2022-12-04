FROM python:3.10

RUN apt update
RUN apt install -y openjdk-11-jdk-headless libimage-exiftool-perl pev

ENV PGPASSWORD=postgres

COPY . /sparkling_snakes
WORKDIR /sparkling_snakes

RUN mkdir -p /s3-files

RUN make install_env
RUN make build
RUN make install

EXPOSE 8000

CMD ["make", "run"]