# WebCrawler
USAGE:      python3 crawler.py <options>
EXAMPLES:   
- (1) python3 crawler.py -u "https://mastercard.wd1.myworkdayjobs.com/CorporateCareers" -d "./mastercard"
retrieves all job postings for mastercard and saves them under the local directory 'mastercard'
- (2) python3 crawler.py -u "https://symantec.wd1.myworkdayjobs.com/careers" -d "./symantec"
retrieve all job posting for symantec
- (3) python3 crawler.py -u "https://pvh.wd1.myworkdayjobs.com/PVH_Careers" -d "./pvh" -t 8 --verbose
\n retrieve all job postings for PVH, using 8 parallel threads and a verbose output


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
