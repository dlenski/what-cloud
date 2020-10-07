from .aws import AWSCloud
from .azure import AzureCloud
from .google import GoogleCloud
from .cloudflare import CloudFlare
from .fastly import Fastly

all_clouds = dict(
    AWS = AWSCloud,
    Azure = AzureCloud,
    Google = GoogleCloud,
    CloudFlare = CloudFlare,
    Fastly = Fastly,
)
