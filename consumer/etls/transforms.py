from consumer.constants import BUSINESS_TOPIC, REVIEW_TOPIC, USER_TOPIC, CHECKIN_TOPIC, TIP_TOPIC
from consumer.transform.business import business_transform
from consumer.transform.review import review_transform
from consumer.transform.user import user_transform
from consumer.transform.checkin import checkin_transform
from consumer.transform.tip import tip_transform


W = {
    BUSINESS_TOPIC: business_transform,
    CHECKIN_TOPIC: checkin_transform,

    REVIEW_TOPIC: review_transform,
    USER_TOPIC: user_transform,
    TIP_TOPIC: tip_transform
}
