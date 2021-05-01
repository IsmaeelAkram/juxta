FROM python:3

WORKDIR /usr/src/app

RUN apt-get update
RUN apt-get install libopus-dev -y

ENV OPUS_PATH=/usr/lib/x86_64-linux-gnu/libopus.so

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "run.py" ]