# pyRAT - interface for Mad Catz R.A.T. 7

![pyRAT](res/pyRAT.png "pyRAT")

pyRAT is a tool which incorporates all features of the communication with a Mad Catz (Cyborg) R.A.T.7.

```
$ sudo python pyRAT.py -h

usage: pyRAT.py [-h] [--setdev Vendor Product]
                [--setdpi MODE X Y | --getdpi MODE | --setmode MODE]

pyRAT supports all features of a R.A.T.7. By Dennis Leroy Wigand

optional arguments:
  -h, --help            show this help message and exit
  --setdev Vendor Product
                        Uses the vendor and product info to find the R.A.T.7
                        device.
  --setdpi MODE X Y     Sets the DPI for a desired MODE in X and Y direction.
                        [0-255]
  --getdpi MODE         Gets the DPI for a desired MODE in X and Y direction.
  --setmode MODE        Sets the active dpi mode. [1-4]
```

## R.A.T.7's Protocol

Lorem Ipsum

#### Change Active DPI Mode

Modes 1 2 3 4
![Visualization of the modes](https://rawgit.com/xwavex/pyRAT/master/res/pSide.svg)

|  Mode |    1   |    2   |    3   |    4   |
|:-----:|:------:|:------:|:------:|:------:|
| value | 0x1000 | 0x2000 | 0x3000 | 0x4000 |

##### Read active DPI Mode

|     command    | value |information|
|:--------------:|:-----:|----------------------------|
|      type      |  0xC0 |                            |
|     request    |  0x90 |                            |
|      value     |  0x0  |                            |
|      index     |  0x74 |                            |
|      size      |  0x1  |                            |
| ioBuffer[size] |       |will contain the active mode|

python snippet:
```javascript
ioBuffer = dev.ctrl_transfer(0xC0, 0x90, 0, 0x74, 1)
```
c++ snippet:
```javascript
err = libusb_control_transfer(handle, 0xC0, 0x90, 0x0, 0x74, ioBuffer, 0x1);
```

##### Write active DPI Mode

|     command    |  value   |         information           |
|:--------------:|:--------:|-------------------------------|
|      type      |   0x40   |                               |
|     request    |   0x91   |                               |
|      value     |   0x1000 | choose from modes table above |
|      index     |   0x74   |                               |
|      size      |   0x0    |                               |

python snippet:
```javascript
ioBuffer = dev.ctrl_transfer(0x40, 0x91, 0x1000, 0x74, [])
```
c++ snippet:
```javascript
err = libusb_control_transfer(handle, 0x40, 0x91, 0x1000, 0x74, 0, 0x1);
```
