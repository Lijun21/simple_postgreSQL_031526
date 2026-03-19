
Given a large empty array, size is 1MB, we call this a disk.
we also have array of bytes, we call these files. 
We need to desgin a system to store these files into disk and read them when needed.


Frist file, 1KB binay file. ("a"*1024)

## Question1: Where to store it?
Hint, the 1MB array have 1024 blocks, each block is 1KB. The read and write unit is 1KB. 
index= [0,1,2,3,4..1023]
disk = [0,0,0,0,0..0] = 1KB

Answer: Pick any random block, say #0 block, and write the file in it. That's it, done.
disk = ["a",0,0,0,0..0] = 1KB


## Question2: another file 1KB("b"*1024), where to store it?
Now, if we pick #0 block again, the previous file would be overwritten, we need a way to know which blocks are empty. 

We can scan the disk from 0 to 1023 blocks, find the first empty block.
It works, but it's O(n) time complexity, disk scan is expensive, do we have a better way? 
It works? what if the frist file was "0"*1024, can you tell if a block is empty or not by reading it? No, so we need a better way.

we can keep track the index of frist empty block, store ptr at block 0. 
This could work, if we never delete any files. But once we delete files, we start to lose track.

ptr = 0
store file_a → use block 0, ptr = 1  O(1)
store file_b → use block 1, ptr = 2  O(1)
store file_c → use block 2, ptr = 3  O(1)

delete file_a (block 0 is now free) → ptr still = 3
store file_d → use block 3, ptr = 4  ← block 0 wasted!

At the moment file_a get deleted, ptr should be 0, not 3.
Okay, what if I delete multi files. you still loose track

ptr = 3
delete file_a → ptr = 0  ✓
delete file_b → ptr = 1  ← now you forgot block 0 is free!

so to reliably find any free block(either filled with all "0" or after deletions), we must know the status of every block. 
Storing that status for all blocks in once place
1 bit per block = minimal space, one disk read to get full picuture
block_usage = [0,0,0,0,0...1023]

now reserve block 0 for block status, then store frist file at index 1
now our disk looks like:
disk = [block_usage,"a",2,3,4...1023]
block_usage = [1,1,0,0,0...0]

we call this method/technique of using bits to show which blocks are free/used as: Bitmap, and the first block got a unique name, as: Block Bitmap

Now with our new structure, to add a new file ("b"*1024), we read the frist block disk[0] and seach for frist 0 value
disk[0] = Block Bitmap = [1,1,0,0,0...0]
then store the file at the index 2 block
update the Block Bitmap 
disk = [block_bitmap,"a","b",3,4...1023]
block_bitmap = [1,1,1,0,0...0]

note, Block Bitmap, 1 bit per block, each block 1KB, max 1024 bits = 128 bytes, if disk size is 1GB, 1 block won't be able to hold all status values, we will discuss the solution later. 


## Question3: How to find the file I just stored in the disk?
Should I tell the disk to give me a file based on block index number? What if it's block 1189, or other random long number that I cannot remember? It seems unreasonable.

Anytime there's a problem, we change the structure of the disk to solve it. We create a name for each file, called file_name, use it to search for it, so we need to record the mapping of file_name and block index number, along with other metadata, total 128 bytes
{
    created_at: "xxx" (4 bytes)
    file_size: "1KB" (4 bytes)
    file_permission: "xxx" (4 bytes)
    block_number: "1" (4 bytes)
    name_length:"6 bytes" (4 bytes)
    file_name: "a_file" (6 bytes)
    ...
}
we call this metadata record for each file as: inode.
Pick a block to store these inode records, and create a name for that block as: inode Table.

now with our new structure, if now we want to store a new file, say 1KB("c"*1024), we need to read from block_bitmap to find frist empty block index, store the data into the index, update the block_bitmap value from 0 to 1, find the inode block index to fill in metadata of this new file.

