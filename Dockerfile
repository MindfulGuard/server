# Stage 1: Build Python
FROM python:3.10 AS python

WORKDIR /home/runner/work/server/server

# Copy the entire project to the container
COPY . .

# Install Python dependencies
RUN make pip-i

# Stage 2: Build Next.js
FROM node:18 AS nextjs

WORKDIR /home/runner/work/server/server/client

# Copy only the necessary files for Next.js
COPY --from=python /home/runner/work/server/server .

# Install the dependencies for Next.js
RUN cd client && yarn install

# Build the Next.js application
RUN cd client && yarn build

# Command to run both applications
CMD ["sh", "-c", "cd /home/runner/work/server/server && make run & python -m routines.__main__ & cd /home/runner/work/server/server/client && yarn start"]