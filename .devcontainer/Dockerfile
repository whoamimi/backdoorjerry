FROM python:3.12.0

RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
RUN apt-get -y update
RUN apt-get install -y google-chrome-stable unzip
RUN CHROME_VERSION=$(google-chrome --version | awk '{print $3}') \
    && CHROMEDRIVER_URL=$(python3 -c "import json, sys, urllib.request; version=sys.argv[1]; build='.'.join(version.split('.')[:3]); known=json.load(urllib.request.urlopen('https://googlechromelabs.github.io/chrome-for-testing/known-good-versions-with-downloads.json'))['versions']; entry=next((item for item in known if item['version'] == version), None); entry=entry or json.load(urllib.request.urlopen('https://googlechromelabs.github.io/chrome-for-testing/latest-patch-versions-per-build-with-downloads.json'))['builds'][build]; print(next(item['url'] for item in entry['downloads']['chromedriver'] if item['platform'] == 'linux64'))" "${CHROME_VERSION}") \
    && wget -q "${CHROMEDRIVER_URL}" -O /tmp/chromedriver-linux64.zip \
    && unzip -q /tmp/chromedriver-linux64.zip -d /tmp \
    && install -m 0755 /tmp/chromedriver-linux64/chromedriver-linux64/chromedriver /usr/local/bin/chromedriver \
    && rm -rf /tmp/chromedriver-linux64 /tmp/chromedriver-linux64.zip