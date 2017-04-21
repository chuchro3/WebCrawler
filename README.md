# WebCrawler
OVERVIEW:
<br />
This is a web crawler intended to scrape job postings given a workday job postings URL. The files are stored by job posting ID, and contain a json with a detailed description of the posting from the given sub-urls, as well as notable labels pulled from the original posting description containing info like job title, location, posted date in a list.
<br />
Once we get all job URLs on the first page, retrieving the details of each job posting from branching URLs can be done in parallel (see options below).
<br />
The crawler has been successfully tested with 3 different workday job posting websites. It should readily expand to more!

<br /><br />


CONTENTS:
<br />
- crawler.py
<br /> main logic for scraping workday job postings, as well as starting the main program
- util.py
<br />  utility functions used by the crawler. not crawler dependent

<br /><br />
USAGE:      python3 crawler.py <options>
EXAMPLES:   
- (1) python3 crawler.py -u "https://mastercard.wd1.myworkdayjobs.com/CorporateCareers" -d "./mastercard"
<br /> retrieves all job postings for mastercard and saves them under the local directory 'mastercard'
- (2) python3 crawler.py -u "https://symantec.wd1.myworkdayjobs.com/careers" -d "./symantec"
<br /> retrieve all job postings for symantec
- (3) python3 crawler.py -u "https://pvh.wd1.myworkdayjobs.com/PVH_Careers" -d "./pvh" -t 8 --verbose
<br /> retrieve all job postings for PVH, using 8 parallel threads and a verbose output


Options:

- -h, --help
show this help message and exit

- -u MAIN_LINK, --url=MAIN_LINK
Job Posting URL 
[Default: https://mastercard.wd1.myworkdayjobs.com/CorporateCareers]

- -d DEST_DIR, --dest=DEST_DIR
Destination Directory 
[Default: ./test]

- -t THREAD_COUNT, --threads=THREAD_COUNT
Number of parallel threads 
[Default: 4]

- -v, --verbose
Verbose output to sdout 
[Default: False]
