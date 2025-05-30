import heapq
import sys

class Treenode:
    def __init__(self, key, num):
        self.num = num  # frequency
        self.key = key  # character
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.num < other.num

def read_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    return lines

def generate_code_table(node, code_table, code=''):
    #check is there still node
    if node is not None:
        #check if its parent node
        if node.key is not None:
            code_table[node.key] = code
        generate_code_table(node.left, code_table, code + '0')
        generate_code_table(node.right, code_table, code + '1')
    return

def hmencoder(x):
    # Read the input file
    lines = read_file(x)
    para = "".join(lines)

    # Count character frequencies
    chdict = {}
    for ch in para:
        if ch not in chdict:
            chdict[ch] = 1
        else:
            chdict[ch] += 1

    #Create heap for nodes by their frequency
    node_heap = []
    for key, num in chdict.items():
        heapq.heappush(node_heap,Treenode(key,num))

    # Build Huffman tree: each loop reduce the heap list by two and make a parent node then put it back in
    while len(node_heap) > 1 :
        left = heapq.heappop(node_heap)
        right = heapq.heappop(node_heap)
        parent = Treenode(None, left.num + right.num)
        parent.left = left
        parent.right = right
        heapq.heappush(node_heap,parent)

    #now the tree is built and the root is the node left in the heap
    root = node_heap[0]

    #making the code table
    code_table = {}
    generate_code_table(root,code_table)

    #outputting the code table with average bits calculation
    total_bits = 0
    total_char = len(para)
    with open("code.txt","w") as file:
        for ch in sorted(code_table.keys()):
            symbol = ch
            if ch == " ":
                symbol = "Space"
            elif ch == "\n":
                symbol = "\\n"
            elif ch == "\t":
                symbol = "\\t"
            file.write(f'{symbol} : {code_table[ch]}\n')
            total_bits += (len(code_table[ch]) * chdict[ch])
        file.write(f'ave = {total_bits/total_char:.2f} bits per symbol')

    #outputting the encoded message
    with open("encodemsg.txt","w") as msg:
        for ch in para:
            msg.write(code_table[ch])
                
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python hmencode.py input_file")
        sys.exit(1)
    
    input_file = sys.argv[1]
    hmencoder(input_file)
