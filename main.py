import heapq
import sys

class Node:
    def __init__(self, freq, val):
        self.val = val
        self.freq = freq
        self.left = None
        self.right = None
    
    def __lt__(self, other):
        return self.freq < other.freq

class HuffMan:
    def __init__(self, data):
        self.data = data
    
    def freq(self):
        hashmap = {}
        for i in range(len(self.data)):
            hashmap[self.data[i]] = hashmap.get(self.data[i], 0)+1
        return list(hashmap.items())
    
    def encodeChar(self):
        heap = []
        items = self.freq()
        for x, y in items:
            heapq.heappush(heap, Node(y, x))
        while len(heap) > 1:
            left = heapq.heappop(heap)
            right = heapq.heappop(heap)
            new_node = Node(left.freq + right.freq, None)
            new_node.left = left
            new_node.right = right
            heapq.heappush(heap, new_node)
        root = heap[0]
        encoding = self.dfs(root, '')
        bit_string = ''.join(encoding[d] for d in self.data)
        byte_data = int(bit_string, 2).to_bytes((len(bit_string)+7)//8, byteorder='big')
        return byte_data, root, len(bit_string)

    def decodeChar(self, encoded, root, bit_length):
        bit_string = bin(int.from_bytes(encoded, byteorder='big'))[2:]
        bit_string = bit_string.zfill(bit_length)
        result = []
        node = root
        for bit in bit_string:
            if bit == '0':
                node = node.left
            else:
                node = node.right
            if node.val is not None:
                result.append(node.val)
                node = root
        return ''.join(result)

    def dfs(self, node, code, codes=None):
        if codes is None:
            codes = {}
        if not node:
           return
        if node.val is not None:
            codes[node.val] = code
        else:
            self.dfs(node.left, code+'0', codes)
            self.dfs(node.right, code+'1', codes)
        return codes

    def serialize_tree(self, root):
        if not root:
            return ""
        if root.val is not None:
            return '1' + root.val
        return '0' + self.serialize_tree(root.left) + self.serialize_tree(root.right)

    def deserialize_tree(self, data):
        def helper(index):
            if data[index] == '1':
                return Node(0, data[index+1]), index + 2
            
            node = Node(0, None)
            node.left, index = helper(index + 1)
            node.right, index = helper(index)
            return node, index
        root, _ = helper(0)
        return root

    def compress(self, filename):
        encoded_bytes, root, bit_length = self.encodeChar()
        tree_string = self.serialize_tree(root)
        tree_bytes = tree_string.encode()
        with open(filename, 'wb') as f:
            f.write(len(tree_bytes).to_bytes(4, 'big'))
            f.write(tree_bytes)
            f.write(bit_length.to_bytes(4, 'big'))
            f.write(encoded_bytes)
    
    def decompress(self, filename):
        with open(filename, 'rb') as f:
            tree_len = int.from_bytes(f.read(4), 'big')
            tree_string = f.read(tree_len).decode()
            bit_length = int.from_bytes(f.read(4), 'big')
            encoded_bytes = f.read()
        root = self.deserialize_tree(tree_string)
        return self.decodeChar(encoded_bytes, root, bit_length)
    
    def efficiency(self, encoded, original):
        print(f'original size: {len(original)} bytes')
        print(f'compressed size: {len(encoded)} bytes')
        print(f'compressed percentage: {(len(encoded)/len(original))*100:.2f}%')
            
def read_file(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        return f.read()

def write_file(filename, data):
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(data)


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage:")
        print("  python main.py compress input.txt output.huff")
        print("  python main.py decompress input.huff output.txt")
        sys.exit(1)

    mode = sys.argv[1]
    input_file = sys.argv[2]
    output_file = sys.argv[3]

    obj = HuffMan("")

    if mode == "compress":
        data = read_file(input_file)
        obj.data = data
        obj.compress(output_file)
        print(f"Compressed {input_file} → {output_file}")

    elif mode == "decompress":
        decoded = obj.decompress(input_file)
        write_file(output_file, decoded)
        print(f"Decompressed {input_file} → {output_file}")

    else:
        print("Invalid mode. Use 'compress' or 'decompress'")

