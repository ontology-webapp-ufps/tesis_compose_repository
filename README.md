# tesis_compose_repository

Este repositorio es desarrollado como parte del trabajo de grado para optar por el titulo de ingeniero de sistemas de los estudiantes de ingeniería de sistemas de la universidad francisco de paula santander:

- Juan Camilo Hernández Parra, correo: juancamilohp@ufps.edu.co
- Jose Manolo Pinzon Hernández, correo josemanoloph@ufps.edu.co

## DESPLIEGUE DE PROYECTO NUBE UFPS
Teniendo en cuenta la nube con la que se cuenta en la universidad francisco de paula santandar, se tienen los siguientes pasos para un despliegue exitoso, usando docker y docker-compose

### PUERTO
Es necesario definir el puerto sobre el cual se tienen disponibilidad, teniendo en cuenta el uso de traefik el cual tiene multiples funciones para las aplicaciones en contendores, entre ellos se destaca el proxy reverso y el api gateway.

> Definir el puerto sobre el cual se tenga disponibilidad y ajustarlo en el puerto del servicio traefik

### Correr el proyecto docker-compose
Ejecutar el siguiente comando para levantar la orquestación de los contenedores usando el docker-compose.
> docker-compose up -d

## Trabajos futuros
- traefik permite activar observalidad sobre la solución usando software como prometheus o grafana.