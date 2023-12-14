# Stage 1: Build Next.js application
FROM node:18 AS nextjs

WORKDIR /home/runner/work/server

# Copy the entire project to the container
COPY server/client server/client

# Install the dependencies for Next.js
RUN cd server/client && yarn install

# Build the Next.js application
RUN cd server/client && yarn build

# Stage 2: Final Image
FROM python:3.10 AS python

WORKDIR /home/runner/work/server

# Copy built Next.js application from the previous stage
COPY --from=nextjs /home/runner/work/server/client server/client

# Install Python dependencies
RUN make pip-i

# Command to run both applications
CMD ["sh", "-c", "make run & python -m routines.__main__ & cd client && yarn start"]
