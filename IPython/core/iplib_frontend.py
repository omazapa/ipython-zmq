# -*- coding: utf-8 -*-
# Copyrigth 2010 Omar Andres Zapata Mesa
# Copyrigth 2010 Fernando Perez

import __builtin__
from contextlib import nested
import time
import readline

from IPython.core.iplib import InteractiveShell
from IPython.utils import session
from IPython.core import completer
from IPython.core import ultratb
from IPython.utils.traitlets import (
    Int, Str, CBool, CaselessStrEnum, Enum, List, Unicode
)

class InteractiveShellFrontend(InteractiveShell):
   def __init__(self,filename="<console>", session = session, request_socket=None, subscribe_socket=None):
       InteractiveShell.__init__(self)
       self.buffer_lines=[]
       #self.shell=InteractiveShell()
       #self.display_banner = CBool(False)
       
       #self.completer=completer.ClientCompleter(self,session,request_socket)
       #self.set_custom_completer(self.completer)
       #self.set_completer()
       
       #readline.parse_and_bind('tab: complete')
       #readline.parse_and_bind('set show-all-if-ambiguous on')
       #readline.set_completer(self.completer.complete)
       #self.set_custom_completer(self.completer.complete,0)
#       self.handlers = {}
#       for msg_type in ['pyin', 'pyout', 'pyerr', 'stream']:
#           self.handlers[msg_type] = getattr(self, 'handle_%s' % msg_type)
#       self.session = session
#       self.request_socket = request_socket
#       self.sub_socket = subscribe_socket
#       self.backgrounded = 0
#       self.messages = {}
   
   def test_push_line(self,line):
       for subline in line.splitlines():
            self._autoindent_update(subline)
       self.buffer_lines.append(line)
       more = self.test_runsource('\n'.join(self.buffer_lines), self.filename)
       if not more:
           self.resetbuffer()
       return more
   
   def test_runsource(self, source, filename='<input>', symbol='single'):
       source=source.encode(self.stdin_encoding)
       if source[:1] in [' ', '\t']:
           source = 'if 1:\n%s' % source
       try:
           code = self.compile(source,filename,symbol)
       except (OverflowError, SyntaxError, ValueError, TypeError, MemoryError):
            # Case 1
           self.showsyntaxerror(filename)
           return None

       if code is None:
            # Case 2
           return True
       else:
           self.buffer_lines[:]=[]
           return False
    
   def prompt(self):
        """Closely emulate the interactive Python console."""

        # batch run -> do not interact        
        if self.exit_now:
            return

        #if self.display_banner is None:
        #    display_banner = self.display_banner
        #if display_banner:
        #    self.show_banner()

        more = 0
        #__builtin__.__dict__['__IPYTHON__active'] += 1
         
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
            else:
                more = self.test_push_line(line)
                if (self.SyntaxTB.last_syntax_error and
                    self.autoedit_syntax):
                    self.edit_syntax_error()
            #print buffer    
            #self.runcode(buffer)
              
        # We are off again...
        #__builtin__.__dict__['__IPYTHON__active'] -= 1

        # Turn off the exit flag, so the mainloop can be restarted if desired
        self.exit_now = False
        
#   def handle_pyin(self, omsg):
#       if omsg.parent_header.session == self.session.session:
#            return
#       c = omsg.content.code.rstrip()
#       if c:
#           print '[IN from %s]' % omsg.parent_header.username
#           print c
#   def handle_pyout(self, omsg):
#       #print omsg # dbg
#       if omsg.parent_header.session == self.session.session:
#           print "%s%s" % (sys.ps3, omsg.content.data)
#       else:
#           print '[Out from %s]' % omsg.parent_header.username
#           print omsg.content.data
#   def print_pyerr(self, err):
#       print >> sys.stderr, err.etype,':', err.evalue
#       print >> sys.stderr, ''.join(err.traceback)       
#    
#   def handle_pyerr(self, omsg):
#       if omsg.parent_header.session == self.session.session:
#           return
#       print >> sys.stderr, '[ERR from %s]' % omsg.parent_header.username
#       self.print_pyerr(omsg.content)
#       
#   def handle_stream(self, omsg):
#       if omsg.content.name == 'stdout':
#           outstream = sys.stdout
#       else:
#           outstream = sys.stderr
#           print >> outstream, '*ERR*',
#           print >> outstream, omsg.content.data,
#
#   def handle_output(self, omsg):
#        handler = self.handlers.get(omsg.msg_type, None)
#        if handler is not None:
#            handler(omsg)
#
#   def recv_output(self):
#        while True:
#            omsg = self.session.recv(self.sub_socket)
#            if omsg is None:
#                break
#            self.handle_output(omsg)
#
#   def handle_reply(self, rep):
#        # Handle any side effects on output channels
#        self.recv_output()
#        # Now, dispatch on the possible reply types we must handle
#        if rep is None:
#            return
#        if rep.content.status == 'error':
#            self.print_pyerr(rep.content)            
#        elif rep.content.status == 'aborted':
#            print >> sys.stderr, "ERROR: ABORTED"
#            ab = self.messages[rep.parent_header.msg_id].content
#            if 'code' in ab:
#                print >> sys.stderr, ab.code
#            else:
#                print >> sys.stderr, ab
#
#   def recv_reply(self):
#        rep = self.session.recv(self.request_socket)
#        self.handle_reply(rep)
#        return rep
#
#   def runcode(self, code):
#       # We can't pickle code objects, so fetch the actual source
#       src = '\n'.join(self.buffer)
#       # for non-background inputs, if we do have previoiusly backgrounded
#       # jobs, check to see if they've produced results
#       if not src.endswith(';'):
#           while self.backgrounded > 0:
#               #print 'checking background'
#               rep = self.recv_reply()
#               if rep:
#                   self.backgrounded -= 1
#               time.sleep(0.05)
#       # Send code execution message to kernel
#       omsg = self.session.send(self.request_socket,
#                                 'execute_request', dict(code=src))
#       self.messages[omsg.header.msg_id] = omsg
#        
#        # Fake asynchronicity by letting the user put ';' at the end of the line
#       if src.endswith(';'):
#           self.backgrounded += 1
#           return
#
#        # For foreground jobs, wait for reply
#       while True:
#           rep = self.recv_reply()
#           if rep is not None:
#               break
#           self.recv_output()
#           time.sleep(0.05)
#       else:
#           # We exited without hearing back from the kernel!
#           print >> sys.stderr, 'ERROR!!! kernel never got back to us!!!'
#    
      
if __name__ == "__main__" :
    # Defaults
    #ip = '192.168.2.109'
    import zmq
    ip = '127.0.0.1'
    #ip = '99.146.222.252'
    port_base = 5555
    connection = ('tcp://%s' % ip) + ':%i'
    req_conn = connection % port_base
    sub_conn = connection % (port_base+1)
    
    # Create initial sockets
    c = zmq.Context()
    request_socket = c.socket(zmq.XREQ)
    request_socket.connect(req_conn)
    
    sub_socket = c.socket(zmq.SUB)
    sub_socket.connect(sub_conn)
    sub_socket.setsockopt(zmq.SUBSCRIBE, '')

    # Make session and user-facing client
    sess = session.Session()
    
    frontend=InteractiveShellFrontend('<zmq-console>',sess,request_socket=request_socket,subscribe_socket=sub_socket)
    frontend.prompt()