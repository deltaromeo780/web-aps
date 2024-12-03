import aiohttp
import asyncio
from datetime import datetime, timedelta


async def fetch_data(session, code, start_date, end_date):
    url = f"http://api.nbp.pl/api/exchangerates/rates/c/{code}/{start_date}/{end_date}?format=json"
    try:
        async with session.get(url) as response:
            json_eu = await response.json()
            return json_eu
    except Exception as e:
        print(f"An error occurred for {code}: {e}")
        return None


async def main():
    # last 10 days
    end_date = datetime.now()
    start_date = end_date - timedelta(days=10)

    start_date_str = start_date.strftime("%Y-%m-%d")
    end_date_str = end_date.strftime("%Y-%m-%d")
    codes = ['USD', 'EUR']

    print(f"start date: {start_date_str} ", end="")
    print(f"end date: {end_date_str}")

    connector = aiohttp.TCPConnector(ssl=False)
    async with aiohttp.ClientSession(connector=connector) as session:
        tasks = [fetch_data(session, code, start_date_str, end_date_str) for code in codes]
        json_eu_list = await asyncio.gather(*tasks)

    result = []

    for json_eu in json_eu_list:
        for rate_entry in json_eu["rates"]:
            date = rate_entry["effectiveDate"]
            code = json_eu["code"]
            bid = rate_entry["bid"]
            ask = rate_entry["ask"]

            found_date = next((item for item in result if date in item), None)

            if not found_date:
                result.append({date: {code: {"purchase": [bid], "sale": [ask]}}})
            else:
                if code not in found_date[date]:
                    found_date[date][code] = {"purchase": [bid], "sale": [ask]}
                else:
                    found_date[date][code]["purchase"].append(bid)
                    found_date[date][code]["sale"].append(ask)

    print(result)
    return result


if __name__ == "__main__":
    r = asyncio.run(main())
    print(r)
