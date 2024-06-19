FROM python:3.10 AS python

WORKDIR /mindfulguard/server

COPY . /mindfulguard/server

RUN apt-get update && apt-get upgrade -y

# Install Nginx
RUN apt-get install -y nginx

# Install migrate
RUN curl -sSL https://github.com/golang-migrate/migrate/releases/download/v4.17.0/migrate.linux-amd64.deb -o /tmp/migrate.linux-amd64.deb \
    && dpkg -i /tmp/migrate.linux-amd64.deb \
    && rm /tmp/migrate.linux-amd64.deb

# Copy Nginx configuration file
RUN mv proxy/nginx.conf /etc/nginx/nginx.conf

RUN chmod +x proxy/gen_certs.sh && chmod +x db/migration.sh

# Install Go
RUN curl -sSL https://go.dev/dl/go1.21.4.linux-amd64.tar.gz -o /tmp/go.tar.gz \
    && tar -xzvf /tmp/go.tar.gz -C /usr/local \
    && rm -f /tmp/go.tar.gz

# Update PATH for Go
ENV PATH="/usr/local/go/bin:${PATH}"

# Verify Go installation
RUN go version

RUN make bootstrap

RUN cd services/dynamic_configurations && \
    make build && \
    cd ../.. && \
    mv services/dynamic_configurations/build/dynamic_configurations dynamic_configurations && \
    rm -rf /services/

CMD ["sh", "-c", "./proxy/gen_certs.sh && service nginx restart && make migration-up && (make run & python -m routines.__main__ & ./dynamic_configurations)"]
