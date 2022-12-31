
import os
import logging

from apiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials

from consts.common_consts import *
from utils.common_utils import *
from entity.google_analytics_entity import *

class GoogleAnalyticsReportClient():

    SCOPES = ['https://www.googleapis.com/auth/analytics.readonly']

    def __init__(self):

        # Credential
        credentials = ServiceAccountCredentials.from_json_keyfile_name(
            os.environ.get('GOOGLE_APPLICATION_CREDENTIALS'),
            GoogleAnalyticsReportClient.SCOPES
        )

        # Build the service object.
        self.analytics = build(
            'analyticsreporting', 
            'v4', 
            credentials=credentials
        )

    def get_performance_report(self, account):

        business_plan = account["name"]
        customer_id = account["account_id"]
        view_id = account["option1"]

        body = {
            'reportRequests': [{
                'viewId': view_id,
                'dateRanges': [{
                    'startDate': 'yesterday',
                    'endDate': 'yesterday'
                }],
                'metrics': [
                    {"expression": "ga:users"},
                    {'expression': 'ga:sessions'},
                    {"expression": "ga:pageviews"},
                    {'expression': 'ga:sessionDuration'},
                ],
#                'dimensions': [{
#                    'name': 'ga:country'
#                }]
            }]
        }

        result = self.analytics.reports().batchGet( body = body ).execute()

        items = []
        for report in result.get('reports', []):

            columnHeader = report.get('columnHeader', {})
            dimensionHeaders = columnHeader.get('dimensions', [])
            metricHeaders = columnHeader.get('metricHeader', {}).get('metricHeaderEntries', [])

            for row in report.get('data', {}).get('rows', []):

                dimensions = row.get('dimensions', [])
                dateRangeValues = row.get('metrics', [])

                dimention_dict = {}
                for header, dimension in zip(dimensionHeaders, dimensions):
                    dimention_dict[header] = dimension

                metrics_dict = {}
                for i, values in enumerate(dateRangeValues):
                    for metricHeader, value in zip(metricHeaders, values.get('values')):
                        metrics_dict[metricHeader.get('name')] = value

                item = GoogleAnalyticsEntity(
                    type = TypeConsts.TYPE_GOOGLE_ANALYTICS,
                    id = view_id,
                    customer_id = customer_id,
                    business_plan = business_plan,
                    users = int(metrics_dict.get("ga:users")),
                    sessions = int(metrics_dict.get("ga:sessions")),
                    pageviews = int(metrics_dict.get("ga:pageviews")),
                    sessionDuration = float(metrics_dict.get("ga:sessionDuration")),
                    ## Info
                    report_date = create_yesterday_date(),
                    create_on = create_today(),
                    create_user = CREATE_USER,
                )
                items.append( item )

        return items
