def get_query_params(**kwargs) -> str:
    params = "?"
    for idx, (k,v) in enumerate(kwargs.items()):
        if idx == len(kwargs)-1:
            params += f"{k}={v}"
        else:
            params += f"{k}={v}&"

    return params