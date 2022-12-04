elf_cals = []
with open("elf_cals.txt", mode="r") as data:
    sum_meals = 0
    for line in data.readlines():
        text = line.strip()
        meal = int(text) if text else 0
        if meal == 0:
            elf_cals.append(sum_meals)
            sum_meals = 0
        else:
            sum_meals += meal

max_cals = max(elf_cals)
print(f"Max calories: {max_cals}")
print(f'Elf with max calories: {elf_cals.index(max_cals) + 1}')
print(f"Sum of top three elfs: {sum(sorted(elf_cals, reverse=True)[:3])}")