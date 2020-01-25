FROM python:3.6-alpine AS base

ENV PYROOT /pyroot
ENV PYTHONUSERBASE $PYROOT

# Build Container
FROM base AS builder
ARG BUILD_DEPS="gcc python3-dev musl-dev postgresql-dev jpeg-dev zlib-dev"
RUN apk --no-cache add ${BUILD_DEPS}
RUN pip install pipenv
COPY Pipfile* ./
RUN PIP_USER=1 PIP_IGNORE_INSTALLED=1 pipenv install --system --deploy \
    && find /usr/local \
        \( -type d -a -name test -o -name tests \) \
        -o \( -type f -a -name '*.pyc' -o -name '*.pyo' \) \
        -exec rm -rf '{}' \+

# Runtime Container
FROM base
ARG RUNTIME_DEPS="libcrypto1.1 libssl1.1 libpq libjpeg"
RUN apk --no-cache add ${RUNTIME_DEPS}
COPY --from=builder $PYROOT/lib/ $PYROOT/lib/
RUN pip install gunicorn

WORKDIR /app
COPY src /app

CMD gunicorn -b :$PORT gymkhana.wsgi
