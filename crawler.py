from multiprocessing import Process, Array
import sys
import util

class JobPosting(object):
    '''
    Holds basic information for each job posting
    '''
    def __init__(self, post, base_url):
        self.ID = post['id']
        
        #we can extract generally useful information from 'text' keys
        labels = list(util.extract_all_keys(post, 'text'))
        self.info = {'labels': labels}

        self.url = base_url + post['title']['commandLink']

def get_job_postings(main_link, dest_dir, thread_count, verbose):

    postings_page_dic = util.get_request_to_dic(main_link, verbose)

    #find the pagination end point
    end_points = util.extract_key(postings_page_dic, 'endPoints')
    base_url = main_link.split('.com')[0] + '.com'
    pagination_end_point = base_url
    pagination_key = "Pagination"
    for end_point in end_points:
        if end_point['type'] == pagination_key:
            pagination_end_point += end_point['uri'] + '/'
            break


    #paginate until we have all the postings
    if verbose:
        print("Scraping list of all job postings..\n")
    job_postings = []
    while True:

        #attempt to retrieve list of job postings from json response
        postings_list = util.extract_key(postings_page_dic, 'listItems')
        if postings_list is None:
            break
        
        paginated_urls = [JobPosting(post, base_url) for post in postings_list]

        job_postings += paginated_urls

        postings_page_dic = util.get_request_to_dic(pagination_end_point + str(len(job_postings)), verbose)

    if verbose:
        print("\nThere are", len(job_postings), "job postings.\n")
        print("Scraping full descriptions of each job posting..\n")
    threads = []
    for i in range(thread_count):
        start = int(i * len(job_postings) / thread_count)
        end = int((i+1) * len(job_postings) / thread_count)
        thread = Process(target=get_job_description, args=(job_postings, start, end, dest_dir, verbose))
        threads.append(thread)
        thread.start()

    for i in range(thread_count):
        threads[i].join()

    if verbose:
        print("\nDone. All files stored under", dest_dir)

def get_job_description(job_postings, start, end, dest_dir, verbose=False):
    '''
    Iterates through [start, end) portion of the job postings, retrieves their full description, and writes to file

    Input:
        job_postings: list of JobPosting
        start: start index
        end: end index
        dest_dir: write path for file storage
    Returns:
        No return, writes to file
    '''
    for i in range(start, end):
        job_posting = job_postings[i]
        job_page_dic = util.get_request_to_dic(job_posting.url, verbose)
        description = util.extract_key(job_page_dic, 'description')
        job_info = job_posting.info
        job_info['description'] = description
        util.write_to_file(job_posting.ID, job_info, dest_dir)





def read_command(argv):
    """
    Processes the command used to get job postings from the command line.
    """
    from optparse import OptionParser
    usageStr = """
    USAGE:      python3 crawler.py <options>
    EXAMPLES:   
        (1) python3 crawler.py -u "https://mastercard.wd1.myworkdayjobs.com/CorporateCareers" -d "./mastercard"
            - retrieves all job postings for mastercard and saves them under the local directory 'mastercard'
        (2) python3 crawler.py -u "https://symantec.wd1.myworkdayjobs.com/careers" -d "./symantec"
            - retrieve all job posting for symantec
        (3) python3 crawler.py -u "https://pvh.wd1.myworkdayjobs.com/PVH_Careers" -d "./pvh" -t 8 --verbose
            - retrieve all job postings for PVH, using 8 parallel threads and a verbose output
    """
    parser = OptionParser(usageStr)
    
    parser.add_option('-u', '--url', type='string', dest='main_link', help=default('Job Posting URL'), default='https://mastercard.wd1.myworkdayjobs.com/CorporateCareers')
    parser.add_option('-d', '--dest', type='string', dest='dest_dir', help=default('Destination Directory'), default='./test')
    parser.add_option('-t', '--threads', type='int', dest='thread_count', help=default('Number of parallel threads'), default=4)
    parser.add_option('-v', '--verbose', action='store_true', dest='verbose', help=default('Verbose output to sdout'), default=False)
    options, otherjunk = parser.parse_args(argv)
    assert len(otherjunk) == 0, "Unrecognized options: " + str(otherjunk)
    return vars(options)


def default(str):
    return str + ' [Default: %default]'

def parse_comma_separated_args(option, opt, value, parser):
    setattr(parser.values, option.dest, value.split(','))

if __name__ == '__main__':
    options = read_command(sys.argv[1:])
    get_job_postings(**options)
