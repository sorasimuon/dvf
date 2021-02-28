import unittest
from src.helper.validate_params import getValidCityParam


class TestValidateParams(unittest.TestCase):
    """
    UnitTest class in order to test the validaty of argument inputs from requests

    """

    def test_getValidCityParam(self):
        """
        Test validity of parameters sent when request endpoint '/city'
        """
        # Expect result = entries
        entries = {'commune': "MAGNY-LE-HONGRE", "code_commune": "77700"}
        result = getValidCityParam(entries)
        self.assertEqual(
            result, {'commune': "MAGNY-LE-HONGRE", "code_commune": "77700"})

        # Check wrong parameter "code"
        entries = {'commune': "MAGNY-LE-HONGRE", "code": "77700"}
        result = getValidCityParam(entries)
        self.assertEqual(
            result, {'commune': "MAGNY-LE-HONGRE"})


if __name__ == "__main__":
    unittest.main()
