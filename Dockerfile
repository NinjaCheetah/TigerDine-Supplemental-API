FROM python:3.14-slim-trixie

RUN ln -sf /usr/share/zoneinfo/America/New_York /etc/localtime

WORKDIR /srv/tigerdine-api

RUN apt update && apt install -y curl

RUN pip install --upgrade pip

COPY requirements.txt /srv/tigerdine-api

RUN pip install -r requirements.txt

COPY . /srv/tigerdine-api

ENTRYPOINT ["uvicorn", "api:app", "--host=0.0.0.0", "--port=80"]

HEALTHCHECK --interval=30s --timeout=5s --retries=3 CMD curl -f http://localhost/api/health || exit 1