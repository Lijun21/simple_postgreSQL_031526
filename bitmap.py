class Bitmap:
    def __init__(self, size):
        """
        size: number of bits
        We store bits packed into Python integers (acting as 64-bit words)
        """
        self.size = size
        self.words = [0] * ((size + 63) // 64)  # ceil(size / 64) words

    def _check(self, i):
        if i < 0 or i >= self.size:
            raise IndexError(f"Bit index {i} out of range [0, {self.size})")

    def set(self, i):
        """Set bit i to 1"""
        self._check(i)
        self.words[i // 64] |= (1 << (i % 64))

    def clear(self, i):
        """Set bit i to 0"""
        self._check(i)
        self.words[i // 64] &= ~(1 << (i % 64))

    def test(self, i):
        """Return True if bit i is 1, False if 0"""
        self._check(i)
        return bool(self.words[i // 64] & (1 << (i % 64)))

    def _check_same_size(self, other):
        if self.size != other.size:
            raise ValueError(f"Bitmap sizes differ: {self.size} vs {other.size}")

    def AND(self, other):
        """Return new bitmap: self & other (intersection)"""
        self._check_same_size(other)
        result = Bitmap(self.size)
        result.words = [a & b for a, b in zip(self.words, other.words)]
        return result

    def OR(self, other):
        """Return new bitmap: self | other (union)"""
        self._check_same_size(other)
        result = Bitmap(self.size)
        result.words = [a | b for a, b in zip(self.words, other.words)]
        return result

    def XOR(self, other):
        """Return new bitmap: self ^ other (difference)"""
        self._check_same_size(other)
        result = Bitmap(self.size)
        result.words = [a ^ b for a, b in zip(self.words, other.words)]
        return result

    def find_first_zero(self):
        """Find index of first 0 bit (first free block). Returns -1 if all set."""
        for word_idx, word in enumerate(self.words):
            if word == ~0 & ((1 << 64) - 1):  # all 64 bits set
                continue
            for bit in range(64):
                i = word_idx * 64 + bit
                if i >= self.size:
                    return -1
                if not (word & (1 << bit)):
                    return i
        return -1

    def count_ones(self):
        """Count number of 1 bits (used blocks)"""
        return sum(bin(w).count('1') for w in self.words)

    def __repr__(self):
        bits = ''.join('1' if self.test(i) else '0' for i in range(self.size))
        # group into nibbles of 4 for readability
        grouped = ' '.join(bits[i:i+4] for i in range(0, len(bits), 4))
        return f"Bitmap({self.size}): {grouped}"


# ─────────────────────────────────────────────
# Demo 1: set / clear / test
# ─────────────────────────────────────────────
print("=" * 55)
print("DEMO 1: set / clear / test")
print("=" * 55)

b = Bitmap(16)
print(f"Initial:       {b}")

b.set(0)
b.set(3)
b.set(7)
b.set(15)
print(f"After set(0,3,7,15): {b}")

print(f"test(3)  → {b.test(3)}   (bit 3 is 1)")
print(f"test(5)  → {b.test(5)}  (bit 5 is 0)")

b.clear(3)
print(f"After clear(3): {b}")
print(f"test(3)  → {b.test(3)}  (now cleared)")


# ─────────────────────────────────────────────
# Demo 2: AND / OR / XOR
# ─────────────────────────────────────────────
print()
print("=" * 55)
print("DEMO 2: AND / OR / XOR")
print("=" * 55)

a = Bitmap(16)
b = Bitmap(16)

# A = bits 0,1,2,3 set     → 0000 0000 0000 1111
# B = bits 2,3,4,5 set     → 0000 0000 0011 1100
for i in [0, 1, 2, 3]:     a.set(i)
for i in [2, 3, 4, 5]:     b.set(i)

print(f"A        = {a}")
print(f"B        = {b}")
print()
print(f"A AND B  = {a.AND(b)}   ← only bits both have (2,3)")
print(f"A OR  B  = {a.OR(b)}   ← all bits either has (0,1,2,3,4,5)")
print(f"A XOR B  = {a.XOR(b)}   ← bits that differ (0,1,4,5)")


# ─────────────────────────────────────────────
# Demo 3: disk block allocation simulation
# ─────────────────────────────────────────────
print()
print("=" * 55)
print("DEMO 3: Disk Block Allocator")
print("=" * 55)

class DiskAllocator:
    def __init__(self, total_blocks):
        self.total = total_blocks
        self.bitmap = Bitmap(total_blocks)  # 0 = free, 1 = used

    def allocate(self, n):
        """Allocate n contiguous free blocks. Returns start index or -1."""
        count = 0
        start = -1
        for i in range(self.total):
            if not self.bitmap.test(i):
                if count == 0:
                    start = i
                count += 1
                if count == n:
                    for j in range(start, start + n):
                        self.bitmap.set(j)
                    return start
            else:
                count = 0
                start = -1
        return -1

    def free(self, start, n):
        """Free n blocks starting at start."""
        for i in range(start, start + n):
            self.bitmap.clear(i)

    def status(self):
        used = self.bitmap.count_ones()
        print(f"  {self.bitmap}")
        print(f"  Used: {used}/{self.total} blocks")

disk = DiskAllocator(24)
print("Initial state:")
disk.status()

f1 = disk.allocate(4)
print(f"\nAllocate 4 blocks for file1 → starts at block {f1}")
disk.status()

f2 = disk.allocate(6)
print(f"\nAllocate 6 blocks for file2 → starts at block {f2}")
disk.status()

print(f"\nDelete file1 (free 4 blocks at {f1})")
disk.free(f1, 4)
disk.status()

f3 = disk.allocate(3)
print(f"\nAllocate 3 blocks for file3 → starts at block {f3}  (reuses freed space)")
disk.status()



"""
=======================================================
DEMO 1: set / clear / test
=======================================================
Initial:             Bitmap(16): 0000 0000 0000 0000
After set(0,3,7,15): Bitmap(16): 1001 0001 0000 0001
test(3)  → True   (bit 3 is 1)
test(5)  → False  (bit 5 is 0)
After clear(3):      Bitmap(16): 1000 0001 0000 0001
test(3)  → False  (now cleared)

=======================================================
DEMO 2: AND / OR / XOR
=======================================================
A        = Bitmap(16): 1111 0000 0000 0000
B        = Bitmap(16): 0011 1100 0000 0000

A AND B  = Bitmap(16): 0011 0000 0000 0000   ← only bits both have (2,3)
A OR  B  = Bitmap(16): 1111 1100 0000 0000   ← all bits either has (0–5)
A XOR B  = Bitmap(16): 1100 1100 0000 0000   ← bits that differ (0,1,4,5)

=======================================================
DEMO 3: Disk Block Allocator
=======================================================
Initial state:
  Bitmap(24): 0000 0000 0000 0000 0000 0000
  Used: 0/24 blocks

Allocate 4 blocks for file1 → starts at block 0
  Bitmap(24): 1111 0000 0000 0000 0000 0000
  Used: 4/24 blocks

Allocate 6 blocks for file2 → starts at block 4
  Bitmap(24): 1111 1111 1100 0000 0000 0000
  Used: 10/24 blocks

Delete file1 (free 4 blocks at 0)
  Bitmap(24): 0000 1111 1100 0000 0000 0000
  Used: 6/24 blocks

Allocate 3 blocks for file3 → starts at block 0  (reuses freed space)
  Bitmap(24): 1110 1111 1100 0000 0000 0000
  Used: 9/24 blocks

"""


