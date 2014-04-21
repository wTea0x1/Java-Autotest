java-autotest
===============================

环境要求
--------------------------
python3 以上版本
jdk 已加入环境变量
附：
[python下载地址](https://www.python.org/downloads/)

程序说明
----------------------
本程序可以将制定文件夹内的java源码自动编译打包，
然后根据输入文件给程序提供输入，
并将结果存储于输出文件。
关于输入文件、输出文件的详细信息，请看 输入文件

使用说明
------------------------
python java-autotest.py path/to/dir [options]
注意：在windows系统下输入路径请加上双引号来防止转义字符引起的问题

 options有：

        -m 设定主类
           如果主类名内有main字样，此选项可不设定
           注意，设定时请不要加上.class后缀

        -i 设定输入文件
           如果没有设定，默认取path下的input.txt
           输入文件的其他要求，请看 四、输入文件
    
        -o 设定输出文件
           如果未设定，默认使用path下的output.txt
    
        -v,--version
           输出版本信息
    
        -h,--help
           输出帮助信息

例子：
        python java-autotest.py "D:\java"
        python java-autotest.py "D:\java" -i in.txt -o out.txt -m elevator

输入文件
-----------------------
输入文件需要符合下述规则：
> 每行有且只有一个输入
> 每行开头需要有 "标示符:"
>   标示符可以任意设定成非：的字符。
>   标示符会被输出到输出文件以方便查看
>   标示符可以为空，即输入":"
> 请不要留空行，这样可能导致程序报错

bug report
------------------
仓促之间完成，bug可能比较多
如果大家发现了什么bug，欢迎来[这里](https://github.com/wTea0x1/Java-Autotest/issue)提交bug,
也欢迎大家帮我修改程序并提交至github
