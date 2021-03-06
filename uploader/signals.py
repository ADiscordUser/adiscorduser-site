from django import dispatch
from django.conf import settings

import requests
import threading

clear_cf_cache = dispatch.Signal()

# if you are using uwsgi, you must set `wsgi-env-behaviour = holy`
# in the config to prevent any threading issues
class ClearCacheThread(threading.Thread):
    def __init__(self, request, instance, **kwargs):
        self.request = request
        self.instance = instance
        super().__init__(**kwargs)

    def run(self):
        headers = {
            "Authorization": f"Bearer {settings.CLOUDFLARE['API_KEY']}"
        }
        payload = {
            "files": [
                self.instance.media.url
            ]
        }
        requests.post(
            f"https://api.cloudflare.com/client/v4/zones/{settings.CLOUDFLARE['ZONE_IDENTIFIER']}/purge_cache",
            json=payload,
            headers=headers
        )

@dispatch.receiver(clear_cf_cache)
def clear_media_cache(sender, request, instance, **kwargs):
    if hasattr(settings, "CLOUDFLARE"):
        if request.get_host() in settings.CLOUDFLARE["PROD_HOST"]:
            ClearCacheThread(request, instance).start()