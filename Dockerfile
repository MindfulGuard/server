FROM node:18 AS nextjs

WORKDIR /home/runner/work/server/server

# Copy the entire project to the container
COPY . .

WORKDIR /home/runner/work/server/server/client

# Install the dependencies for Next.js
RUN yarn install

# Build the Next.js application
RUN yarn build

# Stage 3: Final Image
FROM python:3.10 AS python

WORKDIR /home/runner/work/server/server

# Install Python dependencies
RUN make pip-i

# Command to run both applications
CMD ["sh", "-c", "make run & python -m routines.__main__ & cd client && yarn start"]
