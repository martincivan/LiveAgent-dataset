import os

from dotenv import load_dotenv
from liveagent_api import Configuration, ApiClient
from liveagent_api.rest import ApiException

load_dotenv()
configuration = Configuration()
configuration.host = os.getenv("HOST")
configuration.api_key['apikey'] = os.getenv("API_KEY")


class MyClient(ApiClient):
    def _ApiClient__deserialize_datatime(self, string):
        if not string:
            return None
        try:
            from dateutil.parser import parse
            return parse(string)
        except ImportError:
            return string
        except ValueError:
            raise ApiException(
                status=0,
                reason=(
                    "Failed to parse `{0}` as datetime object"
                    .format(string)
                )
            )

client = MyClient(configuration=configuration)