def buildURL(BASE_URL, args):
    """Concatenate arguments in order to build the URL

    Args:
        BASE_URL (str): URL of the API
        args (dict[str]): list of arguments

    Returns:
        str: URL to request
    """
    string_args = "&".join([f"{k}={v}" for k, v in args.items()])
    URL = BASE_URL + "?" + string_args

    return URL
