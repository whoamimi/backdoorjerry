FROM python:3.12.0

RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
RUN apt-get -y update
RUN apt-get install -y google-chrome-stable unzip
RUN CHROME_MAJOR_VERSION=$(google-chrome --version | awk '{print $3}' | cut -d. -f1) \
    && CHROMEDRIVER_VERSION=$(wget -q -O - "https://googlechromelabs.github.io/chrome-for-testing/LATEST_RELEASE_${CHROME_MAJOR_VERSION}") \
    && wget -q "https://storage.googleapis.com/chrome-for-testing-public/${CHROMEDRIVER_VERSION}/linux64/chromedriver-linux64.zip" -O /tmp/chromedriver-linux64.zip \
    && unzip -q /tmp/chromedriver-linux64.zip -d /tmp \
    && install -m 0755 /tmp/chromedriver-linux64/chromedriver-linux64/chromedriver /usr/local/bin/chromedriver \
    && rm -rf /tmp/chromedriver-linux64 /tmp/chromedriver-linux64.zip