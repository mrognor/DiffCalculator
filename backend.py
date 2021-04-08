from sympy import diff, symbols


def find_diff(our_func, variables):
    #alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"  # задаем алфавит

    mas = []  # задаем массив
    try:
        for count in variables:  # проходим по массиву переменных
            if count != "":  # проверяем на отсутствие переменной и принадлежность к алфавиту
                our_func = our_func.replace("sin", "{")  # меняем синус на скобку
                our_func = our_func.replace("cos", "}")  # меняем косинус на скобку
                our_func = our_func.replace("tan", "|")  # меняем тангенс на палку
                our_func = our_func.replace("pi", "<")  # меняем пи на стрелочку
                our_func = our_func.replace("exp", ">")  # меняем экспоненту на стрелочку

                our_func = our_func.replace("O", "ptro")
                our_func = our_func.replace("I", "ptri")
                our_func = our_func.replace("S", "ptrs")
                our_func = our_func.replace("N", "ptrn")
                our_func = our_func.replace("C", "ptrc")
                our_func = our_func.replace("E", "ptre")
                our_func = our_func.replace("Q", "ptrq")

                if "O" in count:
                    count = count.replace("O", "ptro")
                    print(count)
                    dif_virag = str(diff(our_func, count))  # дифференциируем выражение по переменным

                if "I" in count:
                    count = count.replace("I", "ptri")
                    print(count)
                    dif_virag = str(diff(our_func, count))  # дифференциируем выражение по переменным

                if "S" in count:
                    count = count.replace("S", "ptrs")
                    print(count)
                    dif_virag = str(diff(our_func, count))  # дифференциируем выражение по переменным

                if "N" in count:
                    count = count.replace("N", "ptrn")
                    print(count)
                    dif_virag = str(diff(our_func, count))  # дифференциируем выражение по переменным

                if "C" in count:
                    count = count.replace("C", "ptrc")
                    print(count)
                    dif_virag = str(diff(our_func, count))  # дифференциируем выражение по переменным

                if "E" in count:
                    count = count.replace("E", "ptre")
                    print(count)
                    dif_virag = str(diff(our_func, count))  # дифференциируем выражение по переменным

                if "Q" in count:
                    count = count.replace("Q", "ptrq")
                    print(count)
                    dif_virag = str(diff(our_func, count))  # дифференциируем выражение по переменным

                if count not in "OISNCEQ":
                    dif_virag = str(diff(our_func, count))  # дифференциируем выражение по переменным

                dif_virag = dif_virag.replace("ptro", "O",)
                dif_virag = dif_virag.replace("ptri", "I")
                dif_virag = dif_virag.replace("ptrs", "S")
                dif_virag = dif_virag.replace("ptrn", "N")
                dif_virag = dif_virag.replace("ptrc", "C")
                dif_virag = dif_virag.replace("ptre", "E")
                dif_virag = dif_virag.replace("ptrq", "Q")

                dif_virag = dif_virag.replace("{", "sin")  # меняем скобку на синус
                dif_virag = dif_virag.replace("}", "cos")  # меняем скобку на косинус
                dif_virag = dif_virag.replace("|", "tan")  # меняем палку на тангенс
                dif_virag = dif_virag.replace("<", "pi")  # меняем стрелочку на пи
                dif_virag = dif_virag.replace(">", "exp")  # меняем стрелочку на экспоненту

                if dif_virag != "0":
                    mas.append(dif_virag)  # добавляем продифференциированное выражение в массив\

    except:
        mas = []

    return mas


def set_var(virag, peremennii, znachenia):

    for count in range(len(peremennii)):
        virag = virag.replace("sin", "{")  # меняем синус на скобку
        virag = virag.replace("cos", "}")  # меняем косинус на скобку
        virag = virag.replace("tan", "|")  # меняем тангенс на палку
        virag = virag.replace("pi", "<")  # меняем пи на стрелочку
        virag = virag.replace("exp", ">")  # меняем экспоненту на стрелочку
        virag = virag.replace(peremennii[count], znachenia[count])
        virag = virag.replace("{", "sin")  # меняем скобку на синус
        virag = virag.replace("}", "cos")  # меняем скобку на косинус
        virag = virag.replace("|", "tan")  # меняем палку на тангенс
        virag = virag.replace("<", "pi")  # меняем стрелочку на пи
        virag = virag.replace(">", "exp")  # меняем стрелочку на экспоненту

    return "".join(virag)


if __name__ == "__main__":
    print(find_diff("OO**6+r**3", "OO r"))
