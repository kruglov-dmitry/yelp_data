from sparktestingbase.sqltestcase import SQLTestCase
from pyspark.sql import types as T
from consumer.transform.business import business_transform


OUTPUT_SCHEMA = T.StructType([
    T.StructField("business_id", T.StringType(), True),
    T.StructField("review_count", T.IntegerType(), True)
])

EXPECTED_ENTRIES = ["Cornelius", "Scottsdale", "Montreal", "North Las Vegas", "Mesa"]


class BusinessTest(SQLTestCase):

    def setUp(self):
        SQLTestCase.setUp(self)
        self.business_df = self.sqlCtx.read.json("./tests/fixtures/business.json")

    def test_business_transform(self):
        review_count_df, business_df = business_transform(self.business_df)

        self.assertEqual(review_count_df.schema, OUTPUT_SCHEMA)

        # uncomment below if you running Java8 - compatible with spark
        # self.assertItemsEqual(business_df.select("city").collect(),
        #                       EXPECTED_ENTRIES)
