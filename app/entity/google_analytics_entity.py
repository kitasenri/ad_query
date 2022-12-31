from dataclasses import *

class GetAttr:
    def __getitem__(cls, x):
        return getattr(cls, x)

GOOGLE_ANALYTICS_ENTITY_KEYS = [
    ##
    "type",
    "id",
    "customer_id",
    "business_plan",
    ##
    "users",
    "sessions",
    "pageviews",
    "sessionDuration",
    ## 
    "report_date",
    "create_on",
    "create_user"
]

@dataclass
class GoogleAnalyticsEntity(GetAttr):
    ##
    type: str
    id: str
    customer_id: str
    business_plan: str
    ##
    users: int
    sessions: int
    pageviews: int
    sessionDuration: float
    ## 
    report_date: str
    create_on: str
    create_user: str