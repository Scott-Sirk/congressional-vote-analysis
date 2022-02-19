
import requests
import time
import urllib.request
from cva.core import Core

class Web(Core):
    '''
    parent class for all web collection classes
    
    Attributes:
        <str> _log_file: location of log file(from cva.core.Core)
    '''
    def __init__(self):
        '''
        create an instace of the Web() class
        
        Args:
            None
            
        Returns:
            <cva.collector.web.Web>: instance of the class
            
        Raises:
            N/A
        '''
        super().__init__()
    
    def build_url(self, base, params):
        '''
        build a url given a base string with placeholders
        and a dictionary of paramerters
        
        Args:
            <str> base: base URL formatted like https://www.webste/{param1}/{param2}
            <dict> params: dictionary with real values formatted like
                {'param1':'value1', 'param2':'valule2'}
        
        Returns:
            <str>: formatted URL
            
        Raises:
            N/A
        '''
        #unpack params and format url with "real" values
        url = base.format(**params)
        return url
    
    def ping_url(self, url):
        '''
        check if a URL gives a 200 response
        
        Args:
            <str> url: URL to check
            
        Returns:
            <bool>: true if response wsa 200 else false
            
        Raises:
            N/A
        '''
        #GET to URL
        try:
            response = requests.get(url)
        except Exception as e:
            self.log(
                    'cva.collector.web.Web.Warning'
                    , f'Failed to connect to {url}, Error: {e}')
            return False
        else:
            #unpack response code
            response_code = response.status_code
            #if 200 return true else false
            if response_code == 200:
                return True
            else:
                return False
    
    def download_content(self, url):
        '''
        download content from a URL
        
        Args:
            <str> url: URL to download from
            
        Returns:
            <str>: return content as string(utf-8)
            
        Raises:
            N/A
        '''
        #use ping_url to confirm url is valid
        if self.ping_url(url):
            #try to download content with urlopen            
            try:
                with urllib.request.urlopen(url) as f:
                    #decode content to utf-8
                    content = f.read().decode('utf-8')
                    return content
            #if that fails try to download content with requests.get
            except Exception as e1:
                self.log(
                        'cva.collector.web.Web.download_content.Warning'
                        , f'Failed to download content, Message:{e1}')
                try:
                    content = requests.get(url).content.decode('utf-8')
                    return content
                #if that fails log the error and return
                except Exception as e2:
                    self.log(
                            'cva.collector.web.Web.download_content.Error'
                            , f'Failed to download content, Message:{e2}')
                    return ''
        #if url wasn't valid log and return
        else:
            self.log(
                    'cva.collector.web.Web.download_content.Warning'
                    , f'{url} did not return status 200')
            return ''

class Clerk_House_Gov(Web):
    '''
    data found at https://www.congress.gov/roll-call-votes
    download House data from https://clerk.house.gov/
    
    Attributes:
        <str> _log_file: location of log file(from cva.core.Core)
        <str> _url_template: base URL to download raw data
    '''
    def __init__(self):
        '''
        create an instance of the Clerk_House_Gov class
        
        Args:
            None
            
        Returns:
            <cva.collector.web.Clerk_House_Gov>: instance of the class
            
        Raises:
            N/A
        '''
        super().__init__()
        self._url_template = 'https://clerk.house.gov/evs/{year}/roll{vote}.xml'
        
    def yield_urls(self, st_year=1993, ed_year=2021, st_vote=1, ed_vote=999):
        '''
        create a generator to yield possible URLs for https://clerk.house.gov/
        
        Args:
            <int> st_year(1993): year to start collection
            <int> ed_year(2021): year to stop collection
            <st_vote>(1): vote to start collection at
            <ed_vote>(999): vote to stop collection at
            
        Returns:
            <generator>: generator with 3 items
                [0] <str>: URL
                [1] <int>: year collection is from
                [2] <str>: vote number as 0 padded string
                
        Raises:
            N/A
        '''
        #for the range of years requested(inclusive)
        for i in range(st_year, ed_year+1):
            self.log(
                    'cva.collector.web.Clerk_Hose_Gov.yield_urls.Info'
                    , f'Starting Collection for year:{i}')
            #for range of votes requested(inclusive)
            for j in range(st_vote, ed_vote+1):
                #url for House URLs formatted like 001 for vote 1
                ##so using format to add leading zeros as needed
                vote_str = '{0:03}'.format(j)
                url_params = {'year':i, 'vote':vote_str}
                #build url and yield data
                url = self.build_url(self._url_template, url_params)
                yield url, i, vote_str
                
    def download_xml(self, url_generator, output_folder, rate_limit=1):
        '''
        attempt to download raw data(XML) for a range of
        URLs generated by .yield_urls()
        
        Args:
            <generator> url_generator: generator yielded by .yield_urls()
            <str> output_folder: folder to write raw data to
            <int> rate_limit(1): second(s) to wait to be nice to webiste(and not get IP blocked)
            
        Returns:
            None
            
        Raises:
            N/A
        '''
        #for every item in the generator
        for item in url_generator:
            #unpack the tuple that's yielded
            url, year, vote = item
            #build output file name based on metadata
            output_file = f'{output_folder}/house_{year}_{vote}.xml'
            self.log(
                    'cva.collector.web.Clerk_House_Gov.download_xml.Info'
                    , f'Attempting Collection for {url}')
            xml = self.download_content(url)
            time.sleep(rate_limit)
            #if xml was returned(valid URL) write file and log
            if xml:
                self.write_file(output_file, xml)
                self.log(
                        'cva.collector.web.Clerk_House_Gov.download_xml.Info'
                        , f'Data Saved to {output_file}')
                
