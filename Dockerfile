FROM python:3.8-slim-buster

# Add sources to `/code` and work there
COPY . /code
WORKDIR /code

# Install cap-client
RUN pip3 install --no-cache-dir -e '.[all]'
