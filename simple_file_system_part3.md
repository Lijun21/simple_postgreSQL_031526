# VFS (Linux OS)

At the the end of this session, you'll understand the concepts of: 
disk (fd, kernel disk driver, blocker layer/scheduler, disk driver, disk)
network,
keyboard,
Monitor,
printer,

process (compare disk to network and process and keyboard/printer),

VFS create fack dir(no record in disk), only exist in Kernal RAM, so everyone use OPEN, READ, WRITE, CLOSE, interface
such clean structure.

we built this powerful machine, how to use to solve our problems?
write a program.
CPU so fast, you can run multi programs all together(one by one but looks like altogether).
that's why we need programming languages.

all "power" are files, real ones saved on disk, fack ones created by kernel, stored files on disk, char devices, network, program files, to view them, execute them, we use shell.

when open terminal, start the program, running a process, called shell(zsh, or bash)

tty is teletype, 
that winow is called command line interface, 
type in text as command, get response back in text.

# how shell "calls" other program
The search, when type in command, like "ls"(to list files), the Shell looks through a specific list of folders on your computer(called the PATH) to find a pre-written program with that name.

The execution: Once it finds the program, the Shell asks that OS to start a new process for that program. 

The Handoff: The Shell steps aside, lets that program run and print its output to your screen, and then "wakes up" again once the program finishes. 

## examples of "pre-written programs"
python: a massive pre-written program that runs Python code.
mkdir: a tiny program whose only job is to creat a directory.
grep: a specialist program designed to search for text.
ssh: a program that handles secure connections to other computers. 

## "Build-ins" vs "external"
Shell have a few small commands written directly into its own code so it doesn't have to look them up. These are called Shell Built-ins.
cd(change directory) is ususally a built-in because the Shell needs to change its own current location, rather than starting a new program to do it. 

## Why this is so powerful
Becasue shell is a program that calls other programs, you can pipe them together. You can take the output of one pre-written program and shove it directly into the input of antoher: 

create a file names.txt
```
cat > names.txt << EOF 
Charlie
Alice
Bob
Alice
EOF

Your Input:                What shell see:
cat > names.txt << EOF  →  run cat, stdin=buffer, stdout=names.txt
Alice                   →  buffer line 1
Bob                     →  buffer line 2  
Charlie                 →  buffer line 3
EOF                     →  end of buffer
```

shell sets up:
  stdin  ← the collected buffer ("Alice\nBob\nCharlie\n")
  stdout → names.txt  (because of >)
  then forks and exec's: cat








# process
/proc/1234/          ← process with pid 1234
  fd/                ← its open file descriptors
    0 → stdin
    1 → stdout
    3 → file.txt
    4 → socket
  maps               ← its memory layout
  status             ← state, memory usage, parent pid
  exe                ← symlink to the binary it's running
  cmdline            ← command line arguments


virual memory, to physical memory, MMU
inside of process struct(virutal memory)
```
binary code ready to be executed are loaded from disk to process RAM
commnd line arguments if any 
env variable if any
file descripter(stdin, stdout, socket, file123.txt, etc)
maps -> MMU
parent pid (which process it was forked from)
the binary code its currently running 
```

CPU start to execute the binary code 
create one thread, it may create another thread 
then create heap shared in between threads

each thread have one call stack
8MB size, there can be 1000+ call stacks, but one heap 
stack natually grows, the two are seperated apart physically 



## scheduler 
which thread should run, who's next?

thread pool
priority
priority inversion


# network
file system speak "blocks", disk speaks "sector", process speak "excute, call stack, thread", network work speak "packets"
...




# end of the session
able to explain ABC:

A computer send a file to B computer, B saved it, response back to A "file saved", A tap the shoulder of C computer, go ahead get the file I just saved on B, C make a call to fetch the file, B sometime get it, sometime doesn't get it. Why?


