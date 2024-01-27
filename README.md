# Chat WOW

Uma aplicação Django que usa o [Django Channels](https://channels.readthedocs.io/en/latest/) para criar um chat em tempo real.

## Como rodar o projeto

Além de executar o projeto Django você também vai precisar subir uma instância do [Redis](https://redis.io/). Podemos fazer isso usando o [Docker](https://www.docker.com/).

```bash
docker run --rm -d -p 6379:6379 redis:7
```

