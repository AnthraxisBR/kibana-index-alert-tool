FROM ubuntu

COPY requirements.txt /app/requirements.txt

WORKDIR /app

RUN apt update && apt install -y cron curl unzip python3 python3-pip

RUN pip install -r requirements.txt

EXPOSE 5000

RUN cd /tmp \
    && curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip" \
    && unzip awscliv2.zip \
    && ./aws/install

ENV FLASK_APP=main.py
ENV FLASK_RUN_HOST=0.0.0.0

CMD ["flask", "run", "--host=0.0.0.0"]