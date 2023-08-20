FROM python:3.11.4

RUN groupadd -r cv_user && useradd -r -m -g cv_user cv_user \
  && mkdir -p /home/cv_user/project/ && chown -R cv_user:cv_user /home/cv_user/project/

WORKDIR /home/cv_user/project/

RUN apt-get update
RUN apt-get install -y --no-install-recommends python3-dev libpq-dev mc tmux
RUN rm -rf /var/lib/apt/lists/*
RUN apt-get purge -y

ENV LANG='en_US.UTF-8' LANGUAGE='en_US:en' LC_ALL='en_US.UTF-8'

ENV PIP_NO_CACHE_DIR=1
ENV PIP_DISABLE_PIP_VERSION_CHECK=1
ENV PYTHONPATH /home/cv_user/project/

ENV POETRY_VERSION=1.5.1
ENV POETRY_HOME=/opt/poetry
ENV POETRY_VENV=/opt/poetry-venv
ENV POETRY_CACHE_DIR=/opt/.cache

RUN pip3 install poetry
RUN poetry config virtualenvs.create false

ENV PATH="${PATH}:${POETRY_VENV}/bin"

# PyTorch is completely broken in Poetry, better use pip for builds
# https://github.com/python-poetry/poetry/issues/6409
RUN pip3 install --pre torch torchvision torchaudio --index-url https://download.pytorch.org/whl/nightly/cu121

COPY poetry.lock pyproject.toml ./
RUN poetry install --no-interaction --no-cache --without dev

COPY . /home/cv_user/project/

USER cv_user

EXPOSE 8189
CMD ["gunicorn", "app:app", "--workers", "2", "--threads", "1", "--timeout", "180", "--graceful-timeout", "60", "--keep-alive", "60", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8189"]
