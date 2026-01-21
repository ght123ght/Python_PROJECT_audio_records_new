FILE_NAME = "data.txt"


def load_data():
    # Загружает данные из файла в список словарей.
    records = []
    try:
        with open(FILE_NAME, "r", encoding="utf-8") as file:
            for line in file:
                parts = line.strip().split(";")
                if len(parts) != 6:
                    continue

                try:
                    year = int(parts[3])
                    plays = int(parts[5])
                except ValueError:
                    continue  # пропускаем некорректную строку

                records.append({
                    "artist": parts[0],
                    "track": parts[1],
                    "album": parts[2],
                    "year": year,
                    "duration": parts[4],
                    "plays": plays
                })
    except FileNotFoundError:
        print("ОШИБКА: файл не найден")
    return records


def quicksort(arr, left, right, compare):
    # Метод Хоара (быстрая сортировка).
    if left >= right:
        return

    pivot = arr[(left + right) // 2]
    i, j = left, right

    while i <= j:
        while compare(arr[i], pivot):
            i += 1
        while compare(pivot, arr[j]):
            j -= 1
        if i <= j:
            arr[i], arr[j] = arr[j], arr[i]
            i += 1
            j -= 1

    quicksort(arr, left, j, compare)
    quicksort(arr, i, right, compare)


def compare_all(a, b):
    # Исполнитель - возрастает, год - убывает, прослушивания - убывает.
    if a["artist"] != b["artist"]:
        return a["artist"] < b["artist"]
    if a["year"] != b["year"]:
        return a["year"] > b["year"]
    return a["plays"] > b["plays"]


def compare_artist(a, b):
    # Альбом - убывает, трек - возрастает.
    if a["album"] != b["album"]:
        return a["album"] > b["album"]
    return a["track"] < b["track"]


def compare_period(a, b):
    # Год - убывает, исполнитель - возрастает.
    if a["year"] != b["year"]:
        return a["year"] > b["year"]
    return a["artist"] < b["artist"]


def print_records(records):
    # Красивый вывод.
    for r in records:
        print(
            f'{r["artist"]} | {r["track"]} | {r["album"]} | '
            f'{r["year"]} | {r["duration"]} | {r["plays"]}'
        )


def menu():
    # Циклическое меню.
    records = load_data()

    while True:
        print("\nМЕНЮ")
        print("1 — Все записи")
        print("2 — Записи определенного исполнителя")
        print("3 — Записи за период")
        print("0 — Выход")

        choice = input("Выбор: ")

        if choice == "1":
            data = records.copy()
            if not data:
                print("Нет записей")
                continue
            quicksort(data, 0, len(data) - 1, compare_all)
            print_records(data)

        elif choice == "2":
            artist = input("Исполнитель: ")
            data = [r for r in records if r["artist"] == artist]
            if not data:
                print("Нет записей")
                continue
            quicksort(data, 0, len(data) - 1, compare_artist)
            print_records(data)

        elif choice == "3":
            try:
                n1 = int(input("С (Год N1): "))
                n2 = int(input("По (Год N2): "))
            except ValueError:
                print("Ошибка ввода")
                continue
            if n1 > n2:
                print("Ошибка: начальный год больше конечного")
                continue
            data = [r for r in records if n1 <= r["year"] <= n2]
            if not data:
                print("Нет записей")
                continue
            quicksort(data, 0, len(data) - 1, compare_period)
            print_records(data)

        elif choice == "0":
            break
        else:
            print("Неверный пункт меню")


def main():
    menu()


if __name__ == "__main__":
    main()
