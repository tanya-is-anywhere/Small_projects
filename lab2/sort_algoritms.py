

# Сортировка пузырьком
list_1 = [45, 12, 7, 36, 9, 21, 18, 55, 2, 63]
sorted_index = len(list_1)
while True:
    num_of_swap = 0
    for i in range(0, sorted_index-1):
        if list_1[i]> list_1[i+1]:
            list_1[i], list_1[i + 1] = list_1[i+1], list_1[i]
            num_of_swap += 1
    sorted_index -= 1
    if num_of_swap == 0:
        break
print(list_1)

# Сортировка выбором
list_2 = [45, 12, 7, 36, 9, 21, 18, 55, 2, 63]
for i in range(0, len(list_2)-1):
    min_ind = i
    for j in range(i+1, len(list_2)):
        if list_2[min_ind] > list_2[j]:
            min_ind = j
    if min_ind != i:
        temp = list_2[i]
        list_2[i] = list_2[min_ind]
        list_2[min_ind] = temp
print(list_2)

# Сортировка вставками
list_3 = [45, 12, 7, 36, 9, 21, 18, 55, 2, 63]
for i in range(1, len(list_3)):
    key = list_3[i]
    j = i - 1
    while j >= 0 and list_3[j] > key:
        list_3[j + 1] = list_3[j]
        j -= 1
    list_3[j + 1] = key

print(list_3)