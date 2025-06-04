import requests
from datetime import datetime
import pytz
from flask import current_app
from app import mongo
import os
import json
import time

class TeslaHistoryService:
    def __init__(self):
        self.collection_m3 = mongo.db.stock_history_model3

    def fetch_and_store_stock_model3(self, year, version):
        # Préparation des paramètres pour l'API Tesla
        params_dict = {
            "query": {
                "model": "m3",
                "condition": "used",
                "options": {
                    "TRIM": [version], # M3WD
                    "Year": [str(year)]
                },
                "arrangeby": "Price",
                "order": "asc",
                "market": "FR",
                "language": "fr",
                "super_region": "north america",
                "lng": -1.6744,
                "lat": 48.11,
                "zip": "35200",
                "range": 0,
                "region": "FR"
            },
            "offset": 0,
            "count": 24,
            "outsideOffset": 0,
            "outsideSearch": False,
            "isFalconDeliverySelectionEnabled": False,
            "version": None
        }
        query_str = json.dumps(params_dict)
        api_url = f'https://www.tesla.com/inventory/api/v4/inventory-results?query={requests.utils.quote(query_str)}'
        # print(f"[Tesla API] Appel à l'URL: {api_url}")
        # Préparation des headers pour l'appel API
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:139.0) Gecko/20100101 Firefox/139.0',
            'Accept': '*/*',
            'Accept-Language': 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate, br, zstd',
            'Connection': 'keep-alive',
            'Referer': 'https://www.tesla.com/fr_FR/inventory/used/m3?TRIM=M3RWD^&Year=2022^&arrangeby=plh^&range=0',
            'Cookie': 'tsla-cookie-consent=rejected; _pk_id.1.3c49=b82695ae42009926.1745240190.; akavpau_zezxapz5yf=1748705985~id=ca2fb0f74708d40c8528a028ef6fcea5; _abck=6A8B24D991654C361E6B739D368E457D~0~YAAQ2PsSAtGTrtGWAQAA4aj6Jg2BNCsZV1jol1Cr5PYr6/By23Wvn1zVSMQTY4Mhya19psRFhxv7+v2MkoDU/Mh+fxJxEyftOmqseYhybBWg+0Z+DKICjJni1ZXwblOYCPr29/z2NYRJW+53A9e1mhibFXNsBiC5d823+5Wu8kXKVqCUDu5eyg7Uon3biSGVd8dfTH1yVGJYHYwOvYlUJs1a3JkyYpfSyF+wBxO4ITkoS6iTaBjOsw2nhlAoiAggsGLwzq+eGpOx9ZyQqtuq4AkkA/N9lSRa6Wml+4bAs/cE9iZ3P263HIoFBtwS7NN68F+IeM+9MJKzRwPAXvTqtgCJJmhENj5l76LQ4B25eegyT3JZGHHccfoNWnsloPvVOVt4s3koiNQ72XHqC+HJPtOGEKu0fDca7VZxsgNOuFeA9HxzldLk/xKDKSUClanVsAqklxfnBcZU0dEziej0PFh8MtbzrLNtnn00dqm0IRR5DO6jJYa4xnILUZmRVZsrKTVAILYesLfF6rVtXYCM8sbtgfMTrlGEifPPIzZ5gkyMEnf8UuGlT+EXwz3gxrvIDGOOuT48t2gq/BFgaa3jlVGpQ+pCgmWktEYY0i0RbWe+cAJkbM4d9a3+01wBY5fJeJRc2nqdv4Gy33kZRjK9Z71+rx2hvlleRm7NGw==~-1~-1~1748707843; bm_s=YAAQ2PsSAkqVrtGWAQAAWi/7JgP9m7iw/WhU3N11NjRJqgXdWujnh9NVtryQyC7JK1P+FHWv9PfQLWJjGXHsI9BGHKAg5IZwRFxtqX+VcVoK5OU2zV5kn3h6HTpjgB7/GeqBt/hWfUGpBaKgTuoSU+e/hc11kL89SWAubuBVT4AoIwAI7XcT2exU7OorAmtBJNeodk/c3hBZE1oA2aqsF7267ZdXsr8jWxZWlYwGXy6qrq5+o9yginXqhMgnpJrUSuiyHdQ26c7PvhpzeSxzjRjyMxE9FFEo4I9ZlYWMW1uPbBYdjQU88bolNJSidkH29d10p/7zEq9zb/I+GqhmC+RmoKXNMofgYYBxEXTPuUI5/RaL8YWSq7c5lLlJCxLLb+lgu9yYjC1Wk7rwAXpqMrmqJZpB5dJHddHzl5TAG0zn8OFNSKpKFZCsY5X+x1YEkXojLlX+4wPnG2XTBM6KCd9Kobj2uejp0aiC0Wn5wq8V2Jra75d1PQj+7FrzGkE8s61yoQiGHZplIXyZmGVNn0oICgNDaxkcHPZUrvQllWRXM9JNGYuoTXzMm8J106S52WwwkApxS24ez+HXGlHKg7nM/cA5hlUJopbfvqaL99p2HFgW0qDPaWf3jQUAhWQpYftvUGnZ; bm_lso=2C60F33C3F9F394CAE8E7E10E02DB9C62C434A40A83ABE3DDCDF23BCC22A81DD~YAAQ2PsSAiKVrtGWAQAAnx77JgMESCxWmZ+zcKVseeVMnsmSAwGF2+0KvrwYWh7kcKxg72KhpbVH1sJyZUL5amUxIC2YvcScGwCv7a/svFQ/ShhdjoJxrdJFkqN5Dp39TGvMkbX9Ga4VB7gTgk9cEBrEibclNffziDGl1UOfL19X3KRtA/0XV23a1ET871cqcMJQ+iDDbFKYmJ2x0QqFCvxrgB/HtPyV/rRVuBoG6gWReo5QBRBxG1D/TGvh800NCYlc2WQbG0zod1d3s58HgYYODz0Q3YR8WbTl+x1xKTYNVnI1Z3w9urGIMQXiLttdzjWjlDjornZJflINg3lmtyexaidW1lxnP4q0qipE/6BLKP8ztIyI67gmprk1utEXBMet6jUshmuJBlNy5W2uKGPXfm6j9c1UVn5QU7ky/5ZGMeCP4GNLdt208OM/W6zF5UfciZdKyW+nZZZAhi+a0H/Z+8aUnJbwyPB7fQ6j9ezO4/Gu9cs=^1748705682088; _gcl_au=1.1.68260626.1748603858; _ga_KFP8T9JWYJ=GS2.1.s1748603857$o1$g0$t1748603860$j57$l0$h0; _ga=GA1.1.1506729388.1748603858; optimizelyEndUserId=oeu1748603857951r0.9858700584934214; homepage_ab_test_variation=A; cua_sess=050d5f3cb51cb2e774ec49d9e9ffe982; bm_sz=AF0327A8AB6C047DBD443CA2DA4A031E~YAAQ2PsSAiSVrtGWAQAAnx77JhuoUXbAlx1Ss+7iJmZGMvmkaCE0Do2e96gU+hA40VDotm+qgf7qZBm5o8f2dQTmWPkQvd8XaJGaItafUQYAC52yAjnGpER5FkxnhhSnewVnoTny0gnabF4B1O85Y7ZfZgo7TSAKwsUw8Be3A6ZKjlXQOIshje4gEijP7gAY+VbPwrdehM/jYJO51sWb84iao8L3jJ2anjLYQxiXiwb/LO47t7/T0RwhumY78UbsRXtIXCgjMRP2VerOeTR0dWr6wLnbN1WQajFFQlTfBlIqfJVb5XdF1s4dZD/qSqRVmwWOWo17nvWvPqvoa4y0dd//B9gW0qF+Umyb76oTGZB6Lpm9/qzXsT/yIAF0w0Omic6C4sta+QUzEYjYpI415YkObv6Ot5zC/Rl5tjPso5l/LWT9aeS3JiQ/uwZMVhjhesFyaVRZRNrC5oI=~4408113~3223605; bm_so=2C60F33C3F9F394CAE8E7E10E02DB9C62C434A40A83ABE3DDCDF23BCC22A81DD~YAAQ2PsSAiKVrtGWAQAAnx77JgMESCxWmZ+zcKVseeVMnsmSAwGF2+0KvrwYWh7kcKxg72KhpbVH1sJyZUL5amUxIC2YvcScGwCv7a/svFQ/ShhdjoJxrdJFkqN5Dp39TGvMkbX9Ga4VB7gTgk9cEBrEibclNffziDGl1UOfL19X3KRtA/0XV23a1ET871cqcMJQ+iDDbFKYmJ2x0QqFCvxrgB/HtPyV/rRVuBoG6gWReo5QBRBxG1D/TGvh800NCYlc2WQbG0zod1d3s58HgYYODz0Q3YR8WbTl+x1xKTYNVnI1Z3w9urGIMQXiLttdzjWjlDjornZJflINg3lmtyexaidW1lxnP4q0qipE/6BLKP8ztIyI67gmprk1utEXBMet6jUshmuJBlNy5W2uKGPXfm6j9c1UVn5QU7ky/5ZGMeCP4GNLdt208OM/W6zF5UfciZdKyW+nZZZAhi+a0H/Z+8aUnJbwyPB7fQ6j9ezO4/Gu9cs=; bm_ss=ab8e18ef4e; ak_bmsc=6F55D45511D5F8D5BF3644C5E481E96D~000000000000000000000000000000~YAAQ2PsSAs2TrtGWAQAAkKj6Jhv3fgE+DnTg1X71XggkBvrQ5mRN+2MCy9Adu9oBNnkcBfMWWssRxLwp+XZIDGY0oMk70iSm7kUAmdas26kHSkFetk9VjZTH1D7C+gecI0SIhn1mGaD+nXo2kJ6cMhtXI/opjPPA0zViaUUwm6ezOHutJWtyLFItJ6XCFSf4o21BuW2wLEfKTQEowltpYJ7BWNFDegPAF4XmP+OzyEneeW8B0qAmTuPVRuRS1o3tVJtSSULlGex7qFbo4ylvIHFlwDEtNZgD4sfPRVdn0ktpRiiiyt7jTMzNFbIc9cE++z13uglwplElZXpOLlqWlrQx3NJSEt25SYIWY6zvVIgQN16arm5TDIjR8feiTUED3kxpqJQRitFa5G2X/KK/zZPbI9uBuTujbJfDw8c/LhyHdQ==; bm_sv=522618CBC5D1591A088CE8E66EC34DAF~YAAQ2PsSAkuVrtGWAQAAWi/7JhtJdWy33JDxJ4Sp/o1rwzWP6yWO+0J+UdPoWHODVUIlnEuFP/GOnbcuDKcGiWc0ibPkCP/sDBLKmoTwFSpJkjKbMxbjQYzy0MSO83yjej5TuMNACZP1wYDlGVqC8dcXTlBelcnl28mkCVbhC0mCnfbe5D2eJuZ4HZo5GN3SPIt1p0g9XaTmOpsSb2LH7FTsjYPwvCGbZFpLJARTMDSrpGXhlUEuzydZFbVaPDcW~1; _abck=6A8B24D991654C361E6B739D368E457D~-1~YAAQRIkUAhJkcAeXAQAAcZv8Jg33XWfaA0M0dv9KRCTcMg3o2/iA176CJmsbfnK9UI2O20pTo/trlSh9rQ/bbEHmToa+ffgbB+Eq/BideaN3KmjzmqmQYDEVTAcWBmUh8h/UvUuTUdspyYR0SFpgL+H7UXRMGMNzOX2LR28dJnraweF3yby4XKTbbqtYzc+ZnLms+3D4hvkN/IeqYdW00xUdai+LfVmLr1T/cOGdBbiEiUoQwUoJjUTsWGF8IpYIjfzbhXMmk39iXoluLzv+f07zUztbvtBjqZxU7+//s5/E+ZqUUvGDjy0ZObMwSwASJ9wjMoz0/MfxOQ1f+bxOTc6YndZQOlsK3ve45VDj6sBBI0xiU50oZczwrj6xB1Xjtp+8bNtcGu7uCyppbNJ0BtplI+58HNnA0A5miy0sQ+vSSfORvdGGwZa7ECVlDRhluzM0/Agw3QF4WcexkfeT9S8cMBSBTjs8HMEcfh0Jr65XvHs+2zPapYlR7pXhvIadkbGq7dD3cYhg1WX1+0UEmNR6o1hlnBmAiZzg7SeY59wJARUyRwtCtxEbOYv0E4fwF+fEXptO2of/PcKzi8kX8YQvu+J4DB/STyoNIMboqq3nYj0KAKWXet8L09fCmPVOMT+H27Va/ddVVKrrf5nutYyDgkWNMIswTUWcfg==~0~-1~1748707843; bm_s=YAAQRIkUAhNkcAeXAQAAcZv8JgPjq7gGY8DzSAH4V3gtmNLCXldO2VSSeUgagjYVJ/QWyL2QtirFqLfEIWGt/TOrUIv183XkxkqgXQikK0WPDfiFhsOY2Y9VekZBBMChaRxiB5J/LG3O+7quPnEeQg9ng88vsfOlIT6m6SgX0tCNkhdGe82W3BxPFlcPDEsX8AEiOLOBu0174TPbSob2i73+dCioH45DyL8deVB6mVf4aMcDbLzRV60uvJNTYhIMycg3qIbsvWjDGeJSQ1KqNG4jKZCi59cHdlPCHvP5BqDj4kjg2oFnxHwW92vNBzxjETohOU1lMFiJBcEJ4Q+/47h90ywP+KPKZln3B0k8ZVXfuChN4GdkF21R8789YPIcFhY9kA/TZRrLlUMCEailuxXxy8s6puE9DCUT3gCnamvBmcNSXWimtXpQW5ysKEij3hHTeAGze6i6lIzrHKl50Y4NSejaLIgA4LzF5NJj5WK8LFyteTvBQ3WiPa6Z4Xaw+sLU4hd4G8P3H8qJRvPF8bXF46TuAY8aQWnLj0y72/tpjdodkhJqcPy9tzKuPuODMDuYg48Mr0fQz3weOBqWwMoZRoMN6Y/vcNl5xQ8fQrD2VakGRIEKrySWoTDIAWy5vCX2QJ5y; bm_sv=522618CBC5D1591A088CE8E66EC34DAF~YAAQRIkUAhRkcAeXAQAAcZv8Jhu+TNCyhTuzY37F5dEJp/Po0fi7GpwSiyjdDOH0Mbd5mh4rhE9NMj56u7p5p2qPAMS/6ZuwqxhPV9QCDOw+KUfSai6Wpja85UM0SD57lBomXEdCNl/FUS8DJGvZJHXyNCVxEt/7pxjbkMCiZ9CYMMcNtydSCv5b5kaniddqb7x/LwjcydFgcelctfhVBIGKH0kAMSqtgyURA3P8u9Ie4W9dLZuojr+YmSjCWbmu~1; bm_sz=0861D018460B7C8F994A5B5F82D70BC3~YAAQRIkUAs4HbgeXAQAAy7S3JhtmASn/FcZsBysvPBmyWffy4RuUtSn7zCFll2fGks7sjjsquND5vGQAO0VOkWIb9aN6WB+3v1BpJ+E4NEc2w+aWqShwEtOZL6I7CXKvwcbqaPeIPIMrzRaWt4fyctE0/9qIWPBpttHieyEy/IzdqSxXHTc7k7Zh11dWL2OVj5nWyq1imQijDRYlwqAZWN+QTF9UkXQkY92T41vi8FIg1Yf84Ypa0ow2JbFwZQ9ar/dwaZzIQqT7G6aJBM2ebL9RdgokIxgzEt81EJZerGvBHsnEbwllVGoM9+lFLxNnuCekr6UZMdajczaYT8dXWgmXaXznFlnlGZ4btvMF3Q==~3684164~3749953; akavpau_zezxapz5yf=1748706078~id=e494d7441928bedbe35b5d652ef33dc9',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'TE': 'trailers'
        }
        
        max_retries = 5  # Nombre maximum de tentatives en cas d'échec ou de rate limiting
        base_delay = 5   # Délai de base (en secondes) pour le backoff exponentiel
        for attempt in range(1, max_retries + 1):
            try:
                # Appel à l'API Tesla
                response = requests.get(api_url, headers=headers, timeout=90)
                print(f"[Tesla API] Tentative {attempt}, status: {response.status_code}")
                # Vérification du rate limiting (erreur 429) AVANT raise_for_status()
                if response.status_code == 429:
                    # Si le header Retry-After est présent, on l'utilise comme délai
                    retry_after = response.headers.get('Retry-After')
                    if retry_after:
                        try:
                            delay = int(retry_after)
                        except ValueError:
                            # Si le header n'est pas un entier, on utilise le backoff exponentiel
                            delay = base_delay * (2 ** (attempt - 1))
                    else:
                        # Sinon, on applique un backoff exponentiel classique
                        delay = base_delay * (2 ** (attempt - 1))
                    print(f"[Tesla API] 429 reçu, attente de {delay} secondes avant retry...")
                    # Si c'est la dernière tentative, on abandonne
                    if attempt == max_retries:
                        print("[Tesla API] Nombre maximum de tentatives atteint. Abandon.")
                        return None
                    time.sleep(delay)
                    continue  # On retente l'appel
                # Si ce n'est pas un 429, on vérifie les autres erreurs HTTP
                response.raise_for_status()
                data = response.json()  # On récupère la réponse JSON
                break  # Succès, on sort de la boucle
            except requests.exceptions.HTTPError as e:
                # Gestion explicite du 429 même si c'est une exception
                if hasattr(e.response, 'status_code') and e.response.status_code == 429:
                    retry_after = e.response.headers.get('Retry-After')
                    if retry_after:
                        try:
                            delay = int(retry_after)
                        except ValueError:
                            delay = base_delay * (2 ** (attempt - 1))
                    else:
                        delay = base_delay * (2 ** (attempt - 1))
                    print(f"[Tesla API] 429 (via exception) reçu, attente de {delay} secondes avant retry...")
                    if attempt == max_retries:
                        print("[Tesla API] Nombre maximum de tentatives atteint. Abandon.")
                        return None
                    time.sleep(delay)
                    continue
                else:
                    print(f"Erreur HTTP lors de l'appel API Tesla (tentative {attempt}): {e}")
                    if attempt == max_retries:
                        print("[Tesla API] Nombre maximum de tentatives atteint. Abandon.")
                        return None
                    delay = base_delay * (2 ** (attempt - 1))
                    print(f"[Tesla API] Attente de {delay} secondes avant retry...")
                    time.sleep(delay)
            except Exception as e:
                # Gestion des autres exceptions (réseau, parsing, etc.)
                print(f"Erreur lors de l'appel API Tesla (tentative {attempt}): {e}")
                if attempt == max_retries:
                    print("[Tesla API] Nombre maximum de tentatives atteint. Abandon.")
                    return None
                # Backoff exponentiel en cas d'erreur
                delay = base_delay * (2 ** (attempt - 1))
                print(f"[Tesla API] Attente de {delay} secondes avant retry...")
                time.sleep(delay)
        else:
            # Si la boucle se termine sans break (toutes les tentatives ont échoué)
            return None

        # Prépare le document à insérer dans MongoDB avec timestamp, année, version et data brute
        # Utilise l'heure locale du système (Europe/Paris dans Docker grâce à ENV TZ)
        document = {
            'timestamp': datetime.now(),  # datetime.now() prend le TZ du système si TZ est défini dans Docker
            'year': year,
            'version': version,
            'data': data
        }
        # Insertion du document dans la collection MongoDB
        result = self.collection_m3.insert_one(document)
        return str(result.inserted_id)
