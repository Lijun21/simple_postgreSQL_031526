# Disk to File system

At the the end of this session, you'll understand the concepts of: 
disk(HDD, SSD), secters, disk driver, format disk
hardware protocal: SATA, NVMe, DMA
Kernel, Kernel disk driver, block layer/scheduler, File system,
Kenel RAM, superblock copy, inode cache, dentry cache, page cache, buffer cache

how to store data into disk
how to read data into disk

how to store data from computer into disk
how to read data into disk
-------(one more part)
VFS 
process fd, process struct, relative path, absolute path
network
keyboard
    

## your computer write to a disk
Kernel to disk 

kernel cache miss
  ↓
VFS says "I need block #8801"
  ↓
ext4 driver  ← knows the filesystem layout, translates to physical location
  ↓
block layer  ← queues the request (maybe merges with other pending requests)
  ↓
disk driver  ← speaks the hardware protocol (NVMe, SATA)
  ↓
hardware     ← actual read, DMA transfers bytes into kernel RAM
  ↓
block #8801 now in page cache
  ↓
VFS reads it ← scans for "photo.jpg" → finds inode #91



## you write to a disk

You write a value to a memory address
    ↓
That address is wired to the SATA controller chip
    ↓
The controller translates it to electrical signals on the SATA cable
    ↓
The drive's own internal CPU receives the signal
    ↓
The drive motor seeks, the head reads/writes, sends back signals
    ↓
Controller receives the response, puts result bytes at a memory address
    ↓
You read from that memory address



## two driver 
disk driver   who: hardware manufacturer
              what: speak to this specific hardware
              knows: sectors, read/write commands, DMA

ext4 driver   who: filesystem designer
              what: organize bytes into files/dirs
              knows: inodes, blocks, bitmaps, journals

same ext4 → run on SSD, HDD, USB stick (different disk drivers)
same disk → format as ext4, xfs, btrfs (different filesystems)






## Computer boot full sequence 

Power on
    ↓
UEFI firmware runs (from ROM chip on motherboard — not disk)
    ↓
UEFI reads EFI partition (FAT32) → finds bootloader
    ↓
bootloader (GRUB) loads kernel image into RAM
    ↓
kernel starts executing in RAM
    ↓
kernel creates rootfs in RAM (tiny virtual filesystem)
    ↓
kernel creates /dev in RAM (devtmpfs)
    ↓
kernel probes hardware, populates /dev/*
    ↓
kernel mounts real root filesystem from disk
    ↓
now real /bin, /sbin, /etc available
    ↓
init/systemd starts
    ↓
system fully booted



## file system virtually divided disk into blocks 



## disk speaks "sectors", file system speaks "blocks", kernel speaks "pages"
Application, a process, a thread, wants to read a file, make a system call 
first open(path)
 "/doc/blogs/blog2.txt"


```
open("/doc/blogs/blog2.txt")
  → VFS → ext driver → read superblock → GDT → inode table → inode 2 (root)
  → traverse: root → doc → blogs → blog2.txt  (inode lookup at each step)
  → return fd

read(fd, buf, len)  ← this is where block 5 comes in
  → kernel checks page cache → miss → disk driver → block→sector translation → disk I/O
  → data stored in page cache → copied to user buffer
```


go to disk[1024] read raw bytes, get first_data_block, search in GDT chain for inode number 2, find data block number, 
in the dir data block, seach for dir "doc", get "doc" inode number, go to GDT chain, search for the inode number, find block number for "doc"
go in the block number, seach for dir name "blogs", found it, use the correspond inode number, search in GDT chain, find block number, go to the block number, find file name "blog2.txt", get the inode nubmer, search in GDT, inode tables, find blog2.txt data block, its real content.

each time we get a block number, need to tanslatte from block number to sector number, disk driver reponsoble to do the actual work
the real binary data get store into page cache managed by kernal

disk driver fetch root dir 
read or store file in disk, has to speak disk language, and it's slow.

read(fd, buffer, sizeOfBuffer)

RAM, page cache, managed by Kernel, do you have it? No

what about RAM? does it speak the same language as Kernal? 
what languaeg CPU speak? 








CPU as the manual labor
disk driver read one bit, we catch one
constantly checking if the data is ready 


I want to write a blog for education purpose, I need a "line", logic line, from simple to complex, from most entry level developer knows, to what they don't know, the previous paragraph is the input of the next paragraph, input, outpt, and so on.
set one goal, 
structure start from very basic, able to to satisfy the goal.
then more actions, needs get into the system, we hit a problem, we need to update the structure to feed the need.

You can adjust my line, this is what I want to talk about, if I make mistake, correct me.

assume readers understands
array, blocks, block bitmap, inode table, inode bitmap, GDT, superblock, directory, file system.


## disk speak "sectors" file stystem speak "blocks"
now I want to introduce, real disk, can read and write file, but read, have to tell it from address to address, 
write, have to tell it from address to address.
disk speak "sectors". size veries.
disk has its own controller do the work, read and write bits.
think of it as a smaller computer.

HHD, has a disk head move from position 0 to the end, can only take one command at once.
SSD, can take thousand commands at once.

for CPU to communicate with Disk, is like from one computer talk to another computer, need to follow certain rules, we call it protocals, and their protocals over the years has to changed from ATA/IDE to SATA to NVme. 
different manufactures may use different technology, they all speak "sectors", with their own size.

The file system we designed are for our computer to read/write data from a "virtual disk", help us to manage data in disk.

file system driver (software, ext4 for linux), knows about filesystem layout, need translate requst location to physical location.

kernel disk driver (software, speaks hardware protocal)

disk driver takes the request and scan disk
hardware disk

this way disk and filesystem are seperated, disk can be HHD, SSD or other, filesystem can be diff, as long as they follow same protocal, they can talk.




## Disk is really slow, how can we make the process faster?

DMA,get system bus, directly write to RAM dedicated address

add cache (page/buffer cache, supurblock/dentry/inode cache)
at each layer

multi process want to get file from disk, queue them up 
add block layer, scheduler, queue the request(merge request, sort, priority)
random/sequence IO 

allow multi process to update same file, on different block number, use lock in inode cache to synchronize update to same inode table 

each page cache has a lock, allow multi process to read same file, read lock.

SSD disk can have multi queue, much faster, vs HHD one queue




## how system call OPEN(path) work?

## how system call READ(fd, x, x) work?

## how system call WRITE(fd) work?

## how system call CLOSE(fd) work?



## other concept
DSA
RAID
NAS/SAN

NONE(used in VM) & NOOP(FIFO, used in SSD)

CFQ & Deadline (very sensitive to delay, used in database)





