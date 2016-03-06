Title: 在 CentOS 7 minimal 的终端中获得 256 色支持
Category: 技巧
Date: 2016-02-03 16:12
Tags: centos7,fbtrem
Slug: 256color-tty-centos7-minimal

由于 Linux 的内核限制，命令行界面的终端（使用`Alt+Fn`切换）只支持 8 种颜色。如果希望在这种环境下（如安装了 CentOS 7 minimal）使用 256 色（如 vim 的彩色主题），可以选择自己改内核源码，或者使用 F(rame)B(uffer)Term(inal)。

CentOS 7 的源中没有现成的 fbterm 包，所以需要到[`http://code.google.com/p/fbterm/`](http://code.google.com/p/fbterm/) 下载。安装过程简单直接，`make && make install`，提示缺什么库安上即可。

需要注意的是系统里必须有矢量字体，因为是用 framebuffer，本质上是图形显示。

最后的“窍门”在`.bashrc`文件。在我的CentOS 7 minimal环境下，需要先将`TERM`环境变量设为 `fbterm`，然后启动`fbterm`，再进入`screen`，才能够正确地使用256色。在`.bashrc` 中添加以下内容可以在登录后自动进入`fbterm`的`screen`。来自 [StackExchange 的答案](http://unix.stackexchange.com/a/111667)。
```bash
# FbTerm
if [[ "`tty`" == /dev/tty* || ${SHLVL} -eq 2 ]]; then
    export TERM=fbterm
    if [ ${SHLVL} -eq 1 ]; then
        ((SHLVL+=1)); export SHLVL
        exec fbterm --font-size=16
    elif [ ${SHLVL} -eq 2 ]; then
        ((SHLVL+=1)); export SHLVL
        exec screen -dRq
    fi
fi
```
