import requests

def send_request(method, api_endpoint, timeout, headers=None, body=None):
    try:
        r = requests.request(method,
                             api_endpoint,
                             timeout=timeout,
                             headers=headers,
                             data=body)
        r.raise_for_status()
        return r.json()
    except requests.exceptions.HTTPError as errh:
        print("Http Error:",errh)
    except requests.exceptions.ConnectionError as errc:
        print("Error Connecting:",errc)
    except requests.exceptions.Timeout as errt:
        print("Timeout Error:",errt)
    except requests.exceptions.RequestException as err:
        print("OOps: Something Else",err)
    