import itertools

itempath = '/home/carolinanery/PycharmProjects/Understanding Algorithms_Recommendation/EB-build-goods.sql'
receiptspath = '/home/carolinanery/PycharmProjects/Understanding Algorithms_Recommendation/75000-out1.csv'

with open(receiptspath,"r") as receiptsfile:
  receiptsdata = receiptsfile.read().split('\n')

print(receiptsdata)

baskets = [line.split(", ")[1:] for line in receiptsdata[0:-1]]

print(baskets[0:5])

#Read the text from the items file
with open(itempath,"r") as itemfile:
  lines = itemfile.read().split('\n')

#Extract and create a map {item id: item name}
print(lines)

items = [line.split("(")[1][0:-2].split(",") for line in lines[0:-1]]
print(items[0:5])

#create a map
itemMap = {line[0]:line[1]+" "+line[2] for line in items}

numItems = len(items)
numBaskets = len(baskets)

print(numItems)
print(numBaskets)


#support(itemset) = Baskets with all items / total baskets
def support(itemset):
    basketSubset = baskets #start with all baskets
    for item in itemset:
        #Keep only baskets which contain the item
        basketSubset = [basket for basket in basketSubset if item in basket]
    return float(len(basketSubset))/float(numBaskets)

print(support(['2','24']))

supportItems1 = []
minsupport=0.01
for item in range(numItems): #Iterate through all 1 item sets
    itemset=[str(item)]
    if support(itemset)>=minsupport:
        supportItems1.append(str(item))

print(supportItems1)


def aprioriIteration(i, supportItems, assocRules, newSupportItems, minsupport, minconfidence):
  for itemset in itertools.combinations(supportItems, i):  # Generate all item sets of size i
    itemset = list(itemset)
    # Keep only those item sets which have the minimum support
    if support(itemset) > minsupport:
      # Generate rules from each item set
      for j in range(i):
        rule_to = itemset[j]
        rule_from = [x for x in itemset if x != itemset[j]]
        # Find the confidence of the rule
        confidence = support(itemset) / support(rule_from)
        # Keep the rules which cross the minconfidence threshold
        if confidence > minconfidence:
          assocRules.append((rule_from, rule_to))
          # Keep track of the items in the rules for the next iteration
          for x in itemset:
            if x not in newSupportItems:
              newSupportItems.append(x)
  return assocRules, newSupportItems

minsupport=0.01
minconfidence=0.5
assocRules=[]
newSupportItems=[]

#Generate 2 item sets
assocRules, supportItems2 = aprioriIteration(2,supportItems1,assocRules,newSupportItems,minsupport,minconfidence)

print(assocRules)

assocRules, supportItems3 = aprioriIteration(3,supportItems2,assocRules,newSupportItems,minsupport,minconfidence)

print(assocRules)


def ruleMeta(rule):
  rule_from = [itemMap[x] for x in rule[0]]
  return rule_from, itemMap[rule[1]]

print([ruleMeta(rule) for rule in assocRules])