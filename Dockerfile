FROM odoo:13 As odoobase

USER root

RUN apt-get update && apt-get install libxml2

RUN pip3 install python-stdnum xmltodict

USER odoo
