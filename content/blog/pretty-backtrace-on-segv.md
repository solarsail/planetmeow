Title: 在段错误时打印（醒目！）调用栈
Category: 技巧
Tags: c, tip

刚写好的程序，被`SIGSEGV`挂掉是难免的。为了省事起见，在程序收到`SIGSEGV`终止的时候打印一下调用栈是不错的选择。

首先有个最偷懒的办法：代码里不用加任何调试专用的内容，只要一个小工具：catchsegv。假设编译好的程序为test，其中有bug会导致segmentation fault。运行

    catchsegv ./test

就能在输出里找到：

    Backtrace:
    /home/dev/projects/tools/test.c:15(main)[0x400f10]
    /lib64/libc.so.6(__libc_start_main+0xf5)[0x7fe9d6358af5]
    ??:?(_start)[0x4004b9]

So easy. 但是如果要调试的是个后台服务程序，就需要稍微复杂一点的办法。

基本思路是`sigaction()` + `backtrace()`。首先定义信号处理函数：

    :::c linenums="True" hl_lines="12 14"
    #include <execinfo.h>
    #include <stdio.h>
    #include <stdlib.h>

    void sighandler(int sig)
    {
        void *trace[64];
     
        int size = backtrace(trace, 64);
        char **msg = backtrace_symbols(trace, size);
     
        printf("\e[31m===!! SIGSEGV CAUGHT !!===\e[0m\n");
        for (int i = 2; i < size; ++i) {
            printf("\e[31m[%d] %s\e[0m\n", i-1, msg[i]);
        }
     
        exit(-1);
    }

高亮行使用特殊的终端字符序列`\e[31m`使输出字符为红色。在末尾使用`\e[0m`恢复默认颜色，否则之后的输出会全都变成红色。另外，因为栈的前两项是进入信号处理函数，所以从第三项开始打印。

然后在`main()`中把信号处理函数注册到`SIGSEGV`上：

    :::c hl_lines="13"
    #include <signal.h>
    ...
    int main()
    {
        ...
        struct sigaction sa;
        sa.sa_sigaction = (void*)sighandler;
        sigemptyset(&sa.sa_mask);
        sa.sa_flags = SA_RESTART;
    
        sigaction(SIGSEGV, &sa, NULL);
        ...
        int i = *(int*)0;
        ...
    }

其中高亮行人为制造了一个段错误。

编译时需要加入`-g -rdynmic -std=c99 -D_GNU_SOURCE`，或`-g -rdynamic -std=gnu99`。前两个是`backtrace_symbol()`所需（否则无法获得栈中的函数名），`_GNU_SOURCE`宏是`struct sigaction`所需。

运行结果如下：

![result]({filename}/image/pretty-backtrace-on-segv-result.png)

从第一条记录可知在`main()`函数偏移0x33处有非法内存访问，可以使用objdump工具反汇编并定位。更简单的办法，可以用addr2line工具将地址转换为文件名和行号（前提是编译时使用了`-g`选项）。例如

    $ addr2line -e test -fsp 0x400f10
    main at test.c:15

可知问题出在test.c的第15行，`main()`函数中。
