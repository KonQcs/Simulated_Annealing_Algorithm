import math
import random
from collections import namedtuple
import csv
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import time

def generate_NPE(n):
    block_ids = [str(i) for i in range(1, n + 1)]
    operators = ['H', 'V']
    expr = []
    stack_depth = 0

    random.shuffle(block_ids)
    last_token = None  #

    while block_ids or stack_depth > 1:
        if block_ids and (stack_depth < 2 or random.random() < 0.7):
            token = block_ids.pop()
            expr.append(token)
            last_token = token
            stack_depth += 1
        else:
            possible_ops = [op for op in operators if op != last_token]
            op = random.choice(possible_ops)
            expr.append(op)
            last_token = op
            stack_depth -= 1
    return expr

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
            else:  #if V
                w = b1[0] + b2[0]
                h = max(b1[1], b2[1])
            stack.append((w, h))
    final_w, final_h = stack[0]
    return final_w * final_h

def EvaluateP(d):
    negd = d - 2*d
    p = math.exp( negd / T )
    return p

def evaluate_polish_expression(expr, blocks_dict):
    stack = []

    for token in expr:
        if token not in ('H', 'V'):
            block = blocks_dict[token]
            stack.append({
                'id': token,
                'width': block.width,
                'height': block.height,
                'x': 0,
                'y': 0,
                'children': []
            })
        else:
            b2 = stack.pop()
            b1 = stack.pop()

            if token == 'H':
                width = max(b1['width'], b2['width'])
                height = b1['height'] + b2['height']

                b2['y'] = b1['height']
                b2['x'] = 0
                b1['x'] = 0
                b1['y'] = 0

            elif token == 'V':
                width = b1['width'] + b2['width']
                height = max(b1['height'], b2['height'])

                b2['x'] = b1['width']
                b2['y'] = 0
                b1['x'] = 0
                b1['y'] = 0

            parent = {
                'id': f"({b1['id']}{token}{b2['id']})",
                'width': width,
                'height': height,
                'x': 0,
                'y': 0,
                'children': [b1, b2]
            }

            stack.append(parent)

    return stack[0]  # root block

def draw_block(block, offset_x=0, offset_y=0, ax=None):
    if ax is None:
        fig, ax = plt.subplots()

    x = offset_x + block['x']
    y = offset_y + block['y']
    w = block['width']
    h = block['height']

    if not block['children']:  # leaf block
        facecolor = block_colors[block['id']]
    else:
        facecolor = '0'

    ax.add_patch(plt.Rectangle((x, y), w, h,
                               facecolor=facecolor,
                               edgecolor='black',
                               linewidth=0.8))
    for child in block.get('children', []):
        draw_block(child, offset_x + block['x'], offset_y + block['y'], ax=ax)
    return ax

def random_color():
    colors = list(mcolors.CSS4_COLORS.values())
    excluded = {'black'}
    filtered_colors = [c for c in colors if c.lower() not in excluded]
    return random.choice(filtered_colors)


#πληθος block
n = 100

#δομή block
Block = namedtuple('Block', ['id', 'width', 'height'])
block_colors = {str(i): random_color() for i in range(1, n+1)}

#εκφραση
E = generate_NPE(n)

# x, y για καθε block
blocks = {}
with open('blocks.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        block_id = int(row['id'])
        blocks[str(block_id)] = Block(block_id, int(row['width']), int(row['height']))
print('First NPE:\n')
print(E, '\n')
Best = E
# Εκτίμηση της αρχικής διάταξης
layout = evaluate_polish_expression(Best, blocks)
# Σχεδίαση
ax = draw_block(layout)
plt.title("First Floorplan")
plt.axis('equal')
plt.show()

BestArea = EvaluateArea(E)
#Temperture
T = 100
r = 0.995


# New T after each repeat = r*T >>> 0.999*100 = 99.9
limit =0.1
repeats = 0
rejects = 0
#MT = 1

start = time.time()

while (T > limit)  and (repeats < 99999999):
    NE = RandomMove(E)
    if IsValid(NE):
        area = EvaluateArea(NE)
        delta = area - BestArea
        #MT += 1
        if delta < 0 or random.random() < EvaluateP(delta):
            E = NE
            if area < BestArea:
                Best = NE
                BestArea = area
        T *= r
        else: rejects += 1 #αθροιστης των εκφρασεων που αποριπτονται ωστε οταν βρεθουμε σε σημειο με πολλες αποριψεις να αυξησουμε το Τ
        repeats += 1
        if rejects > 100
            T += 5
            rejects = 0

end = time.time()
print('[Final NPE]  -> Area  ->  Repeats\n')
print(Best,'\t', BestArea,'\t', repeats)
print("Running Time:", end - start, "sec")
with open("csvVersion_results.txt", "a") as file:
    file.write(f"{Best}\t{BestArea}\t{repeats}\t{end}-{start}"sec"\n")

# Εκτίμηση της τελικής διάταξης
layout = evaluate_polish_expression(Best, blocks)

ax = draw_block(layout)
plt.title("Final Floorplan")
plt.axis('equal')
plt.show()


#για n=10 ολοκληρωνεται στο προγραμμα σε λιγοτερο απο 1 sec
#για n=100 και n=150 φτανει στο οριο των επαναληψεων και σταματαει, μπορει
#να εκτελειται και παμω απο μιση ωρα
