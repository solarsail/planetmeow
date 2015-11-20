Title: 使用 gcc 的 -finstrument-functions 编译选项进行调试
Category: 调试
Tags: gcc, c, debug

编程时为了调试需要，经常想把函数的调用关系列出来。在每个函数的开头和结尾加日志输出语句比较繁琐，希望有更简洁的方法。于是就找到了 `-finstrument-functions` 编译选项。

当这个编译选项被启用时，编译器会自动在每个函数进入后和返回前分别插入两个函数：`__cyg_profile_func_enter()` 和 `__cyg_profile_func_exit()`。函数原型如下：

    :::c
    void __attribute__ ((no_instrument_function))
    __cyg_profile_func_enter (void *func_address, void *call_site);
     
     void __attribute__ ((no_instrument_function))
     __cyg_profile_func_exit  (void *func_address, void *call_site);

 其中，`func_address` 是被调用函数的地址，`call_site` 是调用方的执行地址，或函数的返回地址（基本是一回事）。只要实现了这两个函数，在里面打印出这两个地址，就可以（理论上）知道函数间的调用关系了。加入 `no_instrument_function` 属性，是为了让他们不要在进入和返回的时候执行自己。

可以实现如下：

    :::c
    #include <stdio.h>
    
    void __attribute__ ((no_instrument_function))
    __cyg_profile_func_enter( void *func_address, void *call_site )
    {
        printf("!@#C:%p:%p\n", func_address, call_site);
    }
       
    void __attribute__ ((no_instrument_function))
    __cyg_profile_func_exit ( void *func_address, void *call_site )
    {
        printf("!@#R:%p:%p\n", func_address, call_site);
    }

其中 `C` 代表 call，`R` 代表 return。`!@#` 是为了将输出与程序本身的输出区分开来。

使用 `-g -finstrument-functions` 选项编译，执行可以看到类似如下输出：

    !@#C:0x400edd:0x7f78691e3af5
    !@#C:0x4011c9:0x400f0b
    !@#C:0x40117d:0x401213
    !@#R:0x40117d:0x401213
    !@#C:0x400f34:0x401283
    !@#C:0x400e70:0x400ff8
    !@#R:0x400e70:0x400ff8
    !@#C:0x400f34:0x40110d
    !@#C:0x400e70:0x400ff8
    !@#R:0x400e70:0x400ff8
    !@#C:0x400f34:0x40110d
    !@#C:0x400e70:0x400fd2

这就是函数调用关系信息了。但是基本看不懂，需要进一步处理。为了让这些地址能被看懂，需要用到 addr2line 工具。这也是使用 `-g` 选项的原因。显然一个一个地址的查是不可行的，写脚本处理才是正道。这里使用 awk 脚本进行处理。

    #!/bin/awk -f
    BEGIN { FS = ":" }
    {
        if ($1 == "!@#C") {
            faddr = $2
                site = $3
    
                "addr2line -e "binary" -fs "faddr | getline callee
                close("addr2line -e "binary" -fs "faddr)
    
                "addr2line -e "binary" -fsp "site | getline caller
                close("addr2line -e "binary" -fsp "site)
    
                print "\033[32m["caller"]\t==>\t["callee"]\033[0m"
        } else if ($1 == "!@#R") {
            faddr = $2
                site = $3
    
                "addr2line -e "binary" -fs "faddr | getline callee
                close("addr2line -e "binary" -fs "faddr)
    
                "addr2line -e "binary" -fs "site | getline caller
                close("addr2line -e "binary" -fs "site)
    
                print "\033[33m["caller"]\t<==\t["callee"]\033[0m"
        } else {
            print $0
        }
    }

首先，指定分隔符为冒号。如果发现以 `!@#C` 开头，说明是函数调用；用绿色（\033[32m）输出 `[调用方 at 文件:位置] ==> [被调用方]`。如果发现以 `!@#R` 开头，说明是函数返回；用棕黄色（\033[33m）输出 `[调用方] <== [被调用方]`。否则就是程序自己的输出，原样打印。高亮行将 `addr2line -e 程序名 -fs` 地址的第一行输出存入 `callee` 变量，实际上是被调用的函数名。`binary` 是一个未赋值的变量，将作为参数传入，代表编译的可执行程序。调用了外部函数并用 `getline` 获取输出后需要 `close()`，具体见GNU官方文档。

保存成 pretty_printer.awk，`chmod +x` 赋予执行权限。

    $ ./test | ./pretty_printer.awk -v binary=test

可以得到类似下面的输出：

![result]({filename}/image/gcc-finstrument-functions-result.png)

这样就好看多了。（开头的 `??` 是 glibc 中的函数，所以无法显示。）
