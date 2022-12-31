from dataclasses import *

class GetAttr:
    def __getitem__(cls, x):
        return getattr(cls, x)

GOOGLEAD_ENTITY_KEYS = [
    ## Common
    "type",
    "id",
    "customer_id",
    "business_plan",
    "name",
    ## Custom
    "impressions",
    "clicks",
    "ctr",
    "average_cpc",
    "conversions",
    "cost_per_conversion",
    "cost_micros",
    "search_impression_share",
    "search_top_impression_share",
    "absolute_top_impression_percentage",
    "search_rank_lost_impression_share",
    "search_rank_lost_top_impression_share",
    "search_rank_lost_absolute_top_impression_share",
    "search_budget_lost_impression_share",
    "search_budget_lost_top_impression_share",
    "search_budget_lost_absolute_top_impression_share",
    "search_exact_match_impression_share",
    "search_click_share",
    ## Info
    "report_date",
    "create_on",
    "create_user"
]

@dataclass
class GoogleAdEntity(GetAttr):
    ## Common
    type: str
    id: str
    customer_id: str
    business_plan: str
    name: str
    ## Custom
    impressions: int
    clicks: int
    ctr: float
    average_cpc: float
    conversions: float
    cost_per_conversion: float
    cost_micros: int
    search_impression_share: float
    search_top_impression_share: float
    absolute_top_impression_percentage: float
    search_rank_lost_impression_share: float
    search_rank_lost_top_impression_share: float
    search_rank_lost_absolute_top_impression_share: float
    search_budget_lost_impression_share: float
    search_budget_lost_top_impression_share: float
    search_budget_lost_absolute_top_impression_share: float
    search_exact_match_impression_share: float
    search_click_share: float
    ## Info
    report_date: str
    create_on: str
    create_user: str