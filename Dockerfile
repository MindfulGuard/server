FROM python:3.10 AS python

WORKDIR /home/runner/work/server/server

COPY . /home/runner/work/server/server

RUN make pip-i

# Install Nginx
RUN apt-get update && apt-get install -y nginx

# Install migrate
RUN curl -sSL https://github.com/golang-migrate/migrate/releases/download/v4.17.0/migrate.linux-amd64.deb \
--create-dirs -o /home/$USER/migrate.linux-amd64.deb && dpkg -i /home/$USER/migrate.linux-amd64.deb && rm /home/$USER/migrate.linux-amd64.deb

# Copy Nginx configuration file
RUN mv proxy/nginx.conf /etc/nginx/nginx.conf

RUN chmod +x proxy/install_opessl.sh && ./proxy/install_opessl.sh
RUN chmod +x proxy/gen_certs.sh && chmod +x db/migration.sh

CMD ["sh", "-c", "./proxy/gen_certs.sh && service nginx restart && make migration-up && (make run & python -m routines.__main__)"]