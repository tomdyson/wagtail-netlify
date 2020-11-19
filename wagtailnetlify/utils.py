from dateutil.parser import parse
import requests
from django.conf import settings


API_ROOT = "https://api.netlify.com/api/v1/"
HEADERS = {
    "Authorization": str("Bearer " + settings.NETLIFY_API_TOKEN),
    "Content-type": "application/json",
}


def get_site_name():
    site_details_url = API_ROOT + "sites/" + settings.NETLIFY_SITE_ID
    resp = requests.get(site_details_url, headers=HEADERS)
    return resp.json()["name"]


def netlify_deploys():
    site_name = get_site_name()
    deploys_listing_url = (
        API_ROOT + "sites/" + settings.NETLIFY_SITE_ID + "/deploys?per_page=10"
    )
    deploys = requests.get(deploys_listing_url, headers=HEADERS).json()

    for deploy in deploys:
        deploy["admin_url"] = (
            "https://app.netlify.com/sites/" + site_name + "/deploys/" + deploy["id"]
        )
        deploy["created_at_parsed"] = parse(deploy["created_at"])

    return deploys
