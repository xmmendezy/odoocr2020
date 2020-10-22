FROM odoo:13 As odoobase

WORKDIR /etc/odoo

COPY ./etc/odoo.conf  odoo.conf

WORKDIR /mnt

COPY addons addons
