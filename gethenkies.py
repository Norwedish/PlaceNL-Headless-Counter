import requests
import time
from datetime import datetime

def get_total_headless_henk_versions(data):
    total_headless_henk = 0
    brands = data.get('brands', {})
    for brand in brands.values():
        headless_henk = brand.get('Headless-Henk', {})
        for version_count in headless_henk.values():
            total_headless_henk += version_count
    return total_headless_henk

def get_total_userscripts(data):
    total_userscripts = 0
    brands = data.get('brands', {})
    for brand in brands.values():
        userscripts = brand.get('Userscript', {})
        for userscript_count in userscripts.values():
            total_userscripts += userscript_count
    return total_userscripts

def main():
    previous_henkies_count = 0
    previous_userscript_count = 0
    previous_difference_count = 0

    while True:
        try:
            response = requests.get('https://chief.placenl.nl/api/stats')
            data = response.json()

            total_headless_henk = get_total_headless_henk_versions(data)
            henk_change = "up" if total_headless_henk > previous_henkies_count else "down"
            total_userscripts = get_total_userscripts(data)
            userscript_change = "up" if total_userscripts > previous_userscript_count else "down"
            difference = (abs(total_headless_henk - total_userscripts))
            difference_change = "up" if difference > previous_difference_count else "down"

            previous_henkies_count = total_headless_henk
            previous_userscript_count = total_userscripts
            previous_difference_count = difference

            # Clear previous output
            print("\033[H\033[J", end='')

            current_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            print(f'Current Date and Time: {current_datetime}')
            print(f'Total Headless-Henk versions: {total_headless_henk} {henk_change}')
            print(f'Total Userscripts: {total_userscripts} {userscript_change}')
            print(f'Difference: {difference} {difference_change}')

            old_headless_henk = total_headless_henk
            old_userscripts = total_userscripts
        except Exception as e:
            print(f'Error occurred: {e}')

        time.sleep(2)

if __name__ == "__main__":
    main()