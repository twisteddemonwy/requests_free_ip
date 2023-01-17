import requests
import bs4
import random
import time


base_url = "https://www.kuaidaili.com/free/inha/"
user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"


def get_pages():
    pages = set()

    for i in range(5):
        page = random.randint(21, 61)
        pages.add(page)

    pages_url = [base_url + f"{page}/" for page in pages]

    return pages_url


def open_url(url: str):
    r = requests.get(url, headers={"user-agent": f"{user_agent}"})
    print(url, r.status_code)
    soup = bs4.BeautifulSoup(r.text, "html.parser")

    return soup


def get_ip_and_port(urls: list):
    ip_list = []
    port_list = []

    for url in urls:
        soup = open_url(url)
        _ip = soup.select('td[data-title="IP"]')
        _port = soup.select('td[data-title="PORT"]')
        ip_list.extend(_ip)
        port_list.extend(_port)

        time.sleep(5)

    return ip_list, port_list


def verify_effectiveness(ip_list: set):
    effective = []

    for ip in ip_list:
        ip = ip.replace("\n", "")
        proxies = {"http": f"{ip}", "https": f"{ip}"}
        try:
            r = requests.get(url=base_url, headers={"user-agent": f"{user_agent}"}, proxies=proxies)
            if r.status_code == 200:
                print(f"## {ip} 有效")
                effective.append(ip)
                time.sleep(5)
        except:
            print(f"{ip} 无效")

    if len(effective) != 0:
        return effective
    else:
        print("现有ip已全部失效")
        return None


def main(verify: bool = False):
    if verify:
        with open('ip.txt', 'r') as f:
            lines = set(f.readlines())
            effective = verify_effectiveness(lines)
            print(effective)
        if effective:
            with open('ip.txt', 'a') as f:
                for i in effective:
                    f.write(i+"\n")
                return True
        else:
            return True

    pages = get_pages()
    ip_list, port_list = get_ip_and_port(pages)

    with open('ip.txt', 'a') as f:
        for index in range(len(ip_list)):
            ip_str = ip_list[index].text
            port_str = port_list[index].text
            line = ip_str + ":" + port_str + "\n"
            f.write(line)


if __name__ == "__main__":
    main(True)
