:: Start the wavemeter programs.
cd "C:\Program Files (x86)\HighFinesse\Wavelength Meter WS6 536"
Start wlm_ws6.exe
cd "C:\Program Files (x86)\HighFinesse\Wavelength Meter WS8 4711"
Start wlm_ws8.exe

:: Go to the dictionary where your environment is.
cd C:\Users\apq_hifines\pbaus\wmControl
:: Activate the environment.
call env\Scripts\activate
:: Execute the server.py in python.
python3 server.py
