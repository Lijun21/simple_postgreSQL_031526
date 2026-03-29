# how our disk look like:
block 0: boot block (or unused)
block 1: superblock (always at byte offset 1024)
block 2: GDT  ← right after superblock
block 3+: inode table, block bitmap, data blocks...


```
Block Group 0:
  - superblock (primary copy)
  - GDT (primary copy)
  - block bitmap
  - inode bitmap
  - inode table
  - data blocks

Block Group 1:
  - superblock (backup copy, in some ext configs)
  - GDT (backup copy)
  - block bitmap
  - inode bitmap
  - inode table
  - data blocks

```
Each block group is self-contained with its own inode table and data blocks. The GDT in block group 0 is your single authoritative map that tells you where each group's inode table lives. Then you jump directly to the right group's inode table to find your inode 

superblock, GDT, block bitmap, inode bitmap, inode table
all fixed entry fixed size, fixed order, store in raw bits.
can be accessed like an array use offset. 
file name or dir name can not be stored in inode table, because we have no control of its length, they can only be store in data blocks. 



# how do we to read files now 
given file path with file name
```
/doc/blogs/blog2.txt
```
go to root dir at inode #2, hardcoded
to find inode 2, frist find superblock, hardcoded at disk byte 1024, size 1024 bytes, we can find it instantly. Each record is fix sized, fixed order, we can read each value directly by scan raw bytes.

```
From superblock we get:
inodes_count (Total inode count, 4 bytes)
blocks_count (Total block count, 4 bytes)
free_blocks_count (Free block count, 4 bytes)
free_inodes_count (Free inode count, 4 bytes)
first_data_block (This must be at least 1 for 1k-block filesystems and is typically 0 for all other block sizes.)
log_block_size (Block size is 2 ^ (10 + log_block_size))
blocks_per_group (Blocks per group.)
inodes_per_group (Inodes per group.)
...
total 1024 bytes
```

understand first_data_block:
if block size if 1024 bytes, 
disk[0] to disk[1023] bytes, holds file to boot computer.
disk[1024] byte holds superblock, if block size is 1024 bytes, disk[1024] is completely filled, group descripter table block chain, right next to superblock, what being called the frist data block will be starting at the next block disk[1025]
if block size is greater than 1024 bytes, disk[1024] can hold not only superblock, also GDT.

once GDT location is known, can scan the chain of GDT for inode number, once find inode number, can get block numbers for the file.

like all directory, root dir doesn't store file name directly
inode# 2 stores metadata point to data blocks, in those data blocks contain a directory entry table - a list of (file name->inode number) mappings.

```
inode 2(root /)
file_type: directory 
persmission, owner, timestamps
pointers: 22 (data block numbers)

data block 22:
file_name         inode number
.                 2 (itself)
..                2 (parent dir)
doc               47 (sub directory)
etc               83 (sub directory)
home              91 (sub directory)

inode 47
file_type: directory 
persmission, owner, timestamps
pointers: 25 (data block numbers)

data block 25:
file_name         inode number
.                 47 (itself)
..                2 (parent dir)
blogs             102 (sub directory)

inode 102
file_type: directory 
persmission, owner, timestamps
pointers: 34

data block 34 (contain dir table, file_name to inode nubmer mappings):
file_name         inode number
.                 102 (itself)
..                47 (parent dir)
blog1.txt         112 
blog2.txt         209 
blog3.txt         216 
blog4.txt         215 

inode 209
file_type: file 
persmission, owner, timestamps
pointers: 79 (data block number)

data block 79 (contain binary file content):
01010101010100101010101001000000110100011100101010100
01010101010100101010101001000000110100011100101010100
01010101010100101010101001000000110100011100101010100

```
(do i need to go to superblock, group descripter, find inode_table, then its number 2 record?)
search in all files in root, look for dir = "doc"
then go to "doc" inode number 


# file system virtually divided disk into blocks 



# disk speaks "sectors", file system speaks "blocks", kernel speaks "pages"
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





# why use database to store relational data, why not file system?
OS + disk, is able to store and fetch file of any size

what database designed for? 

ignore we have database of any type exists, let's only use file system to store relational data. 

yes relational data, normalized data. 

users table:
id, name, address, phone number, age

orders tables
id, product, name, address, phone number, age, amount, created_at X
id, product, user_id, amount, created_at 

this way we don't need to store duplicate data in orders table.

but when we query this data, we want them physically stay close to each other, file system doesn't offer this. 

# how db enable data to physically stay close to each other?
design application tables, how many estimated users, how many products we offer, each user have how many orders, each table have how many columns, each column is a data type, with fixed size. 
so we roughly know how much size of space we need for each table, plus indexes, so we know roughly the total.

ask OS to get large amount of free space, the split them for each table.
ensure rows in table all close to each other physically.

file system doesn't know the size or type of file it will store ahead of time, it can not plan ahead. 

# why db has predefined data type and what types data database defined and accept?
predefined data types = fixed size = easy to store and query each piece of data, row, table


# how db enable atomic transaction?
what is transaction? each time store or query or update a row?

write ahead log
before write data into disk, write a log into disk? extra space?
then write data next, 
once finish, compare data with log, done
if power outage at the middle of write logs, no data saved into db.
power back, frist thing compare log and db, if log > db, let it be.
if power outage at the middle of write data, 

data: 12345
log:  12345+commit
data_saved: 12345
if commit in log => good 

power outage at the middle of write log
data: 12345
log:  123
data_saved: 
if commit not in log, nothing in db, ignore this

power outage at the middle of write db
data: 12345
log:  12345+commit
data_saved: 123
if commit in log but, "replay" log, write log into db 








# how to handles Isolation?






transactions, ACID



Each letter maps to a specific mechanism:

**Atomicity — Write-Ahead Log (WAL)**
Before touching any data block, the DB writes all intended changes to a log file first.
If it crashes mid-write, on restart it reads the log: either replays the full transaction or rolls it back completely. Never a half-written state.

**Consistency — Constraints enforced at commit**
Checked before the transaction is allowed to commit: foreign keys, unique constraints, NOT NULL, etc.
If any constraint fails → entire transaction is aborted.

**Isolation — Locks or MVCC**
- **Locks**: readers/writers block each other (simple, slow)
- **MVCC** (what PostgreSQL uses): each transaction sees a snapshot of data from when it started. Writers create a new version of a row, old versions stay until no one needs them. Readers never block writers.

**Durability — fsync**
On commit, the DB calls `fsync()` to flush WAL to disk. The OS can't buffer it — it must reach physical disk before `COMMIT` returns.
This sits directly on top of the file system you built — the WAL is just a file, written to data blocks via inodes.

```
Transaction commits:
  1. write changes to WAL file  → fsync() → on disk ✓
  2. write changes to data files → can be lazy (WAL already guarantees recovery)
```

The connection to your file system: **WAL is just a file**. The DB trusts your file system to persist bytes durably, and builds ACID on top of that guarantee.