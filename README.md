# Uso

Primero dar los permisos a los directorios para poder ser copiados por docker:

```shell
sudo chmod -R 777 addons
sudo chmod -R 777 etc
```

Iniciar el contenedor con el siguiente comando:

```shell
docker-compose up
```

-   Esto iniciará la app en `localhost:8069` en donde tendra acceso a Odoo 13.0. Si se desea que el servidor escuche otro puerto, solo hay que cambiar el primer **8069** por otro valor en el archivo **docker-compose.yml**:

```yml
ports:
    - 8069:8069
```

En caso de hacer cambios en los directorios **etc** o **addons**, debe ejecutar:

```shell
docker-compose up --build -V main
```
