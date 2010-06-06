# -*- coding: utf-8 -*-
# Copyrigth 2010 Omar Andres Zapata Mesa
# Copyrigth 2010 Fernando Perez

import __builtin__
from contextlib import nested

from IPython.core.iplib import InteractiveShell
from IPython.utils import session
from IPython.core import completer
from IPython.core import ultratb
from IPython.utils.traitlets import (
    Int, Str, CBool, CaselessStrEnum, Enum, List, Unicode
)

class InteractiveShellFrontend(InteractiveShell):
   def __init__(self,locals=None, filename="<console>", session = session, request_socket=None, subscribe_socket=None):
       InteractiveShell.__init__(self)
       self.shell=InteractiveShell()
       self.display_banner = CBool(False)
       #self._completer=completer.ClientCompleter(None,session,request_socket)
       #self.set_custom_completer(self._completer)
       
       
   def request(self,message):
       pass
    
   def run(self):
        """Closely emulate the interactive Python console."""

        # batch run -> do not interact        
        if self.exit_now:
            return

        #if self.display_banner is None:
        #    display_banner = self.display_banner
        #if display_banner:
        #    self.show_banner()

        more = 0
        
        if self.has_readline:
            self.readline_startup_hook(self.pre_readline)
        # exit_now is set by a call to %Exit or %Quit, through the
        # ask_exit callback.
        
        while not self.exit_now:
            buffer=[]
            self.hooks.pre_prompt_hook()
            if more:
                try:
                    prompt = self.hooks.generate_prompt(True)
                except:
                    self.showtraceback()
                if self.autoindent:
                    self.rl_do_indent = True
                    
            else:
                try:
                    prompt = self.hooks.generate_prompt(False)
                except:
                    self.showtraceback()
            try:
                line = self.raw_input(prompt, more)
                buffer.append(line)
                if self.exit_now:
                    # quick exit on sys.std[in|out] close
                    break
                if self.autoindent:
                    self.rl_do_indent = False
                    
            except KeyboardInterrupt:
                #double-guard against keyboardinterrupts during kbdint handling
                try:
                    self.write('\nKeyboardInterrupt\n')
                    self.resetbuffer()
                    # keep cache in sync with the prompt counter:
                    self.outputcache.prompt_count -= 1
    
                    if self.autoindent:
                        self.indent_current_nsp = 0
                    more = 0
                except KeyboardInterrupt:
                    pass
            except EOFError:
                if self.autoindent:
                    self.rl_do_indent = False
                    if self.has_readline:
                        self.readline_startup_hook(None)
                self.write('\n')
                self.exit()
            except bdb.BdbQuit:
                warn('The Python debugger has exited with a BdbQuit exception.\n'
                     'Because of how pdb handles the stack, it is impossible\n'
                     'for IPython to properly format this particular exception.\n'
                     'IPython will resume normal operation.')
            except:
                # exceptions here are VERY RARE, but they can be triggered
                # asynchronously by signal handlers, for example.
                self.showtraceback()
            print buffer
              
        # We are off again...
        #__builtin__.__dict__['__IPYTHON__active'] -= 1

        # Turn off the exit flag, so the mainloop can be restarted if desired
        self.exit_now = False

    
      
if __name__ == "__main__" :
    frontend=InteractiveShellFrontend()
    frontend.run()