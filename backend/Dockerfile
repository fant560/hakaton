FROM python:3.9
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY ./requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/
COPY ./entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
RUN mkdir -p /root/ml/documents
ENTRYPOINT ["sh", "/entrypoint.sh"]
