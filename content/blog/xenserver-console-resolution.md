Title: 调整XenServer控制台分辨率
Category: 技巧
Date: 2015-12-14 15:53
Tags: xenserver, kernel

XenServer默认使用80列控制台，在大屏幕上显示效果很差。如果希望充分利用屏幕分辨率，则需要修改内核启动参数。

打开`/boot/extlinux.conf`，在第一个启动项（xe）中，将地一个`vga`参数修改为`vga=mode-0x037e`，即可将控制台分辨率调整为1280x1024。如果改为`vga=ask`，则在启动时会显示一个模式列表供选择。找到合适的模式后，将`vga`参数改为对应的值即可。

