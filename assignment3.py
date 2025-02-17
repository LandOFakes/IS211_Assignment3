import argparse
import csv
import re
import urllib.request

def download_log_file(url):
    try:
        response = urllib.request.urlopen(url)
        data = response.read().decode('utf-8')
        with open('web_log.csv', 'w') as file:
            file.write(data)
        print('Web log file downloaded successfully.')
    except Exception as e:
        print(f'Error downloading web log file: {e}')

def process_log_file():
    image_hits = 0
    total_hits = 0
    browser_counts = {}

    try:
        with open('web_log.csv', 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                total_hits += 1

                
                if re.search(r'\.(jpg|gif|png)$', row[0]):
                    image_hits += 1

                
                browser_match = re.search(r'(\w+)\/[\d.]+', row[2])
                if browser_match:
                    browser = browser_match.group(1)
                    browser_counts[browser] = browser_counts.get(browser, 0) + 1

        
        image_percentage = (image_hits / total_hits) * 100

        
        most_popular_browser = max(browser_counts, key=browser_counts.get)

        print(f'Image requests account for {image_percentage:.1f}% of all requests.')
        print(f'The most popular browser is: {most_popular_browser}')
    except FileNotFoundError:
        print("The file 'web_log.csv' does not exist. Please ensure the log file is downloaded correctly.")
    except Exception as e:
        print(f"Error processing the log file: {e}")

def main(url):
    download_log_file(url)
    process_log_file()

if __name__ == "__main__":
    """Main entry point"""
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", help="http://s3.amazonaws.com/cuny-is211-spring2015/weblog.csv", type=str, required=True)
    args = parser.parse_args(['--url', 'http://s3.amazonaws.com/cuny-is211-spring2015/weblog.csv'])
    main(args.url)
    
