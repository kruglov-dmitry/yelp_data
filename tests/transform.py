import unittest


class TransformTest(unittest.TestCase):

    def setUp(self):
        self.BUSINESS_DF =

    def test_output_correct(self):
        sc = SanityCheck(None, self.sanity_def)
        result = sc._test(SANITY_RESULT_CORRECT)
        self.assertTrue(result)

    def test_output_failed(self):
        sc = SanityCheck(None, self.sanity_def)
        result = sc._test(SANITY_RESULT_FAILED)
        self.assertFalse(result)