class Senate_Gov(Web):
    '''
    data found at https://www.congress.gov/roll-call-votes
    download Senate data from https://senate.gov/
    
    Attributes:
        <str> _log_file: location of log file(from cva.core.Core)
        <str> _url_template: base URL to download raw data
    '''
    def __init__(self):
        '''
        create an instance of the Senate_Gov class
        
        Args:
            None
            
        Returns:
            <cva.collector.web.Senate_Gov>: instance of the class
            
        Raises:
            N/A
        '''
        super().__init__()
        self._url_template = 'https://www.senate.gov/legislative/LIS/roll_call_votes/vote{order}{session}/vote_{order}_{session}_{vote}.xml'
        
    def yield_urls(self, st_order=101, ed_order=117, st_vote=1, ed_vote=999, st_session=1, ed_session=2):
        '''
        create a generator to yield possible urls for https://senate.gov/
        
        Args:
            <int> st_order(101): number of the senate sworn in(the 101st sentate) to start with
            <int> ed_order(117): number of the senate sworn in to end with
            <int> st_vote(1): vote to start collection at
            <int> ed_vote(999): vote to end collection at
            <int> st_session(1): session to start collection at
            <int> ed_session(2): session to end collection at
                Note: the only vaild session numbers are 1 and 2
                
        Returns:
            <generator>: yields a generator with 2 items
                [0] <str>: URL
                [1] <dict>: paramerters used to build the url
                
        Raises:
            N/A
        '''
        #for every "Senate" sworn in
        for i in range(st_order, ed_order+1):
            #for every senate session(should always be 1 or 2)
            for j in range(st_session, ed_session+1):
                #for every vote cast
                for k in range(st_vote, ed_vote+1):
                    #add leading zeros to the vote number to match their url format
                    vote_str = '{0:05}'.format(k)
                    #set params and build a url using the template
                    params = {'order':i, 'session':j, 'vote':vote_str}
                    url = self.build_url(self._url_template, params)
                    #yield the built url and paramerters used
                    yield url, params
                    
    def download_xml(self, url_generator, output_folder, rate_limit=1):
        '''
        attempt to download raw data(XML) for a range of
        URLs generated by .yield_urls()
        
        Args:
            <generator> url_generator: generator yielded by .yield_urls()
            <str> output_folder: folder to write raw data to
            <int> rate_limit(1): second(s) to wait to be nice to webiste(and not get IP blocked)
            
        Returns:
            None
            
        Raises:
            N/A
        '''
        #for all URLs passed...
        for item in url_generator:
            #unpack url / params from generator
            url, params = item
            order = params['order']
            session = params['session']
            vote = params['vote']
            #generate a file name based on paramerters
            output_file = f'{output_folder}/senate_{order}_{session}_{vote}.xml'
            self.log(
                    'cva.collector.web.Senate_Gov.download_xml.Info'
                    , f'Attempting Collection for {url}')
            #attempt to download content given the url
            xml = self.download_content(url)
            time.sleep(rate_limit)
            #if we were able to get content write it to a file
            if xml:
                self.write_file(output_file, xml)
                self.log(
                        'cva.collector.web.Senate_Gov.download_xml.Info'
                        , f'Data Saved to {output_file}')

    
def main():
    #vars...
    output = r'C:\Users\Scott\Desktop\congressional-vote-analysis\data'
    
    #run...
    ##Example 1: collect from House
    ###chg = Clerk_House_Gov()
    ###gen = chg.yield_urls(st_year=2017)
    ###chg.download_xml(gen, output)
    
    ##Example 2: collect from Senate
    sg = Senate_Gov()
    gen = sg.yield_urls()
    sg.download_xml(gen, output)

if __name__ == '__main__':
    main()