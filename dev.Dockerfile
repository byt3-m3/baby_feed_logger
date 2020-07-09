# ---- Dependencies ----
FROM python AS core

COPY requirements.txt /
# install app dependencies
RUN pip install -r /requirements.txt

WORKDIR /baby_log

COPY . /baby_log

RUN python3 setup.py sdist

# ---- Copy Files/Build ----
FROM core AS build

COPY --from=core /baby_log/dist /

RUN cd dist && ls | grep tar.gz | xargs pip3 install

ENTRYPOINT  ["python3", "-m","baby_log"]

CMD ["--run"]



