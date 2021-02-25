from googleapiclient.discovery import build


def google_search(search_term, api_key, cse_id, **kwargs):
    service = build("customsearch", "v1", developerKey=api_key)
    res = service.cse().list(q=search_term, cx=cse_id, **kwargs).execute()
    return res


my_api_key = "AIzaSyCbDY9NzTLp5Ep40kEM3VwFaVODw0dVwqk"
my_cse_id = "015777106269543801002:ltgydzdvijk"

result = google_search("Coffee", my_api_key, my_cse_id)
print(result)
