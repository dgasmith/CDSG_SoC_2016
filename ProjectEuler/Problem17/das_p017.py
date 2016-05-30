# "By-hand" solution of Problem 17:

# 900 occurrences of "hundred"
# 891 occurrences of "and"; the even hundred will have no "and" after it (e.g., 100)
# 100 occurrences of each tens-place-base-value (e.g., "twenty")
# 10 occurrences of each of the teens (e.g., "thirteen"), as well as "ten"
# 190 occurrences each of "one"--"nine", 90 for each in ones place, 100 for each as # hundreds
# 1 occurrence of "one thousand"

print(891*len('and') + 900*len('hundred') + 100*(len('twenty') + len('thirty') + len('forty') + len('fifty') + len('sixty') + len('seventy') + len('eighty') + len('ninety')) + len('thousand') + 10*(len('ten') + len('eleven') + len('twelve') + len('thirteen') + len('fourteen') + len('fifteen') + len('sixteen') + len('seventeen') + len('eighteen') + len('nineteen')) + 190*(len('two') + len('three') + len('four') + len('five') + len('six') + len('seven') + len('eight') + len('nine')) + 191*len('one'))
