# import codecs
import os
from html import escape
from env import REPORT_PATH, SCREENSHOT_PATH


class HtmlGenerator:
    def __init__(self, uuid, query_url, dom_screenshot, results):
        self.uuid = uuid
        self.query_url = query_url
        self.screenshot = os.path.join(SCREENSHOT_PATH, f'{self.uuid}.png')
        self.dom_screenshot = dom_screenshot
        self.results = results
        self.template = ''
        self.run()

    def generate_report_template(self):
        img_link = f'<img src={self.screenshot} alt="screenshot" class="text-center my-3 img-fluid" width="70%" />' or ''

        self.template = f'''<html>
        <head>
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" integrity="sha384-1BmE4kWBq78iYhFldvKuhfTAU6auU8tT94WrHftjDbrCEXSU1oBoqyl2QvZ6jIW3" crossorigin="anonymous">
        <title>Safety Report: {self.query_url}</title>
        </head>
        
        <body>
            <div class="text-center">
                <h1 class="text-center">Safety Report:</h1>
                <h2 class="text-center">{self.query_url}</h2>
                {img_link}
            </div>
            <div>
                <h2 class="text-center">Results</h2>
                <div class="overflow-auto ms-2" style="width: 97vw">
                    <pre class="overflow-auto" style="white-space: pre-wrap;">
                    <code id="results">
                    
                    </code>    
                    </pre>
                </div>
            </div>
            <div>
                <h2 class="text-center">DOM Screenshot</h2>
                <div class="overflow-auto ms-2" style="width: 97vw">
                    <pre class="overflow-auto" style="white-space: pre-wrap;"><code class="overflow-auto">{escape(self.dom_screenshot)}</code></pre>
                </div>
            </div>
        </body>
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js" integrity="sha384-ka7Sk0Gln4gmtz2MlQnikT1wXgYsOg+OMhuP+IlRH9sENBO0LRn5q+8nbTov4+1p" crossorigin="anonymous"></script>
        <script>
            const results_to_json = JSON.stringify({self.results}, null, 4)
            const result_el = document.querySelector('#results')
            result_el.innerHTML = results_to_json
        </script>
        </html>
        '''

    def write_to_file(self):
        if not(os.path.exists(REPORT_PATH) and os.path.isdir(REPORT_PATH)):
            os.makedirs(REPORT_PATH, exist_ok=True)
        with open(os.path.join(REPORT_PATH, f'{self.uuid}.html'), 'w') as f:
            f.write(self.template)

    def run(self):
        self.generate_report_template()
        self.write_to_file()
