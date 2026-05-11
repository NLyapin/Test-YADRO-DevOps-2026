FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
    && pip3 install --no-cache-dir requests \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY section1/script.py .

CMD ["python3", "script.py"]
