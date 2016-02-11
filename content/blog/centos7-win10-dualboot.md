Title: CentOS 7 和 Windows 10 双系统引导
Category: 技巧
Date: 2016-01-27 16:42
Tags: centos7, windows10, dualboot
Slug: centos7-win10-dualboot

按照之前使用Ubuntu的经验，在安装好Windows之后再安装Linux发行版，会自动将Windows的启动项放在grub启动菜单里。

然而并没有。

在已经安装了Windows 10的笔记本上（使用MBR分区格式）安装了CentOS 7之后，引导时会进入grub，但是只有CentOS自己的启动项。为了能够引导到Windows，需要以下操作：

1. 进入CentOS 7，编辑`/etc/grub.d/40_custom`，或建立另外的新文件（如果明白工作原理）。

2. 在原有内容的下面加入

        menuentry 'Windows 10' {
            insmod part_msdos
            insmod ntfs
            set root='hd0,msdos1'
            ntldr /bootmgr
        }

    此处假定Windows的引导程序被安装在第一块磁盘的第一个分区（通常如此）。注意分区编号`msdosX`的数字是从1开始的，而磁盘编号`hdX`从0开始。`msdos`是分区类型。

3. 运行`grub2-mkconfig -o /boot/grub2/grub.cfg`更新grub菜单。

4. 重启。新的启动菜单项会出现在最下面。

如果希望默认引导到Windows，可以编辑`/etc/default/grub`文件，设置`GRUB_DEFAULT="Windows 10"`。
