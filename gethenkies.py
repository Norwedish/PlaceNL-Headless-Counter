import requests
import time
import math
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
    previous_henkies_count = [0, 0, 0]
    previous_userscript_count = [0, 0, 0]
    previous_difference_count = [0, 0, 0]

    while True:
        try:
            response = requests.get('https://chief.placenl.nl/api/stats')
            data = response.json()

            prev_henkies_calc = (math.floor((previous_henkies_count[0]+previous_henkies_count[1]+previous_henkies_count[2]) / 3))
            prev_userscript_calc = (math.floor((previous_userscript_count[0]+previous_userscript_count[1]+previous_userscript_count[2]) / 3))
            prev_diff_calc = (math.floor((previous_difference_count[0]+previous_difference_count[1]+previous_difference_count[2]) / 3))

            total_headless_henk = get_total_headless_henk_versions(data)
            henk_change = "up" if total_headless_henk > prev_henkies_calc else "down"
            if total_headless_henk == previous_henkies_count[0]:
                henk_change = "same"

            total_userscripts = get_total_userscripts(data)
            userscript_change = "up" if total_userscripts > prev_userscript_calc else "down"
            if total_userscripts == previous_userscript_count[0]:
                userscript_change = "same"

            difference = (abs(total_headless_henk - total_userscripts))
            difference_change = "up" if difference > prev_diff_calc else "down"
            if difference == previous_difference_count[0]:
                difference_change = "same"


            # Clear previous output
            print("\033[H\033[J", end='')

            current_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            print(f'Current Date and Time: {current_datetime}')

            print(f'Total Headless-Henk versions:	{total_headless_henk},	last count:	{previous_henkies_count[0]},	average of 3:	{prev_henkies_calc},	state:	{henk_change}')
            print(f'Total Userscripts:		{total_userscripts},	last count:	{previous_userscript_count[0]},	average of 3:	{prev_userscript_calc},	state:	{userscript_change}')
            print(f'Difference:			{difference},	last count:	{previous_difference_count[0]},	average of 3:	{prev_diff_calc},	state:	{difference_change}')

            previous_henkies_count.pop(2)
            previous_henkies_count.insert(0, total_headless_henk)

            previous_userscript_count.pop(2)
            previous_userscript_count.insert(0, total_userscripts)

            previous_difference_count.pop(2)
            previous_difference_count.insert(0, difference)
        except Exception as e:
            print(f'Error occurred: {e}')

        time.sleep(1)

if __name__ == "__main__":
    main()