import csv
import json
import requests


URL = 'https://kwork.ru/catalog_kworks_filters/logo/vizitki'


def get_parsed_kwork(kwork: dict, to_parse: tuple[str]) -> tuple:
    return tuple(
        kwork[item]
        if item in kwork else "Not fount"
        for item in to_parse
    )


def parse_url(url: str, page_count: int, file_name: str,
              to_parse: tuple[str] = ("gtitle", "price", "userName", "userRating", "userRatingCount", "url")) -> None:

    exclude_ids: set[int] = set()
    with open(file_name, 'w', encoding='utf-8', newline='') as fout:
        writer = csv.writer(fout)
        writer.writerow(to_parse)

        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                                 "Chrome/114.0.0.0 Safari/537.36 OPR/100.0.0.0"}

        for page in range(page_count):

            exclude_ids_str = ','.join(map(str, exclude_ids))
            payload = {"page": page, "excludeIds": exclude_ids_str}
            raw = requests.get(url, headers=headers, json=payload)

            data = json.loads(raw.text)
            kworks = data["data"]["stateData"]["viewData"]["kworks"]["posts"]["data"]
            for kwork in kworks:
                writer.writerow(get_parsed_kwork(kwork, to_parse))
                exclude_ids.add(kwork["id"])


if __name__ == '__main__':
    parse_url(URL, 5, "data.csv")
