# simple postgreSQL 

postgreSQL = file system + ACID + MVCC + analytics/Vacume
           = OS(RAM + disk driver + disk) + Atomic/Consistency/Isolation/Durability + Multi Version Concurrency Control 


learning path: from fundemental, simplest to complex


store and query one bit, 
in RAM, in disk(use logic gates SSD or magnetic Hard drive)
fetch by value, fetch by address

RAM and DISK are like large array, one is volatile, one is persistent

1KB, 1024 bytes, modurino chip, RAM+DISK+CPU all in one

store a byte, with meaning, for user 

store static fixed sized data 

```c
int temperature = 70; // 2 bytes in memory 
int humidity = 50; // 2 bytes 
char id[] = "12345678"; // 9 bytes (8 + null terminator) 
```
c code get compiled into binary code, store in disk, fetched by 

I know the size of each line, compile this code into binary, store into disk, 
fetch huminty from byte x-y, give it to RAM, CPU can exceute it dirctly


store veried sized data 
store an object, programming language code to binary file 





A file is simply a linear array of bytes. Can be any size.

A disk is large empty array. 


Ignore all other details about disk, only think its an large empty array. cut its relationship with OS, RAM, CPU, for now. 
reader only need to know about array data structure, that's it. I started the beginning, you help witht the rest:







