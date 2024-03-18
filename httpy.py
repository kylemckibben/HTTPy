import http.client
import json

def strip_scheme(url: str) -> str:
    """
        Strip scheme from url to avoid
        conflict from http.client request
        expecting a port number after :

        Params:
        -url: url string passed to request method

        Return:
        -stripped url
    """
    if is_https(url):
        return url[8:]
    if url[0:7] == 'http://':
        return url[7:]
    return url

def parse_path(url: str) -> str:
    """
        Obtain url path for http.client request.

        Params:
        -url: url passed to request method

        Return:
        -path part of url 
    """
    path_start = url.find('/')
    if path_start == -1:
        return
    return url[path_start:]

def is_https(url: str) -> bool:
    """
        Checks url scheme to see if it's https or not

        Params:
        -url: url string passed to request method

        Return:
        -resulting boolean  
    """
    if url[0:8] == 'https://':
        return True
    return False 

def build_response_dict(response: object) -> dict:
    """
        Construct response dictionary out of the response.

        Params:
        -response: response object from http request
        
        Return:
        -formatted response results
    """
    body = response.read().decode()
    return {
        "status": f"{response.status} {response.reason}",
        "version": "HTTP/1.1" if response.version == 11 else "HTTP/1.0",
        "body": json.loads(body) if body != "" else body,
    }

def https_request(method: str, url: str, path: str, port=443) -> object:
    """
        Handle HTTPS requests

        Params:
        -method: HTTP method for request
        -url: host url to establish HTTPS connection
        -path: path for request
        -port: server port for request

        Return:
        -response object
    """
    client = http.client.HTTPSConnection(url, port)
    client.request(method, path)
    response = build_response_dict(client.getresponse())
    client.close()
    return response

def http_request(method: str, url: str, path: str, port=80) -> object:
    """
        Handle HTTP requests

        Params:
        -method: HTTP method for request
        -url: host url to establish HTTP connection
        -path: path for request
        -port: server port for request

        Return:
        -response object
    """
    client = http.client.HTTPConnection(url, port) 
    client.request(method, path)
    response = build_response_dict(client.getresponse())
    client.close()
    return response

def get(url: str, port=None):
    """
        Handle get requests, HTTPS or HTTP depending
        on url scheme. If no scheme present nor port
        443 specified, connection will default to HTTP.

        Params:
        -url: full url for get request

        Return:
        -call to https_request() or http_request() method
    """
    stripped_url = strip_scheme(url)
    path = parse_path(stripped_url) 
    host = stripped_url[:-len(path)] if path != None else stripped_url 
    if is_https(url) == True or port == 443:
        return https_request('GET', host, path, port)
    return http_request('GET', host, path, port)
         

