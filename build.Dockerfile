# ------ Build Core & requirements ------
FROM ubuntu AS build

WORKDIR /build

RUN apt-get update && apt-get install -y python3-pip

COPY requirements.txt ./

RUN pip3 install -r requirements.txt

# ------ Build Release ------
FROM build AS release

WORKDIR /build

COPY dist/ ./

RUN ls | grep tar.gz | xargs pip3 install

ENTRYPOINT  ["python3", "-m","baby_log"]

CMD ["--run"]
