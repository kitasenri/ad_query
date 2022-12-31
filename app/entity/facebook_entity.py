from dataclasses import *

class GetAttr:
    def __getitem__(cls, x):
        return getattr(cls, x)

FACEBOOK_ENTITY_KEYS = [
    ## Common
    "type",
    "id",
    "customer_id",
    "business_plan",
    "name",
    ## Custom　Info
    "adset_id",
    "adset_name",
    "ad_id",
    "ad_name",
    ## Custom
    "impressions",
    "clicks",
    "ctr",
    "cpc",
    "conversions",
    "cost_per_conversion",
    "spend",
    "reach",
    "action_values",
    "inline_link_click_ctr",
    "inline_link_clicks",
    ## Info
    "report_date",
    "create_on",
    "create_user"
]

@dataclass
class FacebookEntity(GetAttr):
    ## Common
    type: str
    id: str
    customer_id: str
    business_plan: str
    name: str
    ## Custom Info
    adset_id: str
    adset_name: str
    ad_id: str
    ad_name: str
    ## Custom
    impressions: int
    clicks: int
    ctr: float
    cpc: float
    conversions: str
    cost_per_conversion: str
    spend: int
    reach: int
    action_values: str
    inline_link_click_ctr: float
    inline_link_clicks: str
    ## Info
    report_date: str
    create_on: str
    create_user: str