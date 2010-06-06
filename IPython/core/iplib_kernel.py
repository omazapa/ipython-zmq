# -*- coding: utf-8 -*-
import sys
from IPython.utils.session import Session, Message, extract_header
from IPython.utils import session
from IPython.core.completer import KernelCompleter
from IPython.core.iplib import InteractiveShell
from IPython.core import ultratb
import traceback
import __builtin__
class DisplayHook(object):

    def __init__(self):
        self._object=""
    def __call__(self, obj):
        if obj is None:
            return
        print "hola"
        self._object=obj
        __builtin__._ = obj
        
    def get_obj(self):
        return self._object

class StdOut:
    def __init__(self):
        self._stdout=[]
    def __call__(self, obj):
        if obj is None:
            return
        __builtin__._ = obj
        self._stdout=obj   
    def write(self,message):
        self._stdout.append(message)
        
    def get_output(self):
        return self._stdout

class InteractiveShellKernel(InteractiveShell):
    def __init__(self,input_queue=None,output_queue=None):
        InteractiveShell.__init__(self)
        self._input_queue=input_queue
        self._output_queue=output_queue
        self._stdout=sys.stdout
        self._stderr=sys.stderr
        self._hook=StdOut()
        sys.excepthook = ultratb.ColorTB()
        sys.excepthook = ultratb.VerboseTB()
        self.ftb=ultratb.FormattedTB()
    def send_message(message):
        self._output_queue.put(message) 


    def get_message():
        return self._input_queue.get()
    
    def start(self):
        msg_id=0
        while True:
            msg=raw_input("In [%i]"%msg_id)
            try:                
                #sys.stdout=StdOut()
                #sys.stderr=StdOut()
                for type in ['editor', 'fix_error_editor', 'synchronize_with_editor', 'result_display', 'input_prefilter', 'shutdown_hook', 'late_startup_hook', 'generate_prompt', 'generate_output_prompt', 'shell_hook', 'show_in_pager', 'pre_prompt_hook', 'pre_runcode_hook', 'clipboard_get']:
                    self.set_hook(type, self._hook)
                self.runlines(msg)
            except:
                etype, evalue, tb = sys.exc_info()
                tb = traceback.format_exception(etype, evalue, tb)
                exc_content = {
                    u'status' : u'error',
                    u'traceback' : tb,
                    u'etype' : unicode(etype),
                    u'evalue' : unicode(evalue)
                    }
                session=Session()
                exc_msg = session.msg(u'pyerr', exc_content,{})
                #sys.stderr=self._stderr
                #sys.stdout=self._stdout
                print "traceback captured"
                                
                #self.set_custom_exc((etype, evalue, tb),None)
                #self.excepthook(etype, evalue, tb)
                self.ftb.text(etype, evalue, tb)
                
                #self.showtraceback((etype,evalue,tb),"<ipython console>",0)
                
              #  for index in exc_content:
               #     if index == "traceback" :
                #        for value in exc_content[index]:
                 #           print value
                  #  else:
                   #     print index," = ", exc_content[index]        
            msg_id=msg_id+1
        
if __name__ == "__main__" :
    kernel=InteractiveShellKernel()
    kernel.start()        