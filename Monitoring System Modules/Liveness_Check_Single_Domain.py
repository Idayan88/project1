import requests

def url_status():
    url = input("Input the URL (with or without https://): ").strip()
    # Ensure the URL has a scheme
    if not url.startswith(('http://', 'https://')):
        url = f'https://{url}'
    result = {"url": url, 'status_code': ''}
    try:
        response = requests.get(url, timeout=2)
        result['status_code'] = response.status_code
        result['status_code'] = 'Alive'
    except requests.exceptions.RequestException:
        result['status_code'] = "Down"
    return result

# Call the function and print the result
print(url_status())

