FROM python:3.8-slim AS patch-image

RUN apt-get update && apt-get upgrade -y

# --------------------------------------------------------------------

FROM patch-image AS compile-image

ENV PATH="/opt/venv/bin:${PATH}"
WORKDIR "/tmp"

COPY requirements.txt .

RUN apt-get install -y --no-install-recommends build-essential gcc libpq-dev
RUN python -m venv /opt/venv
RUN python -m pip install --upgrade pip
RUN python -m pip install -r requirements.txt

# --------------------------------------------------------------------

FROM patch-image

LABEL maintainer="Nicholas Elia <me@nichelia.com>"

ENV USER="nobody"
ENV PATH="/opt/venv/bin:$PATH"
WORKDIR "/tmp"

RUN apt-get install -y --no-install-recommends libpq-dev
COPY --from=compile-image /opt/venv /opt/venv

USER ${USER}

ENTRYPOINT [ "python" ]
