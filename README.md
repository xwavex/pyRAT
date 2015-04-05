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

<img src="data:image/svg+xml;base64,PHN2ZyB4bWxucz0naHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmcnIHdpZHRoPSczMCcgaGVpZ2h0PSczMCc+PGNpcmNsZSBjeD0nMTUnIGN5PScxNScgcj0nMTAnIC8+PC9zdmc+" />
