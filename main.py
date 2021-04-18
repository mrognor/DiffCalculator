from kivmob import KivMob, TestIds
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.core.clipboard import Clipboard
from backend import find_diff, set_var
from math import sin, cos, pi, exp, tan

mass_var = []  # в этом массиве будут храниться техтовые блоки, которы создаются динамически
mass_znach = []  # в цикле. Для получения доступа к их параметрам нужно обращаться к параметрам
mass_pogresh = []  # через точку


class MainWindow(BoxLayout):
    # используем глобальные переменные
    global mass_var  # массив имен переменных
    global mass_znach  # массив значений переменных
    global mass_pogresh  # массив остатков переменных

    try:
        locale_file_ru = open("localizations_ru.txt")
        mass_locale_ru = locale_file_ru.read().splitlines()

        locale_file_en = open("localizations_en.txt")
        mass_locale_en = locale_file_en.read().splitlines()
    except:
        pass

    if open("which_locale.txt").read() == "en":
        mass_locale = mass_locale_en
    if open("which_locale.txt").read() == "ru":
        mass_locale = mass_locale_ru

    box_layout_languages = BoxLayout()
    box_layout_languages.size_hint = [1, 0.4]

    button_russia = Button(text="Русский")
    button_english = Button(text="English")

    box_layout_languages.add_widget(button_russia)
    box_layout_languages.add_widget(button_english)

    box_layout_popup = BoxLayout()  # задаем переменную бокс лэйаут для попапа
    box_layout_popup.size_hint = [1, 1]  # задаем бокс лэйауту размер
    box_layout_popup.orientation = "vertical"  # задаем бокс лэйауту ориентацию
    box_layout_popup.add_widget(box_layout_languages)
    # добавляем в бокс лэйаут этикетку с текстом

    box_layout_popup.add_widget(Label(text=(mass_locale[0].split("//")[0] + "\n" + mass_locale[0].split("//")[1] + "\n" + mass_locale[0].split("//")[2] + "\n") + mass_locale[0].split("//")[3] + "\n" + mass_locale[0].split("//")[4] + "\n" + mass_locale[0].split("//")[5] + "\n" + mass_locale[0].split("//")[6] + "\n" + mass_locale[0].split("//")[7] + "\n" + mass_locale[0].split("//")[8] + "\n" + mass_locale[0].split("//")[9] + "\n"))
    # создаем кнопку для попапа
    button_copy = Button(text=mass_locale[1])
    button_copy.size_hint = [1, 0.4]
    box_layout_popup.add_widget(button_copy)  # добавляем кнопку в бокс лэйаут

    # создаем объект попапа
    popup = Popup(title=mass_locale[2], content=box_layout_popup, size_hint=[1, 0.7])

    # строка для вывода в буфер обмена
    to_clipboard = mass_locale[3]

    # задаем функцию обработки нажатия
    def calculate(self):

        variables = []  # создаем массивы для дальнейшего заполнения
        znachs = []  # текстом с текст инпута
        pogreshn = []  #

        for i in range(11):
            variables.append(mass_var[i].text)  # добавляем в массив названия переменных
            znachs.append(mass_znach[i].text.replace(",", "."))  # добавляем в массив значения переменных
            pogreshn.append(mass_pogresh[i].text.replace(",", "."))  # добавляем в массив погрешности

        self.ishodnoe_podstanovka_var.background_color = 1, 1, 1, 1  # сбрасываем цвет полей с
        self.diff_podstanovka_var.background_color = 1, 1, 1, 1  # ошибками
        self.diff_result_var.background_color = 1, 1, 1, 1
        self.ishodnoe_result_var.background_color = 1, 1, 1, 1
        self.diff_virag_var.background_color = 1, 1, 1, 1

        try:
            func = self.func_var.text.replace(",", ".")  # берем нашу функцию
            func = func.replace("^", "**")  # меняем запятые на точки, крышечки на **
            diff_func = find_diff(func, variables)  # дифференциируем нашу функцию

            self.ishodnoe_podstanovka_var.text = set_var(func, variables, znachs)  # выводим подстановку переменных в исходном выражении

            self.ishodnoe_result_var.text = str(eval(self.ishodnoe_podstanovka_var.text))  # считаем подстановку в исходное выражение

            mass_results = []  # массив для записи всех дифференциалов и подставноки туда переменных
            mass_diff = []

            for count in range(len(diff_func)):
                if pogreshn[count] != "0":
                    #mass_diff.append("((" + diff_func[count] + ")*" + pogreshn[count] + ")**2")
                    mass_diff.append("((" + diff_func[count] + ")*σ[" + variables[count] + "])**2")
                    mass_results.append(
                        set_var("((" + diff_func[count] + ")*" + pogreshn[count] + ")**2", variables, znachs))

            diff_result = 0  # переменная для записи результата

            for i in mass_results:
                diff_result += eval(i)  # возведенеи в квадрат каждого члена

            diff_result = diff_result ** 0.5  # извлечение корня из финального результата
            
            self.diff_virag_var.text = "(" + "+".join(mass_diff) + ")**0,5"
            self.diff_podstanovka_var.text = "(" + "+".join(
                mass_results) + ")**0,5"  # вывод подстановки дифференцированного выражения
            self.diff_result_var.text = str(diff_result)  # вывод результата подстановки дифференциированного выражения

            #  закидываем исходную формулу в строку
            self.to_clipboard += self.func_var.text + "\n"

            #  закидываем в цикле все величины в строку
            for i in range(len(variables)):
                if variables[i] != "":
                    if pogreshn[i] == "0":
                        self.to_clipboard += self.mass_locale[4] + variables[i] + self.mass_locale[5] + znachs[i] + self.mass_locale[6] + pogreshn[i] + "\n"
                    else:
                        self.to_clipboard += self.mass_locale[7] + variables[i] + self.mass_locale[8] + znachs[i] + self.mass_locale[9] + pogreshn[i] + "\n"

            #  засовываем в строку остальные величины
            self.to_clipboard += self.mass_locale[10]
            self.to_clipboard += self.mass_locale[11] + self.diff_virag_var.text + "\n"
            self.to_clipboard += self.mass_locale[12] + self.diff_podstanovka_var.text + "\n"
            self.to_clipboard += self.mass_locale[13] + self.diff_result_var.text
            self.to_clipboard += self.mass_locale[34]
            self.button_copy.on_release = self.to_bufer

        except SyntaxError:
            self.ishodnoe_podstanovka_var.text = self.mass_locale[14]
            self.diff_virag_var.text = self.mass_locale[15]
            self.diff_result_var.text = ""
            self.ishodnoe_result_var.text = ""
            self.ishodnoe_podstanovka_var.background_color = 255, 0, 0, 0.95
            self.ishodnoe_result_var.background_color = 255, 0, 0, 0.95

            self.diff_podstanovka_var.text = self.mass_locale[16]
            self.diff_podstanovka_var.background_color = 255, 0, 0, 0.95
            self.diff_result_var.background_color = 255, 0, 0, 0.95
            self.diff_virag_var.background_color = 255, 0, 0, 0.95

        except NameError:
            self.ishodnoe_podstanovka_var.text = self.mass_locale[17]
            self.ishodnoe_podstanovka_var.background_color = 255, 0, 0, 0.95
            self.ishodnoe_result_var.background_color = 255, 0, 0, 0.95

            self.diff_podstanovka_var.text = self.mass_locale[18]
            self.diff_virag_var.text = self.mass_locale[19]
            self.diff_result_var.text = ""
            self.ishodnoe_result_var.text = ""
            self.diff_podstanovka_var.background_color = 255, 0, 0, 0.95
            self.diff_result_var.background_color = 255, 0, 0, 0.95
            self.diff_virag_var.background_color = 255, 0, 0, 0.95

        except ZeroDivisionError:
            self.ishodnoe_podstanovka_var.text = self.mass_locale[20]
            self.ishodnoe_podstanovka_var.background_color = 255, 0, 0, 0.95
            self.ishodnoe_result_var.background_color = 255, 0, 0, 0.95

            self.diff_podstanovka_var.text = self.mass_locale[21]
            self.diff_virag_var.text = self.mass_locale[22]
            self.diff_result_var.text = ""
            self.ishodnoe_result_var.text = ""
            self.diff_podstanovka_var.background_color = 255, 0, 0, 0.95
            self.diff_result_var.background_color = 255, 0, 0, 0.95
            self.diff_virag_var.background_color = 255, 0, 0, 0.95

        except:
            self.ishodnoe_podstanovka_var.text = self.mass_locale[23]
            self.diff_virag_var.text = self.mass_locale[24]
            self.diff_result_var.text = ""
            self.ishodnoe_result_var.text = ""
            self.ishodnoe_podstanovka_var.background_color = 255, 0, 0, 0.95
            self.ishodnoe_result_var.background_color = 255, 0, 0, 0.95

            self.diff_podstanovka_var.text = self.mass_locale[25]
            self.diff_podstanovka_var.background_color = 255, 0, 0, 0.95
            self.diff_result_var.background_color = 255, 0, 0, 0.95
            self.diff_virag_var.background_color = 255, 0, 0, 0.95

    def show_popup(self):
        self.popup.open()  # функция спавна попапа

    def setlocale_ru(self):
        self.mass_locale = self.mass_locale_ru
        f = open("which_locale.txt", "w")
        f.write("ru")

    def setlocale_en(self):
        self.mass_locale = self.mass_locale_en
        f = open("which_locale.txt", "w")
        f.write("en")

    def to_bufer(self):
        Clipboard.copy(self.to_clipboard)  # функция для копирования переменной в буфер обмена

    def on_enter(self):
        self.button_russia.on_release = self.setlocale_ru
        self.button_english.on_release = self.setlocale_en

    def clean(self):
        self.func_var.text = ""

        self.ishodnoe_podstanovka_var.background_color = 1, 1, 1, 1  # сбрасываем цвет полей с
        self.diff_podstanovka_var.background_color = 1, 1, 1, 1  # ошибками
        self.diff_result_var.background_color = 1, 1, 1, 1
        self.ishodnoe_result_var.background_color = 1, 1, 1, 1
        self.diff_virag_var.background_color = 1, 1, 1, 1

        self.ishodnoe_podstanovka_var.text = self.mass_locale[26]
        self.diff_virag_var.text = self.mass_locale[27]
        self.diff_podstanovka_var.text = self.mass_locale[28]

        self.ishodnoe_result_var.text = self.mass_locale[29]
        self.diff_result_var.text = self.mass_locale[30]

        for i in range(11):
            mass_var[i].text = ""  # добавляем в массив названия переменных
            mass_znach[i].text = ""  # добавляем в массив значения переменных
            mass_pogresh[i].text = ""  # добавляем в массив погрешности


