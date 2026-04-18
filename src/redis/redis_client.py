import os

from dotenv import load_dotenv
from redis import Redis
from redis.exceptions import ConnectionError, TimeoutError

load_dotenv()

redis_client = Redis(host=os.getenv('REDIS_HOST'),
              password=os.getenv('REDIS_PASSWORD'),
              port=int(os.getenv('REDIS_PORT')),
              decode_responses=True,
              retry_on_error=[ConnectionError, TimeoutError],
              retry_on_timeout=True,
              health_check_interval=int(os.getenv('REDIS_CHECK_INTERVAL_SECONDS'))
              )   

# Host: IP/DNS que o Redis usará para se conectar;
# No docker, será o nome que dermos para o container do redis no compose.yml
