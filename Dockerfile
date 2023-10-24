FROM python:3.10

WORKDIR /home/runner/work/server/server

COPY . /home/runner/work/server/server

RUN make pip-i

CMD ["make run | python -m routines/__main__.py"]