if one inode is 128 bytes, 1 block can store maximum 1024/128 = 8 inodes, we call these as: inode table
{
    0: file_a
    1: file_b
    2: file_c
    ...
    7: xxx
}
more files, more inodes, we need more blocks for inode tables.
How to keep track of which inode table has available empty record spots?
Just as we use a bitmap to find free blocks for files, we use a bitmap to find free inode records.
keep at disk[1]
and create a name for it: Inode Bitmap

one inode table maps to one inode bitmap
if 1 block is not enough to store all inodes, we can use two or more blocks to store inode records. But this way the blocks used to store files would be reduced.

# How to store a file size 5kb?
we need continuous blocks to store this large file, but when there are deleted blocks, it's hard to find a contiguous gap that fits. We can store in non-contiguous blocks, 
in inode, we store all block indexes in block_number.
{
    file_name: "a_file" (4 bytes)
    created_at: "xxx" (4 bytes)
    file_size: "1KB" (4 bytes) 
    block_number: "2" (4 bytes) -> "2, 4, 6 .." (8 * 4 bytes)
    name_length:"6 bytes" (4 bytes)
    ...
}

but each inode is 128 bytes, what if we need to store a 20KB file? do we really need to expand inode?

Use the last entry to point to another block of indexes. Now, suddenly, 1024/4 = 256 block numbers can be stored, file size max ~256KB.
This type of link is called single indirect link.

If the file is even larger, the last entry of that index block can point to yet another block of indexes.
File size max ~512KB, and so on.
This type of link is called a double indirect link.

Now we can record large files, and not wasting space in the disk.
[Block Bitmap][Inode Bitmap][Inode Table][Data blocks...]



# how to fix perfermance degraded issue?
As the disk size grow, we need more than one Inode Bitmaps, and Inode Tables, and all inodes are at the front the disk, data blocks at the back. Every file access require a long seek around the whole disk. 
[Block Bitmap][Inode Bitmap0][Inode Bitmap1][Inode Table0][Inode Table1][Data blocks...]

Bitmap blocks become too large, one bitmap couldn't fit in one block anymore.

solution is, divide the disk into groups, each group has one Block Bitmap. And this block used to record the group info is called: Group Decriptor Table

Group Descriptor (one entry per group, 32 bytes):
{
    block_bitmap_block: 0  4 bytes  ← which block holds this group's Block Bitmap
    inode_bitmap_block: 1  4 bytes  ← which block holds this group's Inode Bitmap
    inode_table_block: 2   4 bytes  ← which block holds this group's Inode Table
    free_blocks_count: 30   2 bytes  ← how many free data blocks in this group
    free_inodes_count: 42   2 bytes  ← how many free inodes in this group
    <!-- used_dirs_count:      2 bytes  ← how many directories in this group -->
    ...
}
[GDT][GDT][GDT][Block Bitmap][Inode Bitmap][Inode Table][Data...]
               [Block Bitmap][Inode Bitmap][Inode Table][Data...]
               [Block Bitmap][Inode Bitmap][Inode Table][Data...]

Now a file's inode and it's data blocks live in the same group, faster access.

GDT is stored in contiguous blocks,reading all GDT entries is one sequential read, its fast. 

But before we are able to read GDT, we need to know where does the GDT start, how many groups are there? how big is each block? 
Is the disk full? so I can skip read GDT entirely. 

use a block to record overall layout of the disk
{
     -- disk layout --
    total_inodes:          4 bytes  ← total inodes on disk
    total_blocks:          4 bytes  ← total blocks on disk
    block_size:            4 bytes  ← 1024, 2048, or 4096 bytes
    blocks_per_group:      4 bytes  ← how many blocks in each group
    inodes_per_group:      4 bytes  ← how many inodes in each group
    group_count:           4 bytes  ← total number of block groups
    
    -- free space cache --
    free_blocks_count:     4 bytes  ← total free blocks across all groups
    free_inodes_count:     4 bytes  ← total free inodes across all groups
}
1024 bytes, always at byte offset 1024 from disk start,
we call this: Superblock


