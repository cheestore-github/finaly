FROM m.docker-registry.ir/python:3.8-slim

ENV PYTHONUNBUFFERED 1

# Set working directory
RUN mkdir /force
WORKDIR /force
ADD . /force

# Installing requirements
ADD requirements.text /force
RUN pip install --upgrade pip
# RUN apk update && apk add python3-dev \
#                           gcc \
#                           libc-dev \
#                           libffi-dev
RUN pip install -r requirements.text

# Collect static files
RUN python manage.py collectstatic --no-input

CMD ["gunicorn", "--chdir", "force", "--bind", ":8000", "force.wsgi:application"]
#CMD python manage.py runserver 0.0.0.0:8000



