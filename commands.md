Create python virtual environment
`python -m venv venv`

Start an already created virtual environment in terminal
`source venv/bin/activate`

Create a new Scrapy project
`scrapy startproject bookscraper`

Run a spider using Scrapy
`scrapy crawl bookspider`

Run a spider using Scrapy and save output to a file
`scrapy crawl bookspider -O bookdata.csv`