inode has no idea where it is in the tree.


This Is Actually How Early Systems Worked
Early filesystems like CP/M (1974) were essentially flat:
CP/M flat namespace:
  filename limited to 8 chars + 3 extension  (8.3 format)
  one global directory per disk
  no subdirectories at all
It worked fine for floppy disks with ~50 files. It collapsed the moment disks got large and multi-user systems arrived — which is exactly why Unix introduced the tree with inodes separated from dirents in the late 1960s.

