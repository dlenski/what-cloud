from .aws import AWSCloud
from .azure import AzureCloud
from .google import GoogleCloud
from .oracle import OracleCloud
from .cloudflare import CloudFlare
from .fastly import Fastly

all_clouds = dict(
    AWS = AWSCloud,
    Azure = AzureCloud,
    Google = GoogleCloud,
    Oracle = OracleCloud,
    CloudFlare = CloudFlare,
    Fastly = Fastly,
)
