#!/usr/bin/python
#
# pyRAT is a tool which incorporates all features of
# the communication with a MadCatz R.A.T.7.
# This reverse engineered collection of functionality
# should later work as an inspiration or rather interface
# for a real driver.
#
# by Dennis Leroy Wigand (xwavedw@gmail.com)
#
#
import usb.core
import usb.util
import sys
import time
import argparse

class pyRAT:

    def pyRAT_claim_device(self, dev, interface):
        # detach and claim the device from the OS kernel
        if dev.is_kernel_driver_active(interface) is True:
            # detach
            dev.detach_kernel_driver(interface)
            # claim
            usb.util.claim_interface(dev, interface)

    def pyRAT_release_device(self, dev, interface):
        # release the device
        usb.util.release_interface(dev, interface)
        # reattach the device to the OS kernel
        dev.attach_kernel_driver(interface)

    def pyRAT_get_active_dpi_mode(self, dev):
        mode = -1
        try:
            ret = dev.ctrl_transfer(0xC0, 0x90, 0, int('0x74', 16), 1)
            if ret[0] is 16:
                mode = 1
            elif ret[0] is 32:
                mode = 2
            elif ret[0] is 48:
                mode = 3
            elif ret[0] is 64:
                mode = 4
            time.sleep(0.1)
        except:
            print("Error: reading active dpi mode failed!")
        return mode


    def pyRAT_getDPI_XY(self, dev, mode):
        try:
            retX = dev.ctrl_transfer(0xC0, 0x90, 0, int('0x'+str(mode)+'1'+'73', 16), 2) # get dpi for mode 4 axis 1
            time.sleep(0.1)
            retY = dev.ctrl_transfer(0xC0, 0x90, 0, int('0x'+str(mode)+'2'+'73', 16), 2) # get dpi for mode 4 axis 1
            time.sleep(0.1)
            dpiX = retX[1]
            dpiY = retY[1]
            return [dpiX,dpiY]
        except:
            print("Error: reading dpi values for mode %s failed!"%(str(mode)))
            return None

    def pyRAT_setDPI_XY(self, dev, mode, x, y):
        try:
            print("Setting DPI for mode %s on axis %s to %s hex"%(str(mode),'1',str(x)))
            ret = dev.ctrl_transfer(0x40, 0x91, int('0x'+str(mode)+'1'+str(x), 16), 0x73, [])
            print("...ret: %s"%(ret is 0 and "OK" or ret))
            time.sleep(0.3)
            print("Setting DPI for mode %s on axis %s to %s hex"%(str(mode),'2',str(y)))
            ret = dev.ctrl_transfer(0x40, 0x91, int('0x'+str(mode)+'2'+str(y), 16), 0x73, [])
            print("...ret: %s"%(ret is 0 and "OK" or ret))
            time.sleep(0.3)
            print("Confirm new DPI setting")
            ret = dev.ctrl_transfer(0x40, 0x91, 0x51, 0x70, []) # confirm!
            print("...ret: %s"%(ret is 0 and "OK" or ret))
            time.sleep(0.3)
            return True
        except:
            print("Error: setting dpi values for mode %s failed! (x: %s, y: %s)"%(str(mode), str(x), str(y)))
            return False

    def pyRAT_resetDPI(self, dev):
        try:
            print("Reset the DPI settings")
            ret = dev.ctrl_transfer(0x40, 0x91, 0x0, 0x73, [])
            print("...ret: %s"%(ret is 0 and "OK" or ret))
            time.sleep(0.3)
            print("Confirm reset of DPI settings")
            ret = dev.ctrl_transfer(0x40, 0x91, 0x51, 0x70, []) # confirm!
            print("...ret: %s"%(ret is 0 and "OK" or ret))
            time.sleep(0.3)
            return True
        except:
            print("Error: resetting dpi values failed!")
            return False

    def pyRAT_set_active_dpi_mode(self, dev, mode):
        try:
            realMode = 0x1000
            if mode is 1:
                realMode = 0x1000
            elif mode is 2:
                realMode = 0x2000
            elif mode is 3:
                realMode = 0x3000
            elif mode is 4:
                realMode = 0x4000
            else:
                print("Error: wrong DPI mode (%s) selected!"%(str(mode)))
                return False

            print("Activating DPI mode %s"%(str(mode)))
            ret = dev.ctrl_transfer(0x40, 0x91, realMode, 0x74, [])
            print("...ret: %s"%(ret is 0 and "OK" or ret))
            time.sleep(0.2)
            return True
        except:
            print("Error: activating dpi mode %s failed!"%(str(mode)))
            return False


    def __init__(self):
        # parse args
        parser = argparse.ArgumentParser(description='pyRAT supports all features of a R.A.T.7. By Dennis Leroy Wigand')
        parser.add_argument('--setdev', metavar=('Vendor','Product'), type=str, nargs=2, default=['1848','5896'],
                           help='Uses the vendor and product info to find the R.A.T.7 device.', required=False)
        # make both args mutual exclusive
        group = parser.add_mutually_exclusive_group()
        group.add_argument('--setdpi', metavar=('MODE','X','Y'), type=str, nargs=3,action='store',
                           help='Sets the DPI for a desired MODE in X and Y direction. [0-255]',required=False)
        group.add_argument('--getdpi', metavar='MODE', type=str, nargs=1,action='store',
                           help='Gets the DPI for a desired MODE in X and Y direction.',required=False)
        group.add_argument('--setmode', metavar='MODE', type=int, nargs=1,action='store',
                           help='Sets the active dpi mode. [1-4]',required=False)
        args = parser.parse_args()

        desiredMode = 'ALL'

        if args.getdpi:
            desiredMode = args.getdpi[0]

        # find our R.A.T.7 device
        dev = usb.core.find(idVendor=1848, idProduct=5896)

        if not dev:
            print("Error: R.A.T.7 not found! (used VendorId: %s and ProductId: %s)"%(args.setdev[0], args.setdev[1]))
            sys.exit(1)
        else:
            print("Found a R.A.T.7! (used VendorId: %s and ProductId: %s)"%(args.setdev[0], args.setdev[1]))

        # sets up the interface and endpoint for connection
        interface = 0
        endpoint = dev[0][(0,0)][0]

        self.pyRAT_claim_device(dev, interface)

        if desiredMode is 'ALL' and not args.setdpi and not args.setmode:
            print("\nActive DPI mode: %s"%(self.pyRAT_get_active_dpi_mode(dev)))
            print("\nDPI Settings:\n")
            for i in range(1, 5):
                xy = self.pyRAT_getDPI_XY(dev, i)
                print("\tMode %s\t X: %s\t Y: %s"%(i, xy[0], xy[1]))
            print("\n\n by Dennis Leroy Wigand (xwavedw@gmail.com)\n")

        elif desiredMode is not 'ALL':
            xy = self.pyRAT_getDPI_XY(dev, desiredMode)
            print("\n\tMode %s\t X: %s\t Y: %s\n"%(desiredMode, xy[0], xy[1]))

        elif args.setdpi:
            self.pyRAT_setDPI_XY(dev, args.setdpi[0], hex(int(args.setdpi[1]))[2:], hex(int(args.setdpi[2]))[2:])
            xy = self.pyRAT_getDPI_XY(dev, args.setdpi[0])
            print("\nCheck new DPI settings:")
            print("Mode %s\t X: %s\t Y: %s\n"%(args.setdpi[0], xy[0], xy[1]))

        elif args.setmode:
            self.pyRAT_set_active_dpi_mode(dev, args.setmode[0])

        time.sleep(0.3)
        self.pyRAT_release_device(dev, interface)

if __name__ == '__main__':
    pyRAT()
