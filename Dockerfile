FROM python:3.8

# Set environment variables
ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update
RUN apt-get install -y build-essential
RUN apt-get install -y python3-dev
RUN apt-get install -y swig
RUN apt-get install -y gettext
RUN apt-get install -y libgettextpo-dev
RUN apt-get install -y graphviz-dev
ENV DJANGO_SETTINGS_MODULE=digidex.settings

# Set work directory
RUN mkdir /src
WORKDIR /src

# Install dependencies:
COPY requirements.txt .
RUN pip install --upgrade pip
RUN python3 -m pip install wheel
RUN python3 -m pip install m2crypto
RUN python3 -m pip install -r requirements.txt

# Run the application:
COPY . /src/
