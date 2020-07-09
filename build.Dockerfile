# ---- Dependencies ----
FROM python:3.7-slim AS core

RUN apt-get update
RUN apt-get install -y --no-install-recommends build-essential gcc

RUN python -m venv /opt/venv

# Make sure we use the virtualenv:
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt /
RUN pip install -r /requirements.txt

WORKDIR /baby_log

COPY . /baby_log

RUN python3 setup.py sdist

# ---- Copy Files/Build ----
FROM python:3.7-slim AS build

COPY --from=core /baby_log /
COPY --from=core /opt/venv /opt/venv

# Make sure we use the virtualenv:
ENV PATH="/opt/venv/bin:$PATH"

RUN cd dist && ls | grep tar.gz | xargs pip3 install

ENTRYPOINT  ["python3", "-m","baby_log"]

CMD ["--run"]



