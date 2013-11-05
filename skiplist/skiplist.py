# http://pythonsweetness.tumblr.com/post/45227295342/fast-pypy-compatible-ordered-map-in-89-lines-of-python

import math, random

class SkipList:
    """Doubly linked non-indexable skip list, providing logarithmic insertion
    and deletion. Keys are any orderable Python object.

        `maxsize`:
            Maximum number of items expected to exist in the list. Performance
            will degrade when this number is surpassed.
    """
    def __init__(self, maxsize=65535):
        self.max_level = int(math.log(maxsize, 2))
        self.level = 0
        self.head = self._makeNode(self.max_level, None, None)
        self.nil = self._makeNode(-1, None, None)
        self.tail = self.nil
        self.head[3:] = [self.nil for x in xrange(self.max_level)]
        self._update = [self.head] * (1 + self.max_level)
        self.p = 1/math.e

    def _makeNode(self, level, key, value):
        node = [None] * (4 + level)
        node[0] = key
        node[1] = value
        return node

    def _randomLevel(self):
        lvl = 0
        max_level = self.level + 1
        while random.random() < self.p and lvl < max_level:
            lvl += 1
        return lvl

    def items(self, searchKey=None, reverse=False):
        """Yield (key, value) pairs starting from `searchKey`, or the next
        greater key, or the end of the list. Subsequent iterations move
        backwards if `reverse=True`. If `searchKey` is ``None`` then start at
        either the beginning or end of the list."""
        if reverse:
            node = self.tail
        else:
            node = self.head[3]
        if searchKey is not None:
            update = self._update[:]
            found = self._findLess(update, searchKey)
            if found[3] is not self.nil:
                node = found[3]
        idx = 2 if reverse else 3
        while node[0] is not None:
            yield node[0], node[1]
            node = node[idx]

    def _findLess(self, update, searchKey):
        node = self.head
        for i in xrange(self.level, -1, -1):
            key = node[3 + i][0]
            while key is not None and key < searchKey:
                node = node[3 + i]
                key = node[3 + i][0]
            update[i] = node
        return node

    def insert(self, searchKey, value):
        """Insert `searchKey` into the list with `value`. If `searchKey`
        already exists, its previous value is overwritten."""
        assert searchKey is not None
        update = self._update[:]
        node = self._findLess(update, searchKey)
        prev = node
        node = node[3]
        if node[0] == searchKey:
            node[1] = value
        else:
            lvl = self._randomLevel()
            self.level = max(self.level, lvl)
            node = self._makeNode(lvl, searchKey, value)
            node[2] = prev
            for i in xrange(0, lvl+1):
                node[3 + i] = update[i][3 + i]
                update[i][3 + i] = node
            if node[3] is self.nil:
                self.tail = node
            else:
                node[3][2] = node

    def delete(self, searchKey):
        """Delete `searchKey` from the list, returning ``True`` if it
        existed."""
        update = self._update[:]
        node = self._findLess(update, searchKey)
        node = node[3]
        if node[0] == searchKey:
            node[3][2] = update[0]
            for i in xrange(self.level + 1):
                if update[i][3 + i] is not node:
                    break
                update[i][3 + i] = node[3 + i]
            while self.level > 1 and self.head[3 + self.level].key is None:
                self.level -= 1
            if self.tail is node:
                self.tail = node[2]
            return True

    def search(self, searchKey):
        """Return the value associated with `searchKey`, or ``None`` if
        `searchKey` does not exist."""
        node = self.head
        for i in xrange(self.level, -1, -1):
            key = node[3 + i][0]
            while key is not None and key < searchKey:
                node = node[3 + i]
                key = node[3 + i][0]
        node = node[3]
        if node[0] == searchKey:
            return node[1]

if __name__ == '__main__':
    sl = SkipList()
    sl.insert("IRR", "ivan ribeiro rocha")
    sl.insert("ALE", "alessandra cristina dos santos")
    sl.insert("BAB", "babi cristina dos santos")
    sl.insert("LAR", "lara cristina dos santos")
    sl.insert("LUM", "luma cristina dos santos")
    for n in sl.items():
        print n
