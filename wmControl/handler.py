from scpiparser.CommandInterpreter import CommandInterpreter
from scpiparser.CommandHandler import CommandHandler
from scpiparser.QueryHandler import QueryHandler

# Erst überlegen ob Messung läuft, dann starten.

class SwitchingHandler(QueryHandler,CommandHandler):
    def __init__(self):
        self.value = 0

    def query(self,program_header):
        return str(self.value)

    def set(self,program_header,program_data):
        if not isinstance(program_data, float):
            raise TypeError('Number between 0 and 8 expected.')
        elif program_data>-1 and program_data<9:
            self.value=program_data
        else: raise ValueError('Given channel number not exisiting.')
        return "Ok"

class IPHandler(QueryHandler,CommandHandler):
    def __init__(self):
        self.value = "195.168.1.45"

    def query(self,program_header):
        return str(self.value)

    def set(self,program_header,program_data):
        self.value=program_data
        return "Ok"

#ci = CommandInterpreter(manufacturer='HighFinesse',model='WS8',serial='4734',firmware_version='0.1')

#sh = SwitchingHandler()
#iph = IPHandler()

#ci.register_query_handler("CHANNEL:SWITCH",sh)
#ci.register_command_handler("CHANNEL:SWITCH",sh)
#ci.register_query_handler("CONTROLpc:IP",iph)
#ci.register_command_handler("CONTROLpc:IP",iph)

#print(ci.process_line("*IDN?"))
#print(ci.process_line("CHANNEL:SWITCH?"))
#print(ci.process_line("CHANNEL:SWITCH 8"))
#print(ci.process_line("CHANNEL:SWITCH?"))
#print(ci.process_line("CONTROL:IP?"))
#print(ci.process_line("CONTROL:IP \'195.168.1.240\'"))
#print(ci.process_line("CONTROL:IP?"))
