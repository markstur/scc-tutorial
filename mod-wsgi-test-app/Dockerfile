from alpine:latest
RUN apk add --no-cache py3-pip \
    && pip3 install --upgrade pip

ENV PORT 8080
EXPOSE 8080

WORKDIR /app
COPY . /app

RUN pip3 --no-cache-dir install -r requirements.txt

ENTRYPOINT ["python3"]
CMD ["app.py"]

