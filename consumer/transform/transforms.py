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
    TIP_TOPIC: tip_transform,
    USER_TOPIC: user_transform
}

CASSANDRA_TABLE_NAMES = {
    BUSINESS_TOPIC: ["business_review_count", "business"],
    CHECKIN_TOPIC: ["checkin"],
    REVIEW_TOPIC: ["review_reactions", "review"],
    TIP_TOPIC: ["tip_compliment_count", "tip"],
    USER_TOPIC: ["user_statistics", "user"],
}
