import os
import logging


from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.adobjects.campaign import Campaign
from facebook_business.adobjects.adset import AdSet
from facebook_business.adobjects.ad import Ad

from consts.common_consts import *
from utils.common_utils import *
from entity.facebook_entity import *

class FaceBookReportClient():

    '''
    https://developers.facebook.com/docs/marketing-api/reference/sdks/python/campaign/v6.0
    https://github.com/facebook/facebook-python-business-sdk/blob/master/facebook_business/adobjects/campaign.py
    https://github.com/facebook/facebook-python-business-sdk/blob/master/facebook_business/adobjects/adset.py
    https://github.com/facebook/facebook-python-business-sdk/blob/master/facebook_business/adobjects/ad.py
    '''

    PARAM_CAMPAIGN_INSIGHTS = {
        'date_preset': 'yesterday',
        'fields': [
            'campaign_name', 
        ]
    }

    PARAM_SETS_INSIGHTS = {
        'date_preset': 'yesterday',
        'fields': [
            "adset_id",
            "adset_name",
        ]
    }

    PARAM_AD_INSIGHTS = {
        'date_preset': 'yesterday',
        'fields': [
            "ad_id",
            "ad_name",
            "impressions",
            "clicks",
            "ctr",
            "cpc",
            ##
            "conversions",
            ##
            "cost_per_conversion",
            "spend",
            "reach",
            ##
            "action_values",
            "inline_link_click_ctr",
            "inline_link_clicks",
        ]
    }


    def __init__(self, access_info):
        self.client = FacebookAdsApi.init(
            os.environ.get('FACEBOOK_APP_ID'),
            os.environ.get('FACEBOOK_APP_SECRET'), 
            access_info["access_token"]
        )

    def get_campaign_ids(self, account_id):
        my_account = AdAccount('act_%s' % (account_id) )
        return my_account.get_campaigns()

    def get_performance_report(self, account):

        account_id = account["account_id"]
        business_plan = account["name"]
        campaign_ids = self.get_campaign_ids(account_id)

        items = []
        for campaign_id in campaign_ids:

            ## (1) Get Campaign
            id = campaign_id["id"]
            campaign = Campaign(id)
            campaign_insights = campaign.get_insights( 
                params = FaceBookReportClient.PARAM_CAMPAIGN_INSIGHTS
            )
            if len(campaign_insights) == 0:
                continue

            ## (2) Get AdSets
            ad_sets_ids = campaign.get_ad_sets( fields = [AdSet.Field.id] )
            for ad_sets_id in ad_sets_ids:

                ad_set = AdSet( ad_sets_id[AdSet.Field.id] )
                ad_set_insights = ad_set.get_insights( 
                    params = FaceBookReportClient.PARAM_SETS_INSIGHTS
                )
                if len(ad_set_insights) == 0:
                    continue

                ## (3) Get Ads
                ad_ids = ad_set.get_ads( fields = [Ad.Field.id] )
                for ad_id in ad_ids:

                    ad = Ad( ad_id[Ad.Field.id] )
                    ad_insights = ad.get_insights(
                        params = FaceBookReportClient.PARAM_AD_INSIGHTS
                    )
                    if len(ad_insights) == 0:
                        continue

                    campaign_insight = campaign_insights[0]
                    ad_set_insight = ad_set_insights[0]
                    ad_insight = ad_insights[0]

                    item = FacebookEntity(
                        ## Common
                        type = TypeConsts.TYPE_FACEBOOK,
                        id = id,
                        name = campaign_insight.get("campaign_name"),
                        customer_id = get_int( account_id ),
                        business_plan = business_plan,
                        ## Custom Info
                        adset_id = get_int( ad_set_insight.get("adset_id") ),
                        adset_name = ad_set_insight.get("adset_name"),
                        ad_id = get_int( ad_insight.get("ad_id") ),
                        ad_name = ad_insight.get("ad_name"),
                        ## Custom
                        impressions = get_int(ad_insight.get("impressions")),
                        clicks = get_int(ad_insight.get("clicks")),
                        ctr = get_float(ad_insight.get("ctr")),
                        cpc = get_float(ad_insight.get("cpc")),
                        conversions = dict_to_json(ad_insight.get("conversions")),
                        cost_per_conversion = dict_to_json(ad_insight.get("cost_per_conversion")),
                        spend = get_float(ad_insight.get("spend")),
                        reach = get_int(ad_insight.get("reach")),
                        action_values = dict_to_json(ad_insight.get("action_values")),
                        inline_link_click_ctr = get_float(ad_insight.get("inline_link_click_ctr")),
                        inline_link_clicks = get_float(ad_insight.get("inline_link_clicks")),
                        # Info
                        report_date = create_yesterday_date(),
                        create_on = create_today(),
                        create_user = CREATE_USER,
                    )
                    items.append(item)

        return items