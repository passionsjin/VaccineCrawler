from time import sleep

import requests

from get_config import get_config
from send_telgram import send_msg

config = get_config()
x = config['x']
y = config['y']


def get_graph_items():
    url = 'https://api.place.naver.com/graphql'
    header = {
        'content-type': 'application/json',
        'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.106 Mobile Safari/537.36'
    }
    payload = [{"operationName": "vaccineList",
                "variables": {"input": {"keyword": "코로나백신위탁의료기관", "x": x, "y": y},
                              "businessesInput": {"start": 0, "display": 100, "deviceType": "mobile", "x": x,
                                                  "y": y, "sortingOrder": "distance"}, "isNmap": False,
                              "isBounds": False},
                "query": "query vaccineList($input: RestsInput, $businessesInput: RestsBusinessesInput, $isNmap: Boolean!, $isBounds: Boolean!) {\n  rests(input: $input) {\n    businesses(input: $businessesInput) {\n      total\n      vaccineLastSave\n      isUpdateDelayed\n      items {\n        id\n        name\n        dbType\n        phone\n        virtualPhone\n        hasBooking\n        hasNPay\n        bookingReviewCount\n        description\n        distance\n        commonAddress\n        roadAddress\n        address\n        imageUrl\n        imageCount\n        tags\n        distance\n        promotionTitle\n        category\n        routeUrl\n        businessHours\n        x\n        y\n        imageMarker @include(if: $isNmap) {\n          marker\n          markerSelected\n          __typename\n        }\n        markerLabel @include(if: $isNmap) {\n          text\n          style\n          __typename\n        }\n        isDelivery\n        isTakeOut\n        isPreOrder\n        isTableOrder\n        naverBookingCategory\n        bookingDisplayName\n        bookingBusinessId\n        bookingVisitId\n        bookingPickupId\n        vaccineOpeningHour {\n          isDayOff\n          standardTime\n          __typename\n        }\n        vaccineQuantity {\n          totalQuantity\n          totalQuantityStatus\n          startTime\n          endTime\n          vaccineOrganizationCode\n          list {\n            quantity\n            quantityStatus\n            vaccineType\n            __typename\n          }\n          __typename\n        }\n        __typename\n      }\n      optionsForMap @include(if: $isBounds) {\n        maxZoom\n        minZoom\n        includeMyLocation\n        maxIncludePoiCount\n        center\n        __typename\n      }\n      __typename\n    }\n    queryResult {\n      keyword\n      vaccineFilter\n      categories\n      region\n      isBrandList\n      filterBooking\n      hasNearQuery\n      isPublicMask\n      __typename\n    }\n    __typename\n  }\n}\n"}]

    req = requests.post(url=url,
                        headers=header,
                        json=payload)

    res = req.json()

    return res[0]['data']['rests']['businesses']['items']


def detect_action(id):
    url = f'https://m.place.naver.com/rest/vaccine?vaccineFilter=used&x={x}&y={y}&selected_place_id={id}'
    send_msg(url)


if __name__ == '__main__':
    while True:
        for item in get_graph_items():
            # if item['id'] == '1721286029':
            #     detect_action(item['id'])
            if item['vaccineQuantity']['totalQuantity'] > 0:
                detect_action(item['id'])
        sleep(1)

# https://m.place.naver.com/rest/vaccine?vaccineFilter=used&selected_place_id=13229703
# url = f'https://m.place.naver.com/rest/vaccine?vaccineFilter=used&x={127.1082207}&y={37.3206381}&selected_place_id=13229703'
# https://m.place.naver.com/rest/vaccine?vaccineFilter=used&x=127.1082207&y=37.3206381&selected_place_id=13229703