Title: 在基于XenServer的OpenStack中使用ISO镜像引导安装Windows
Category: 经验
Date: 2015-11-28 15:20
Tags: c, tip

  部署环境为DevStack的Liberty版

1. 在XenServer中建立一个ISO SR，将其uuid记录下来。
2. 在Dom 0中执行`xe sr-param-set uuid=[记录的uuid] other-config:i18n-key=local-storage-iso`。
3. 使用web界面上传ISO镜像，选择适当的核心数、内存和硬盘容量。
4. （可选）建立新的flavor，以匹配上述配置。
5. 使用上传的ISO镜像启动虚拟机。

如果无法正常启动，可以尝试修改`/etc/nova/nova.conf`，在`[xenserver]`一节下增加`default_os_type = windows`并重启nova服务。不确定是否相关。

在安装xp和7时均发现磁盘已经被预先分区，而安装程序无法在分区上执行安装。可以尝试在建立虚拟机时将高级选项中“磁盘分区”一项改为手动，可能可以避免此问题。

安装xp时，会在起始阶段卡住较长的时间，最后报错，按任意键之后可以继续正常安装。不确定与上述分区问题是否有关。
