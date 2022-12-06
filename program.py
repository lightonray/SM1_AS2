"This application is for calculates URL web console performance"

import unittest
import json
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

CYCLE = 10
URL = "https://en.wikipedia.org/wiki/Software_metric"

class Test(unittest.TestCase):
    "This class is to calculate URL Performance and produce the required report files"

    def setUp(self):
        "Webdriver configuration"
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(30)
        self.verification_errors = []
        self.wait = WebDriverWait(self.driver, CYCLE)
        self.address = URL

    def test_er(self):
        """
        Main function // runs URL performance for 10 times,
        generates csv, txt, and json files, while calculates
        average of the performance.
        """
        driver = self.driver
        total = {}
        csv_count = {}
        csv_duration = {}
        # Creates an output.txt file and appends the name and duration
        with open("result.txt", mode='w' , encoding='utf-8') as json_file:
            for result in range(CYCLE):
                driver.get(URL)
                result = driver.execute_script("return window.performance.getEntries()")

                for current in result:
                    url = current["name"]
                    current_list = total.get(url, [])
                    current_list.append(current["duration"])
                    total[url] = current_list
                    json_file.write(f"{current['name']}, {current['duration']}\n")

        # Creates a csv file and calculates the average duration and appends it to the csv file
        with open("result_in_csv.csv", "w", encoding='utf-8') as csv_file:
            for key, value in total.items():
                average = sum(value) / len(total)
                csv_file.write(f"{key}, {average}\n")

        # Creates a JSON output file and prettifies it
        with open("output_json" + ".json", "w",encoding="utf-8") as file:
            json.dump(result, file, ensure_ascii=False, indent=4)
            result = self.driver.get(URL)
            self.assertIn(self.address, self.driver.current_url)
            script = "return window.performance.getEntries();"
            perf = self.driver.execute_script(script)

            for curr in perf:
                if 'https:' not in curr['name']:
                    continue
                if csv_count.get(curr['name'], None):
                    csv_count[curr['name']] += 1
                else:
                    csv_count[curr['name']] = 1
                csv_duration[curr['name']] = csv_duration.get(curr['name'], 0) + curr['duration']

        dict_for_json = {}
        dict_for_json_id = 0
        for key, value in csv_duration.items():
            dict_for_json[f'{dict_for_json_id}'] = {'name': key, 'duration': (value/csv_count[key])}
            dict_for_json_id += 1

        with open('output_json_name_and_duration.json','w',encoding='utf-8') as f_h:
            json.dump(dict_for_json, f_h, indent=1)
        with open('output_json_name_and_duration.json', 'r',encoding='utf-8') as f_h:
            result = json.load(f_h)

    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verification_errors)


if __name__ == "__main__":
    unittest.main()
