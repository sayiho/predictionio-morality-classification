# Single attribute

*PredictionIO Morality Classification*

## Collecting Data

Use PredicitonIO's API to import data to Event Server.

### Using REST API

```shell
# import a totally new inspect
$ curl -i -X POST http://localhost:7070/events.json?accessKey=$ACCESS_KEY \
-H "Content-Type: application/json" \
-d '{
  "event" : "$set",
  "entityType" : "user"
  "entityId" : "u0",
  "properties" : {
    "attr" : 0,
    "plan" : 1
  }
  "eventTime" : "2014-11-02T09:39:45.618-08:00"
}'

# You may also set the properties one by one, or update data of an existing inspect
$ curl -i -X POST http://localhost:7070/events.json?accessKey=$ACCESS_KEY \
-H "Content-Type: application/json" \
-d '{
  "event" : "$set",
  "entityType" : "user"
  "entityId" : "u1",
  "properties" : {
    "attr" : 0
  }
  "eventTime" : "2014-11-02T09:39:45.618-08:00"
}'

$ curl -i -X POST http://localhost:7070/events.json?accessKey=$ACCESS_KEY \
-H "Content-Type: application/json" \
-d '{
  "event" : "$set",
  "entityType" : "user"
  "entityId" : "u1",
  "properties" : {
    "plan" : 1
  }
  "eventTime" : "2014-11-02T09:39:45.618-08:00"
}'
```

### Using Python API

```python
import predictionio

client = predictionio.EventClient(
    access_key=<ACCESS KEY>,
    url=<URL OF EVENTSERVER>,
    threads=5,
    qsize=500
)

# import a totally new inspect
client.create_event(
    event="$set",
    entity_type="user",
    entity_id=<USER ID>,
    properties= {
      "attr" : int(<VALUE OF ATTR0>),
      "plan" : int(<VALUE OF PLAN>)
    }
)

# You may also set the properties one by one, or update data of an existing inspect
client.create_event(
    event="$set",
    entity_type="user",
    entity_id=<USER ID>,
    properties= {
      "attr" : int(<VALUE OF ATTR0>)
    }
)
client.create_event(
    event="$set",
    entity_type="user",
    entity_id=<USER ID>,
    properties= {
      "plan" : int(<VALUE OF PLAN>)
    }
)
```

## Query

Use PredicitonIO's API to retrieve predicted results.

### Using REST API

```shell
$ curl -H "Content-Type: application/json" \
-d '{ "attr":2}' http://localhost:8000/queries.json
```

### Using Python API

```python
import predictionio
engine_client = predictionio.EngineClient(url="http://localhost:8000")
print engine_client.send_query({"attr":2)
```

### Sample JSON Response

The following is sample JSON response:

```shell
{"label":0.0}
```
