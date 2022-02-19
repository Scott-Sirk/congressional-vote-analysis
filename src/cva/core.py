
from datetime import datetime
import os

class Core():
    '''
    core class with basic finctionality used by many child classes
    
    Attributes:
        <str> _log_file: file written to by the .log() method
    '''
    def __init__(self, log_file=''):
        '''
        make an instace of the cva.core.Core class
        
        Args:
            <str> log_file(''): file written to by the .log() method
                defaults to <current-working-directory>/cva.log
                
        Returns:
            <cva.core.Core>: instance of the class
            
        Raises:
            N/A
        '''
        if not log_file:
            log_file = os.getcwd() + '/cva.log'
        self._log_file = log_file
    
    def log(self, mode, msg):
        '''
        write a message to the _log_file
        
        Args:
            <str> mode: what type of message is being logged
                generally I do <class-path>.<description>
                so something like cva.core.Core.Warning for a warning
                But it can be anything so long as it's descriptive
            <str> msg: log message
            
        Returns:
            None
            
        Raises:
            N/A
        '''
        ts = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        string = f'{ts}|{mode}|{msg}\n'
        with open(self._log_file, 'a') as f:
            f.write(string)
    
    def write_file(self, file, content, encoding='utf-8'):
        '''
        write a file(mainly done for consistent encoding)
        
        Args:
            <str> file: path to file to write
            <str> content: data to write to the file
            <str> enconding('utf-8'): encoding to use
                defaults to utf-8
                
        Returns:
            None
            
        Raises:
            N/A
        '''
        with open(file, 'w', encoding=encoding) as out:
            out.write(content)
    
def main():
    pass

if __name__ == '__main__':
    main()