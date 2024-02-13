import aiohttp
import asyncio
import aiofiles
from time import time

# pip install aiohttp asyncio aiofiles

valid_file_name = "ok.txt"
invalid_file_name = "failed.txt"
input_file_name = "inputs.txt"
proxy = "http://username:password@host:port"
threads = 100
timeout = 30
retry_count = 3


async def make_request(session, url, headers, data, proxy):
    for i in range(retry_count):
        try:
            async with session.post(url, headers=headers, data=data, proxy=proxy, timeout=timeout) as response:
                response_text = await response.text()
                return response_text
        except asyncio.TimeoutError:
            print(f"Timeout error for {url}")
        except aiohttp.ClientError as e:
            print(f"Failed to open {url}: {e}")
    return None


async def checkData(session, number, sem, lock):
    if number.strip() == "":
        return

    url = 'api link here'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/116.0'
    }

    data = {
        # form data is placed here
    }

    async with aiohttp.ClientSession() as session:
        response_text = await make_request(session, url, headers, data, proxy)
        if response_text is None:
            print("Failed to make the request.")
            return
        if 'condition is true' in response_text:
            print("Valid {}".format(number))
            async with sem:
                async with lock:
                    async with aiofiles.open(valid_file_name, mode='a', encoding='utf-8') as file:
                        await file.write(number + '\n')
        else:
            print("Invalid {}".format(number))
            async with sem:
                async with lock:
                    async with aiofiles.open(invalid_file_name, mode='a', encoding='utf-8') as file:
                        await file.write(number + '\n')


async def main():
    numbers = open(input_file_name, mode='r',
                   encoding='utf-8').read().split('\n')
    sem = asyncio.Semaphore(threads)
    lock = asyncio.Lock()
    async with aiohttp.ClientSession() as session:
        await asyncio.gather(*[checkData(session, number, sem, lock) for number in numbers])

if __name__ == "__main__":
    started = int(time())
    asyncio.run(main())
    print("Time taken: {}".format(int(time()) - started))
