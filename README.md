## Сборка 
```
docker build -t marina-gpt .
```
---

## Запуск
```
docker run -d \
  --name marina-gpt \
  --env-file .env \
  --restart unless-stopped \
  marina-bot
```
