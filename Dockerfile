FROM python:3.10 AS python

WORKDIR /home/runner/work/server/server

COPY . /home/runner/work/server/server

RUN make pip-i
RUN make generate-locales

# Install Nginx
RUN apt-get update && apt-get install -y nginx

# Copy Nginx configuration file
RUN mv proxy/nginx.conf /etc/nginx/nginx.conf

# Install Node.js and Yarn
RUN curl -sL https://deb.nodesource.com/setup_18.x | bash - \
    && apt-get install -y nodejs \
    && npm install -g yarn

RUN cd client && yarn install && yarn build

CMD ["sh", "-c", "service nginx restart && make run & python -m routines.__main__ & cd client && yarn build && yarn start"]