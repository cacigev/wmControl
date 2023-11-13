![Tests](../../actions/workflows/pytest.yml/badge.svg)
[![code style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](LICENSE)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=flat&logo=docker&logoColor=white)
# wmControl
Wavemeter HighFinesse WS8 control via ethernet.

Creates a host which serves for every connected wavemeter. It uses SCPI for communication with the wavemeters.
```
import asyncio


request = "MEASURE:WAVELENGTH (@1,2)\n"  # SCPI-command
reader, writer = await asyncio.open_connection(interface, port)  # Interface and port of wavemeter server.
await writer.write(request.encode())
await writer.drain()

wave_1 = await reader.readline().decode().rstrip()
print("Wavelength channel 1: ", wave_1)
wave_2 = await reader.readline().decode().rstrip()
print("Wavelength channel 2: ", wave_2)
```

# Installation instructions
## Linux
```
python3 -m venv env  # Create a virtual environment for the build tools
pip install -r requirements.txt
pre-commit install
```

## Windows
```
conda install pip
pip install -r requirements.txt
pre-commit install
```
To configure the host use a *.env*-file. Within it, a wavemeter is represented by a list of the version of the wavemeter,
the IP-address or interface of the host and a port of the host. You can also use a *.bat*-file to automate the host.

An example for both is shown in the example dictionary. 

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](../../tags).

## Authors

* **Simon Schultheis** - *Initial work* - [cacigev](https://github.com/cacigev)
* Patrick Baus - [PatrickBaus](https://github.com/PatrickBaus)

## License


This project is licensed under the GPL v3 license - see the [LICENSE](LICENSE) file for details
