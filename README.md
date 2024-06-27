# UGC Research

### В рамках данного проекта было выполнено 3 задачи:
- Описана структура проекта в формате UML в состоянии до начала спринта (AS_IS) и по его завершению (TO_BE)
- Написан API получения событий клиента и записи их в Kafka
- Реализован ETL загрузки сообщений из Kafka в ClickHouse

#### Запуск проекта
Для запуска проекта необходимо выполнить docker-compose.yml, предварительно создав и заполнив .env.

```
docker-compose up -d --build
```

#### Api
Отправка данных в Kafka реализована на FastApi.
Ручка /api/v1/view_progress/save принимает в body параметры о просмотре фильма и сохраняет их в кафку.

#### ETL
При старте проекта `docker-compose up --build` создастся бд в clickhouse и подключится прием данных из kafka.

#### Kafka
Топик **mviews** должен создаться автоматически. 

### В рамках второй части проекта было выполнены следующие задачи:
- Проведено исследование по выбору хранилища для UGC материалов
- Реализовано CI/CD
- Выполнен ELK

#### Архитектура
При проработке архитектуры было принято решение добавить функциональность в уже существующий проект с прошлого модуля для ускорения процесса разработки, т.к. это учебный проект. В реальной разработке корректней было бы реализовать отдельные сервисы под разные задачи.

#### MongoDB
В качестве хранилища было выбрано MongoDB, так как она полностью соответствует установленным требованиям (чтение до 200 ms), а также было интересно поэксперементировать с новой БД (в прошлом спринте работа проводилась с Clickhouse). Детальное исследование доступно в соответствующем [README](https://github.com/mod-web/ugc_sprint_1/blob/main/mongo/README.md).

#### CI/CD
- добавлен mypy, исправлены его ошибки
- добавлена проверка билда на трех версиях питона
- уведомление об успешной сборке в телеграм

#### ELK
- filebeat отправляет данные в logstash
- logstash перенаправляет данные в формате json в elasticsearch
- elasticsearch хранит логи в индексах по датам
- в kibana (http://127.0.0.1:5601) можно смотреть и анализировать логи
- сообщения об ошибках собираем в sentry
