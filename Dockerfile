FROM python:3.10 AS python

WORKDIR /home/runner/work/server/server

COPY . /home/runner/work/server/server

RUN make pip-i

# Install Nginx
RUN apt-get update && apt-get install -y nginx

# Copy Nginx configuration file
RUN mv proxy/nginx.conf /etc/nginx/nginx.conf

CMD ["sh", "-c", "service nginx restart && make run & python -m routines.__main__"]