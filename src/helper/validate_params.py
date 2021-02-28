
def getValidCityParam(arguments):
    """Check that parameters sent are among the authorized parameters

    Args:
        arguments (dict): dictionnary of arguments sent from the request

    Returns:
        dict: dit containing the authorized arguments
    """
    authorized_args = ['commune', 'code_commune']
    args = {}
    for k, v in arguments.items():
        if k.lower() in authorized_args:
            args[k] = v
    return args
