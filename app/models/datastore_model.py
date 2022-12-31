from gcloud import datastore

from consts.common_consts import *
from typing import List, Set, Dict, Tuple, TypeVar, Callable

class DataStoreClient():

    KIND_ACCOUNT_INFO = "account_info"
    KIND_ACCESS_INFO = "access_info"

    def __init__(self, parameter: Dict[str, str]) -> None:
        self.client = datastore.Client(parameter['project'])

    def get_accounts(self, type: str) -> List[datastore.Entity]:
        
        query = self.client.query(
            kind = DataStoreClient.KIND_ACCOUNT_INFO
        )

        query.add_filter("type", "=", type)
        return list(query.fetch())

    def get_access_info(self, type: str) -> datastore.Entity:
        
        query = self.client.query(
            kind = DataStoreClient.KIND_ACCESS_INFO
        )

        query.add_filter("type", "=", type)
        ret = list(query.fetch())
        if len(ret) == 1:
            return ret[0]
        else:
            print( "Access Info is not correct for %s." % (type) )
            return None