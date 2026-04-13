FROM python
COPY . /code

WORKDIR /code

# Update aptitude with new repo
RUN apt-get update

# Install software
RUN apt-get install -y git curl

RUN pip install .[all]
