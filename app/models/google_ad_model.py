
import logging

import google.ads.google_ads.client
from google.ads.google_ads.client import *

from consts.common_consts import *
from utils.common_utils import *
from entity.google_ad_entity import *

class GoogleAdReportClient():

    _DEFAULT_PAGE_SIZE = 1000

    def __init__(self):
        self.client = (google.ads.google_ads.client.GoogleAdsClient.load_from_env())
        self.page_size = GoogleAdReportClient._DEFAULT_PAGE_SIZE

    def get_performance_report(self, account):

        business_plan = account["name"]
        customer_id = account["account_id"]

        ga_service = self.client.get_service('GoogleAdsService', version='v2')
        query = (
            '''
            SELECT 
                campaign.id,
                campaign.name,
                metrics.impressions,
                metrics.clicks,
                metrics.ctr,
                metrics.average_cpc,
                metrics.conversions,
                metrics.cost_per_conversion,
                metrics.cost_micros,
                metrics.search_impression_share,
                metrics.search_top_impression_share,
                metrics.absolute_top_impression_percentage,
                metrics.search_rank_lost_impression_share,
                metrics.search_rank_lost_top_impression_share,
                metrics.search_rank_lost_absolute_top_impression_share,
                metrics.search_budget_lost_impression_share,
                metrics.search_budget_lost_top_impression_share,
                metrics.search_budget_lost_absolute_top_impression_share,
                metrics.search_exact_match_impression_share,
                metrics.search_click_share
            FROM
                campaign
            WHERE
                segments.date DURING YESTERDAY
            '''
        )

        result = ga_service.search(
            customer_id, 
            query = query, 
            page_size = self.page_size
        )

        items = []
        for rr in result:
            item = GoogleAdEntity(
                ## Common
                type = TypeConsts.TYPE_GOOGLE_AD,
                id = rr.campaign.id.value,
                customer_id = customer_id,
                business_plan = business_plan,
                name = rr.campaign.name.value,
                ## Custom
                impressions = rr.metrics.impressions.value,
                clicks = rr.metrics.clicks.value,
                ctr = rr.metrics.ctr.value,
                average_cpc = get_float( rr.metrics.average_cpc.value ),
                conversions = get_int(rr.metrics.conversions.value),
                cost_per_conversion = rr.metrics.cost_per_conversion.value,
                cost_micros = get_int(rr.metrics.cost_micros.value / 1000000),
                search_impression_share = rr.metrics.search_impression_share.value,
                search_top_impression_share = rr.metrics.search_top_impression_share.value,
                absolute_top_impression_percentage = rr.metrics.absolute_top_impression_percentage.value,
                search_rank_lost_impression_share = rr.metrics.search_rank_lost_impression_share.value,
                search_rank_lost_top_impression_share = rr.metrics.search_rank_lost_top_impression_share.value,
                search_rank_lost_absolute_top_impression_share = rr.metrics.search_rank_lost_absolute_top_impression_share.value,
                search_budget_lost_impression_share = rr.metrics.search_budget_lost_impression_share.value,
                search_budget_lost_top_impression_share = rr.metrics.search_budget_lost_top_impression_share.value,
                search_budget_lost_absolute_top_impression_share = rr.metrics.search_budget_lost_absolute_top_impression_share.value,
                search_exact_match_impression_share = rr.metrics.search_exact_match_impression_share.value,
                search_click_share = rr.metrics.search_click_share.value,
                ## Info
                report_date = create_yesterday_date(),
                create_on = create_today(),
                create_user = CREATE_USER,
            )
            items.append(item)

        return items