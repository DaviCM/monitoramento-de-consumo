import os

from dotenv import load_dotenv
from redis import Redis
from redis.exceptions import ConnectionError

load_dotenv()

redis_client = Redis(host=os.getenv('REDIS_HOST'),
              password=os.getenv('REDIS_PASSWORD'),
              port=os.getenv('REDIS_PORT'),
              decode_responses=True,
              retry_on_error=[ConnectionError],
              retry_on_timeout=True,
              )   

# Host: IP/DNS que o Redis usará para se conectar;
# No docker, será o nome que dermos para o container do redis no compose.yml