class DiffApp(App):
    #ads = KivMob(TestIds.APP)

    def build(self):
        #self.ads.new_banner(TestIds.BANNER, False)
        #self.ads.request_banner()
        #self.ads.show_banner()

        return MainWindow()

    def on_start(self):
        # используем глобальные переменные
        global mass_var  # массив имен переменных
        global mass_znach  # массив значений переменных
        global mass_pogresh  # массив погрешностей переменных

        self.root.on_enter()

        self.root.func_var.hint_text = self.root.mass_locale[39]
        self.root.button1_var.text = self.root.mass_locale[40]
        self.root.button2_var.text = self.root.mass_locale[41]
        self.root.button3_var.text = self.root.mass_locale[42]
        self.root.ishodnoe_podstanovka_var.text = self.root.mass_locale[43]
        self.root.ishodnoe_result_var.text = self.root.mass_locale[44]
        self.root.diff_virag_var.text = self.root.mass_locale[45]
        self.root.diff_podstanovka_var.text = self.root.mass_locale[46]
        self.root.diff_result_var.text = self.root.mass_locale[47]

        # цикл для заполнения скролл бокса полями ввода текста
        for i in range(11):
            # задание переменных
            text_input_var = TextInput()  # создаем переменную класса текст инпут
            mass_var.append(text_input_var)  # добавляем переменную в массив для дальнейшей работы
            self.root.variables_var.add_widget(text_input_var)  # добавляем переменную в гуи виджет
            text_input_var.hint_text = self.root.mass_locale[31]  # устанавливаем подсказку

            # задание значений переменных
            text_input_znach = TextInput()
            mass_znach.append(text_input_znach)
            self.root.znachs_var.add_widget(text_input_znach)
            text_input_znach.hint_text = self.root.mass_locale[32]

            # задание погрешностей переменных
            text_input_pogreshn = TextInput()
            mass_pogresh.append(text_input_pogreshn)
            self.root.pogreshns_var.add_widget(text_input_pogreshn)
            text_input_pogreshn.hint_text = self.root.mass_locale[33]


if __name__ == "__main__":
    DiffApp().run()
