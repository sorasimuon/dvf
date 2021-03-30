import unittest
from src.helper.validate_params import getValidCityParam, isValidCityCode


class TestValidateParams(unittest.TestCase):
    """
    UnitTest class in order to test the validaty of argument inputs from requests

    """

    def test_getValidCityParam(self):
        """
        Test validity of parameters sent when request endpoint '/summary' or '/history'
        """
        # Expect result = entries
        entries = {'commune': "MAGNY-LE-HONGRE", "code_commune": "77268"}
        result = getValidCityParam(entries)
        self.assertEqual(
            result, {'commune': "MAGNY-LE-HONGRE", "code_commune": "77268"})

        # Check wrong parameter "code"
        entries = {'commune': "MAGNY-LE-HONGRE", "code": "77268"}
        result = getValidCityParam(entries)
        self.assertEqual(
            result, '''Name Error : Field name "code" is invalid''')
    
    def test_isValidCityCode(self):
        """test code_commune format should normally return 5-digits string
        """
        code = "77268"
        self.assertTrue(isValidCityCode(code))
        code = "34534534"
        self.assertFalse(isValidCityCode(code))
        code = "2a"
        self.assertFalse(isValidCityCode(code))

if __name__ == "__main__":
    unittest.main()

