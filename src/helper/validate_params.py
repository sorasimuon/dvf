import re

def getValidCityParam(arguments):
    """Checkey that parameters sent are among the authorized parameters

    Args:
        arguments (dict): dictionnary of arguments sent from the request

    Returns:
        dict: dit containing the authorized arguments
    """
    authorized_args = ['commune', 'code_commune']
    args = {}
    try:
        for key, value in arguments.items():
            if key.lower() in authorized_args:
                # checkey code_commune validity
                if key.lower() == "code_commune":
                    if isValidCityCode(value):
                        args[key] = value
                        continue
                    else:
                        raise ValueError(key)
                args[key] = value
            else:
                raise NameError(key)
    except NameError as e:
        return f'''Name Error : Field name "{''.join(e.args)}" is invalid'''
    except ValueError as e:
        return f"ValueError: value format is incorrect"
    return args

def isValidCityCode(code):
    """Checkey if the code_commune is valid format 

    Args:
        code (string): string format code of digits

    Return: True if 5-digits code, else False
    """

    regex = re.compile("^[0-9]{5}$")

    return True if regex.match(code) else False 