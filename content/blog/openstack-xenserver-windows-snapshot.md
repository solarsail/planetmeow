Title: 在使用XenServer的OpenStack中从快照启动Windows虚拟机
Category: 经验
Date: 2016-01-05 13:27
Tags: openstack, xenserver, snapshot
Slug: boot-windows-snapshot-in-openstack-upon-xenserver

从正在运行的Windows虚拟机创建快照，再从快照启动新虚拟机时，可能会出现错误导致无法启动。在nova的日志中可以看到来源于XenServer的错误信息：

    Failure: ['INTERNAL_ERROR', 'xenopsd internal error: VM = 65a989bd-b00a-412c-5117-4c332748dd25; domid = 12; Bootloader.Bad_error Traceback (most recent call last):\n File "/usr/bin/pygrub", line 903, in ?\n fs = fsimage.open(file, part_offs[0], bootfsoptions)\nIOError: [Errno 95] Operation not supported\n']

这实际上是由于XenServer在以启动PV kernel的方式启动HVM模式的Windows虚拟机。检查镜像的元数据（metadata）可以发现，其中已经设置了一项`os_type (XenServer API Options > OS Type)`，默认值是Linux。将其改为Windows，再从快照启动新实例，就可以正常创建新虚拟机了。
