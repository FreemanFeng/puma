# -*- coding:utf-8 -*-
'''
This Class is to register event
'''
from MBase import MBase
from handle_exception import handle_exception

class Event(MBase):
    '''
    Event class, derived from MBase to run multi instance
    '''
    (PENDING, FINISHED) = (0, 1)
    def __init__(self, *args, **kargs):
        '''
        initialize event instance
        '''
        super(Event, self).__init__()
        # -------------------------------------------------
        #    ******** name ********
        # event name is used to find handler module
        # -------------------------------------------------
        self.name       = None

        # -------------------------------------------------
        #    ******** handler ********
        # handler is used to handle event
        # -------------------------------------------------
        self.handler    = None

        # -------------------------------------------------
        #    ******** data ********
        # event config data
        # -------------------------------------------------
        self.data       = None

        # -------------------------------------------------
        #    ******** params ********
        # params transmit sender's data to event handler
        # -------------------------------------------------
        self.params     = dict()

        # -------------------------------------------------
        #    ******** level ********
        # level limit in which level event could be handled
        # 0: top level, could be omitted
        # 1 ... n (n < 900): specific level
        # 998: check media, special use for hummer
        # 999: force handling, used for set_events handler
        # -------------------------------------------------
        self.level      = None

        # -------------------------------------------------
        #    ******** status ********
        # status record event handling is finished or not
        # -------------------------------------------------
        self.status     = None

        # -------------------------------------------------
        #    ******** result ********
        # event handling result for sender's next action
        # -------------------------------------------------
        self.result     = dict()

    @handle_exception
    def done(self):
        '''
        set event to be done
        '''
        self.status = Event.FINISHED

    @handle_exception
    def init(self):
        '''
        reset event status
        '''
        self.status = Event.PENDING
        self.result = dict()

    @handle_exception
    def is_done(self):
        '''
        set event to be done
        '''
        return 0 if not self.status else 1
