from consumer.constants import BUSINESS_TOPIC, REVIEW_TOPIC, USER_TOPIC, CHECKIN_TOPIC, TIP_TOPIC
from consumer.transform.business import business_transform
from consumer.transform.review import review_transform
from consumer.transform.user import user_transform
from consumer.transform.checkin import checkin_transform
from consumer.transform.tip import tip_transform


TRANSFORM_METHOD = {
    BUSINESS_TOPIC: business_transform,
    CHECKIN_TOPIC: checkin_transform,

    REVIEW_TOPIC: review_transform,
    USER_TOPIC: user_transform,
    TIP_TOPIC: tip_transform
}

CASSANDRA_TABLE_NAMES = {
    BUSINESS_TOPIC: ["yelp_data.business_review_count", "yelp_data.business"],
    CHECKIN_TOPIC: ["yelp_data.checkin"],
    REVIEW_TOPIC: ["yelp_data.review_reactions", "yelp_data.review"],

    TIP_TOPIC: ["yelp_data.tip", "yelp_data.tip_compliment_count"],
    USER_TOPIC: ["yelp_data.user_statistics", "yelp_data.user"],
}