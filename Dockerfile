FROM node:18 AS nextjs

WORKDIR /home/runner/work/server/server

COPY . /home/runner/work/server/server

RUN cd client && yarn install

# Build the Next.js application
RUN cd client && yarn build

FROM python:3.10 AS python

WORKDIR /home/runner/work/server/server

COPY --from=nextjs /home/runner/work/server/server /home/runner/work/server/server

RUN curl -sL https://deb.nodesource.com/setup_18.x | bash - \
    && apt-get install -y nodejs \
    && npm install -g yarn

RUN make pip-i

CMD ["sh", "-c", "make run & python -m routines.__main__ & cd client && yarn build && yarn start"]