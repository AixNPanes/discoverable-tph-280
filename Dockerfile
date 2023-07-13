FROM python:3.11

ARG application_version
LABEL maintainer="Tim Daley <timdaley@earthling.net>"
LABEL description="discoverable-tph-280 utility image"
LABEL version=${application_version}

RUN apt-get update && \
    apt-get install --no-install-recommends -y apt-utils ca-certificates && \
		update-ca-certificates && \
		rm -fr /tmp/* /var/lib/apt/lists/*

# Copy wheel file built by Poetry
COPY dist/*.whl /app/

RUN python -m pip install --upgrade pip --no-cache-dir && \
    pip install --no-cache-dir /app/*.whl && \
    pip cache purge && \
    rm -rf /app/*.whl

USER nobody

CMD ["bash", "-l"]
