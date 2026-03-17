# (not related to postgreSQL will removed to other folders)

# simple malloc 
malloc manage a heap(a big chunk of memory)
use free list(linked list) to record empty blocks 

heap = [0,1,2...999]
free_list = {start:0, size: 1000, next:null}

malloc(100) - find a free chunk big enough, split it:
heap = [AAAAA....999]
free_list = {start:100, size: 900, next:null}

malloc(200)
heap = [AAAAA|BBBBBBBB....999]
free_list = {start:300, size: 700, next:null}

free(A)
heap = [.....|BBBBBBBB....999]
free_list = {start:0, size: 100} -> {start:300, size: 700, next:null}

malloc(50)
heap = [CCC...|BBBBBBBB....999]
free_list = {start:50, size: 50} -> {start:300, size: 700, next:null}

