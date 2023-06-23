# wmControl
WM HighFinesse WS8 control via ethernet

# Plains

* Netaccess-plain: Communicates with WMs on the control PC, wlm... files and the wlmDataServer.exe are dedicated to this plain
* Control-plain: Wraps user friendly functionality around the HighFinesse offered solution: control.wavemeter(Version).do_something()
* Stephan-plain (client-side): Requests from a user-PC to the control-plain, not yet implemented
        
# Netaccess-Plain
* On the WM-PC the wlmDataServer.exe needs to be installed.
* The wlmData.ini holds the IP-Adress of the instrument server. In this case the IP of the control PC.
* The control-plain communicates via the wlmData.dll with the NetAccess-Server.

# Control-Plain
* In module control wavemeters are initialized with their version-number. When the user wants to measure_something a object of thread.callback is initialized.
   * version number....
   * Setters of the wavemeter are not threaded.
* At initialisation of thread.callback the version attribute of callback is set. This used to get something from a specific wavemeter.

# Stephan-plain (client-side)
* There is (will be) a secondary server implemented, wich handels the requests of user PC.
   * The request are of structur control.wavemeter(Version).do_something()
