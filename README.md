Persian NLP
===========

Use [Virastyar] (http://sourceforge.net/projects/virastyar/) on python

<img src="http://virastyar.ir/themes/virtheme/images/virastyar.png">

## Install [Mono] (http://www.mono-project.com/‎)

for basic installation of **Mono**, use below instruction:

```bash
sudo apt-get install mono-runtime
```

for full installation of **Mono**, use below instruction:

```bash
sudo apt-get install mono-complete
```

<hr />

## Install [IronPython] (http://ironpython.net/)

* Note: if you use basic installation of **Mono**, you should install all **IronPython**'s dependencies manually.

for install all dependencies, use below instructions:

```bash
sudo apt-get install libmono-corlib2.0-cil

sudo apt-get install libmono-system2.0-cil

sudo apt-get install libmono-system-runtime2.0-cil

sudo apt-get install libmono-winforms2.0-cil
```

there is one more dependency that is not possible use **apt-get** to install it, you should download **libdlr0.9-cil** from below link:
```
http://packages.ubuntu.com/lucid/libdlr0.9-cil
```

for installing `.deb` package manually, use below instruction:

```bash
sudo dpkg -i PACKAGE_NAME.deb
```

download **IronPython**, from below link:

```
http://packages.ubuntu.com/lucid/all/ironpython/download
```

for installing `.deb` package manually, use below instruction:

```bash
sudo dpkg -i PACKAGE_NAME.deb
```

<hr />

## Example

for run sample code `test.py`, you should use below instruction:

```bash
ipy test.py
```

here is a example for using **Virastyar** DLLs within python:

```python
import clr

# loading the DLL
clr.AddReference("/home/user/virastyar/Bin/SCICT.PersianTools.dll")
                                                                                                                                                                                                                                                                                                    
from SCICT.NLP.Utility.Parsers import ParsingUtils

str = "123,456.78"
result = ParsingUtils.ConvertNumber2Persian(str)

print result.ToString()
```
<hr />

### License

[Virastyar] (http://virastyar.ir/).
