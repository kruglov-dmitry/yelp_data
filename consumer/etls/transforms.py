from consumer.constants import BUSINESS_TOPIC, REVIEW_TOPIC, USER_TOPIC, CHECKIN_TOPIC, TIP_TOPIC
from consumer.etls.business import business_transform
from consumer.etls.review import review_transform
from consumer.etls.user import user_transform
from consumer.etls.checkin import checkin_transform
from consumer.etls.tip import tip_transform


W = {
    BUSINESS_TOPIC: business_transform,
    REVIEW_TOPIC: review_transform,
    USER_TOPIC: user_transform,
    CHECKIN_TOPIC: checkin_transform,
    TIP_TOPIC: tip_transform
}
