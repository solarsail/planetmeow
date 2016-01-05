Title: 使用OpenStack向XenServer虚拟机中挂载的磁盘无法工作
Category: 经验
Date: 2016-01-04 15:50
Tags: openstack, xenserver, iscsi

通过dashboard可以在volume面板中直接建立虚拟磁盘并将其挂载至虚拟机。

OpenStack向XenServer虚拟机中挂载磁盘的基本过程如下：

1. 将要挂载的卷映射为ISCSI目标（target）

2. 将ISCSI目标的参数提供给XenServer，建立ISCSI SR

3. 通过XenAPI将SR中的虚拟磁盘挂载到虚拟机中

如果DevStack是使用其自带的脚本安装在XenServer上的，那么在挂载磁盘到虚拟机后可能会发现磁盘未被识别（Linux/Win XP）或系统停止响应（Win 7）。这是由XenServer本身的[bug](https://ask.openstack.org/en/question/79549/windows-instance-freezes-after-attaching-a-cinder-volume/)导致的，如果通过Citrix提供的镜像和supplement pack安装则不存在该问题。解决方法为将Dom0中/opt/xensource/sm/ISCSISR.py中唯一出现的一处`'phy'`改为`'aio'`（XenServer 6.5）。
