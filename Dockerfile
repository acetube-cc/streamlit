# syntax=docker/dockerfile:1.4
FROM public.ecr.aws/docker/library/python:3.12.2-slim
WORKDIR /app
ENV PATH="/root/.local/bin:${PATH}"
RUN pip install pipx \
    && pipx install poetry
COPY acetube_streamlit ./acetube_streamlit
COPY pyproject.toml .
COPY poetry.lock .
COPY README.md .
RUN poetry install
EXPOSE 80
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
