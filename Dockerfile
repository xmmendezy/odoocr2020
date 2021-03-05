FROM odoo:14 As odoobase

USER root

RUN apt-get install -y openssl

COPY requirements.txt .

RUN pip3 install --upgrade pip

RUN pip3 install --no-warn-script-location -r requirements.txt
