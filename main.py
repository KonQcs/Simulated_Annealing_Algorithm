import math
import random
from collections import namedtuple

#δομή block
Block = namedtuple('Block', ['id', 'width', 'height'])

#εκφραση
E = ['10', '9', 'H', '2', '5', 'V', '1', 'H', '3', '7', '4', 'V', 'H', '6', 'V', '8', 'V', 'H', 'V']

# x, y για καθε block
blocks = {
    str(1): Block(id=1, width=3, height=2),
    str(2): Block(id=2, width=1, height=1),
    str(3): Block(id=3, width=4, height=1),
    str(4): Block(id=4, width=3, height=1),
    str(5): Block(id=5, width=1, height=5),
    str(6): Block(id=6, width=1, height=2),
    str(7): Block(id=7, width=5, height=1),
    str(8): Block(id=8, width=1, height=3),
    str(9): Block(id=9, width=6, height=1),
    str(10): Block(id=10, width=1, height=2)
}

def RandomMove(expr):
    new_expr = expr.copy()
    move_type = random.randint(1, 4)  #choose random move 1,2,3,4

    if move_type == 1:
        # Ανταλλαγή δύο τελεστών
        i = random.randint(0, len(expr) - 2)
        if (expr[i] in ['H', 'V'] and expr[i + 1] in ['H', 'V']) or (expr[i] not in ['H', 'V'] and expr[i + 1] not in ['H', 'V']):
            new_expr[i], new_expr[i + 1] = new_expr[i + 1], new_expr[i]

    elif move_type == 2:
        # Αντιστροφή αλυσίδας
        start = random.randint(0, len(expr) - 3)
        end = random.randint(start + 2, len(expr) - 1)
        sub = new_expr[start:end]
        sub.reverse()
        new_expr[start:end] = sub

    elif move_type == 3:
        #αλλαγή e(i) -- e(i+1)
        for i in range(1, len(expr) - 1):
            ei = expr[i]
            if ei not in ['H', 'V']:
                ei_prev = expr[i - 1]
                ei_next = expr[i + 1]
                if ei_prev != ei_next and expr.count(ei_next) * 2 < i:
                    new_expr[i], new_expr[i + 1] = new_expr[i + 1], new_expr[i]
                    break

    elif move_type == 4:
        #ανταλλαγή width - height
        operand_indices = [i for i, token in enumerate(expr) if token not in ['H', 'V']]
        if operand_indices:
            index = random.choice(operand_indices)
            block_id = new_expr[index]
            original = blocks[block_id]
            blocks[block_id] = Block(id=block_id, width=original.height, height=original.width)

    return new_expr

def IsValid(expr):
    count = 0
    for i in range(len(expr)):
        token = expr[i]

        # διαδοχικά H ή V
        if i < len(expr) - 1:
            if token in ['H', 'V'] and token == expr[i + 1]:
                return False

        #ισορροπίας
        if token in ['H', 'V']:
            count -= 1
        else:
            count += 1

        if count < 1:
            return False

    return True

def EvaluateArea(expr):
    stack = []
    for token in expr:
        if token not in ['H', 'V']:
            b = blocks[token]
            stack.append((b.width, b.height))
        else:
            b2 = stack.pop()
            b1 = stack.pop()
            if token == 'H':
                w = max(b1[0], b2[0])
                h = b1[1] + b2[1]
            else:  # Κάθετη: πλάτη προστίθενται
                w = b1[0] + b2[0]
                h = max(b1[1], b2[1])
            stack.append((w, h))
    final_w, final_h = stack[0]
    return final_w * final_h

def EvaluateP(d):
    negd = d - 2*d
    p = math.exp( negd / T )
    return p


Best = E
BestArea = EvaluateArea(E)
#Temperture
T = 100
r = 0.999
# New T after each repeat = r*T >>> 0.999*100 = 99.9
limit =0.1
repeats = 0

while T > limit:
    NE = RandomMove(E)
    if IsValid(NE):
        area = EvaluateArea(NE)
        delta = area - BestArea
        if delta < 0 or random.random() < EvaluateP(delta):
            E = NE
            if area < BestArea:
                Best = NE
                BestArea = area
        T *= r
        repeats += 1
        if repeats > 100000:  # ασφάλεια για άπειρους βρόχους
            break

print(Best,'\t', BestArea,'\t', repeats)

with open("results.txt", "a") as file:
    file.write(f"{Best}\t{BestArea}\t{repeats}\n")
