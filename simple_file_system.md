
Given a large empty array, size is 1MB, we call this a disk.
we also have array of bytes, we call these files. 
We need to desgin a system to store these files into disk and read them when needed.


Frist file, 1KB binay file. ("a"*1024)

## Question1: Where to store it?
Hint, the 1MB array have 1024 blocks, each block is 1KB. The read and write unit is 1KB. 
disk[0,1,2,3,4..1023] = 1KB

Answer: Pick any random block, say #3 block, and store in it. That's it, done.
disk[0,1,"a",3,4..1023] = 1KB


## Question2: another file 1KB("b"*1024), where to store it?
Now, if we pick #3 block again, the previous file would be overwritten, we need a way to know which blocks are empty. 

We can scan the disk from 0 to 1023 blocks, find the first empty block.
It works, but it's O(n) time complexity, do we have a better way? 

we can keep track the index of frist empty block, store it at block 0. Only track the frist empty block, once its filled, still need to scan the entire disk to find the next empty block, still O(n) time complexity, any better way? 

We can keep the info about which blocks are empty or used block 0
disk = [0,1,"a",3,4...1023]
block_usage = [0,0,1,0,0...0]
note, block useage value is boolean type, only takes 1 bit space, 1024 blocks total 1024 bits = 128 bytes, we can use block 0 to store it, fits easily in 1 block.

now our disk looks like:
disk = [block_usage,1,"a",3,4...1023]
block_usage = [1,0,1,0,0...0]

we call this method of indicating which empty block as: Bitmap, and the first block got a unique name, as: Block Bitmap

Now we our new structure, to add a new file ("b"*1024), we read the frist block disk[0] and seach for frist 0 value
disk[0] = Block Bitmap = [1,0,1,0,0...0]
it's the second block 
then store the file at the second block
at last update the Block Bitmap 
disk = [block_bitmap,"b","a",3,4...1023]
block_bitmap = [1,1,1,0,0...0]

## Question3: How to find the file I just stored in the disk?
Should I tell the disk to give me file base on block index number? What if it's block 1189, or other random long number that I can not remember? It seems unreasonable. 

Anytime there's challenge, we change the structure of the disk, feed the need. We create a name for each file, called file_name, use it to seach for it, so we need record the corresponse of file_name and block index number, also other info like time_created, file_size, file_permission, name_length etc, total 128 bytes
{
    file_name: "a_file" (4 bytes)
    created_at: "xxx" (4 bytes)
    file_size: "1KB" (4 bytes)
    block_number: "2" (4 bytes)
    name_length:"6 bytes" (4 bytes)
    ...
}
we need to pick a block in disk to store these info(metadata of the file stored in disk), and create a name for that block as: inode.

now with our new structure, if now we want to store a new file, say 1KB("c"*1024), we need to read from block_bitmap to find frist empty block index, store the data into the index, update the block_bitmap value from 0 to 1, find the inode block index to fill in metadata of this new file.

# how to find this inode block index?
if one inode is 128 bytes, 1 block can store maxinum 1000/128 = 7 inodes, we call these as: inode table
{
    0: file_a
    1: file_b
    2: file_c
}
The same as we need to find the blocks for files, we also need a way to store inode block info, bitmap to find inodes unsage info.
keep at disk[1]
and create a name for it: Inode bitmap

one inode table, coresponse to one inode bitmap
if 1 block is not enough store all inodes, we can use two or more blocks to store inodes info. But this way the blocks used to store files would be reduced.

# How to store a file size 5kb?
we need continuous blocks to store, but what there are deleted blocks, hard to find a gap that fits it. We can store in non-contigoues blocks, 
in inode, we store block_number 4 bytes, add more
{
    file_name: "a_file" (4 bytes)
    created_at: "xxx" (4 bytes)
    file_size: "1KB" (4 bytes) 
    block_number: "2" (4 bytes) -> "2, 4, 6 .." (5 * 4 bytes)
    name_length:"6 bytes" (4 bytes)
    ...
}

but each inode is 128 bytes, what if we need to store 20KB file? do we really need to expand inode? 

use last byte to point to the another block to indexes, now, suddenly, 1000/4  = 250 block number can be stored, file size max 255KB
this type of link, is called frist class link.

if file is even larger
the last bit of the block can point to another block. 
file size max can be 510KB, and so on.
this type of link, is called second class link.

Now we can record large files, and not wasting space in the disk.


now try to save file_d, we need to find inode_bitmap block frist, it tell use which inode table row can be used to fill out inode info for file_d, but there can be multi inode_bitmap block, where are they?

create a block used to store decription blocks, we call it: Group Desciptor table
{
    block_bitmap: 1
    inode_bitmap: 2
    inode_table: 3
}

inside a disk, the nubmer of inodes and blocks are limited, we want to have space to store this info.

we use another block at disk[0], called: Superblock
{
    inode count:
    empty inodes: 
    file block numers
    empty blocks count
}

now, we have a new file_d, frist see








Fun things at the end to think about:
why did I set the disk block size a 1KB, why not 1byte, why not 1GB? Modern HDD/SSD disk read/write unit size is 4KB, CPU MMU uses 4KB pages, do you know why they are the same?

what if I store many many tiny files in the disk, what would happen? 
inodes blocks are limited

















 