[Superblock][GDT][GDT][GDT][Block Bitmap][Inode Bitmap][Inode Table][Data...]
                           [Block Bitmap][Inode Bitmap][Inode Table][Data...]
                           [Block Bitmap][Inode Bitmap][Inode Table][Data...]


So to write file_d:

Read Superblock (hardcoded at byte offset 1024) → get block_size, blocks_per_group, group_count
GDTs starts right after the Superblock block (no pointer needed, position is fixed once you know block_size)
Read GDTs → find a group with free_blocks_count > 0 and free_inodes_count > 0
Go to that group's inode_bitmap_block → find free inode slot
Go to that group's block_bitmap_block → find free data block
Write data, fill inode, update both bitmaps, update GDT counts, update Superblock


With our current design, to read file_d (filename stored in inode):

Read Superblock → get block_size, group_count
GDT is right after Superblock block → read all GDT entries
For each group, go to inode_table_block → scan every inode looking for file_name == "file_d"  ← O(n) scan, slow!
Found the inode → get its block_number list
Read those data blocks → file_d content

we must scan ALL inodes across ALL groups just to find one file by name.

# how to access files faster?

we can create hash table, use a block dedicated to map file_name to inode_number 
O(1) look up any file by name globally. 
Problem is, hash collissions, renames are expensive

we can use B-tree index on disk
Store file_name mapping to inode number, in a sorted B-tree
O(log n) lookup

we can give each group a topic, dedicate group 0 to music, group 1 to documents, group 2 to downloads ...
To find "blog.txt" in documents, we need to know 
files for documents live in group2 (record this somewhere)
Scan only Group 2's inodes -> smaller scan, not a full disk scan 

To store "blog1.txt", we need to know 
blog file belong to documents, and it lives in group2 (base on record)

O(n/g) where g = group_count
better than O(n), but still a linear scan — just over a smaller set
Problems:
  - still not O(1), just O(n/g)
  - groups fill up unevenly — one group overflows, another is empty
  - need another lookup structure to say "which group is documents?" — pushes the problem up one level
  - doesn't scale: 1 million files in documents still means a huge per-group scan

any other better way? I want O(1) lookup time, no collisions, easy rename


O(n/n) = O(1), scope the search all the way down to a group of size 1.
Each "group" contains exactly 1 file = the file you already know you want.

we need a method or technique to be able to find any inode in this system, 
but doesn't require to visit every single inode in the disk

A hierarchical tree, unify everything into one tree starting at root.

Separate the file_name from inode. file_name would be stored and searched in tree structure, and inode stored and searched in linear structure.

continue tomorrow ...












## Fun things at the end to think about:
why did I set the disk block size a 1KB, why not 1byte, why not 1GB? Modern HDD/SSD disk read/write unit size is 4KB, CPU MMU uses 4KB pages, do you know why they are the same?
the block size can be set and reset on a new disk => format disk, reformat disk, haha

mkfs.ext4 -b 4096 /dev/sda1   # format with 4KB blocks
mkfs.ext4 -b 1024 /dev/sda1   # format with 1KB blocks


what if I store many many tiny files in the disk, what would happen? 
inodes blocks are limited

do you think bitmap is also data structure? 


The directory is a file, but in it's inode file_type = directory not file, hahahah




## how I structured this doc 
Problem encountered → add structure to solve it

Problem	                                Structure added
Can't tell which blocks are free	    Block Bitmap
Can't find file by name	                inode (metadata record)
Can't find which inode to use	        Inode Bitmap + Inode Table
File too large for one block	        Block pointers list in inode
Inode can't hold enough block pointers	Indirect blocks (direct/indirect links)
Can't find bitmap/inode blocks	        Group Descriptor Table
Don't know disk-wide stats	            Superblock

Each layer of structure exists because a simpler version hit a limitation. This is also how databases, networks, and most systems are designed — start simple, hit a wall, add the minimum structure needed to solve it.












 







