#Обновлено: баги чинили

import time, copy, random, sys, math
from threading import Timer
sys.setrecursionlimit(10000)

class Number:
    def __init__(self, num):
        self.__length = 0
        self.__isBanned = 0
        self.__savedCurrent = {}

        if type(num) == str:
            if num[:3] == "gen":
                self.__randomGenerate(int(num.split('-')[1]))
            else:
                self.__number = self.__createNum(num)
                self.__current = self.__number["number"]
        else:
            self.__number = num["link"]
            if "current" in num:
                self.__current = num["current"]
            else:
                self.__current = self.__number["number"]

    def __randomGenerate(self, length):
        self.__number = self.__createNum("0")
        self.__current = self.__number["number"]
        for i in range(length):
            if i == length - 1:
                num = random.randint(1, 9)

            else:
                num = random.randint(0, 9)
            if i == 0:
                self.updateN(num)
            else:
                self.addToHead(num)

    def __correctFigure(self, n, methodName = ""):
        if type(n) != int:
            raise Exception("Метод {} принимает параметр типа int. Был получен {}".format(methodName, str(type(n))))
        if n < 0 or n > 9:
            raise Exception("Попытка установить недопустимое значение для цифры ({}).".format(str(n)))

    def __permitChecker(self):
        if self.__isBanned == 1:
            raise Exception("Работа c данным объектом класса запрещена: был передан указатель на объект числа.")

    def __createNum(self, num):
        number = {
            "data": {
                "sign": "+",
                "mainHead": "", #link
            },
            "number": {
                "n": "",        #int
                "head": "",     #link
                "tail": "",     #link
            }
        }

        current = number["number"] #указатель на объект со значением первой цифры в числе (мы идём с десятков, т.е. от меньшего к большему)
        current["tail"] = None     #У первого элемента хвоста нет

        #обрабатываем наличие знаков.
        if num[0] == '-':
            number["data"]["sign"] = "-"
            isSigned = 1 #поможет нам игнорировать знак при создании объектов с цифрами числа
        elif num[0] == "+":
            isSigned = 1 #поможет нам игнорировать знак при создании объектов с цифрами числа
        else:
            isSigned = 0 #поможет нам игнорировать знак при создании объектов с цифрами числа

        # если в числе есть знак, то нам нужно его проигнорировать, когда мы будем создавать объекты с цифрами.
        # так как мы идём с конца строки (читаем мы слева направо, а самый самый маленький разряд самый правый, т.е. перебор
        # строки идёт справа налево), и если мы хотим проигнорировать последний элемент (знак), то просто сделаем на 1 итерацию меньше.
        # Т.е. для этого и нужен флаг isSigned

        for i in range(len(num) - isSigned):
            try:
                current["n"] = int(num[len(num) - i - 1]) #идём с конца строки и присваиваем значению ("n") текущего объекта цифру
            except ValueError:
                raise Exception("Число может содержать только цифры! Проблема с симвовлом {}, Было передано {}".format(num[len(num) - i - 1], num))
            self.__length += 1
            if i == len(num) - 1 - isSigned: # Если число со знаком, то и "отрубить голову" нужно на 1 итерацию раньше.
                current["head"] = None
            else:
                current["head"] = {}   #создаём в голове текущего объекта объект.
                current["head"]["tail"] = current #создаём в голове текущего объекта поле хвоста и присваиваем указатель на текущий объект.
                current = current["head"]  #обновляем текущий объект
        number["data"]["mainHead"] = current #создаём указатель на главную голову (крайнее левое число, т.е. самый большой разряд)
        return number


    def saveCurPos(self):
        time.sleep(0.000001)
        key = str(time.time())
        self.__savedCurrent[key] = self.__current
        return key

    def recoverCurPos(self, key):
        if key in self.__savedCurrent:
            self.__current = self.__savedCurrent[key]
            del self.__savedCurrent[key]
        else:
            raise Exception("Попытка восстановить значение указателя по несуществующему ключу!")

    def show(self, setup = ""):
        self.__permitChecker()
        number = ""
        current = self.__number["data"]["mainHead"]  # указатель на объект головы числа, т.е. самого большого разряда.

        if (self.__number["data"][
            "sign"] == "-" and setup != "get_abs"):  # Если число отрицательное, то добавляем минус. Если положительное, то игнор.
            number += self.__number["data"]["sign"]
        number += str(current["n"])  # Прибавляем к строке значение головы.

        while current["tail"] != None:  # Проверяем, если ховст есть, то прибавляем к строке следующую цифру
            current = current["tail"]  # указатель на объект предыдущей цифры.
            number += str(current["n"])
        if setup != "get" and setup != "get_abs":
            print(int(number))
        else:
            return int(number)

    def showN(self):
        self.__permitChecker()
        print(self.__current["n"])

    def next(self, times = 1):
        self.__permitChecker()
        i = 0
        response = 0
        stop = 0
        while i < times and not stop:
            if self.__current["head"] != None:
                self.__current = self.__current["head"]
                response = 1
            else:
                stop = 1
                response = 0
            i += 1
        return response

    def before(self, times = 1):
        self.__permitChecker()
        i = 0
        response = 0
        stop = 0
        while i < times and not stop:
            if self.__current["tail"] != None:
                self.__current = self.__current["tail"]
                response = 1
            else:
                stop = 1
                response = 0
            i += 1
        return response

    def toHead(self):
        self.__permitChecker()
        self.__current = self.__number["data"]["mainHead"]

    def toTail(self):
        self.__permitChecker()
        self.__current = self.__number["number"]

    def getN(self):
        self.__permitChecker()
        return self.__current["n"]

    def getSign(self):
        self.__permitChecker()
        sign = 0
        if self.__number["data"]["sign"] == "-":
            sign = 1
        return sign

    def updateSign(self, sign):
        self.__permitChecker()
        if sign == 0 or sign == 1:
            if sign == 0:
                self.__number["data"]["sign"] = "+"
            else:
                self.__number["data"]["sign"] = "-"
        else:
            raise Exception("Попытка установить некорректное значение знака! (0 = '+', 1 = '-')")

    def updateN(self, n):
        self.__permitChecker()
        self.__correctFigure(n, "updateN")
        self.__current["n"] = n

    def addToHead(self, n):
        self.__permitChecker()
        self.__correctFigure(n, "addToHead")
        self.__number["data"]["mainHead"]["head"] = {
            "n": n,
            "head": None,
            "tail": self.__number["data"]["mainHead"]
        }
        self.__number["data"]["mainHead"] = self.__number["data"]["mainHead"]["head"]
        self.__length += 1

    def addToTail(self, n):
        self.__permitChecker()
        self.__correctFigure(n, "addToTail")
        self.__number["number"] = {
            "n": n,
            "head": self.__number["number"],
            "tail": None,
        }
        self.__number["number"]["head"]["tail"] = self.__number["number"]
        self.__length += 1

    def remove(self):
        self.__permitChecker()
        if self.__current["tail"] == None:
            if self.__current["head"] == None:
                raise Exception("Попытка удалить едиственный элемент числа")
            else:
                self.__number["number"] = self.__current["head"]
                self.__current = self.__current["head"]
                self.__current["tail"] = None
                self.__current["mainHead"] = self.__current
                self.__length -= 1

        elif self.__current["head"] == None:
            if self.__current["tail"] == None:
                raise Exception("Попытка удалить едиственный элемент числа")
            else:
                self.__current["tail"]["head"] = None
                self.__current = self.__current["tail"]
                self.__number["data"]["mainHead"] = self.__current
                # if self.__current["n"] == 0:
                #     self.zeroClear()
                self.__length -= 1
        else:
            raise Exception("Попытка удалить срединный элемент числа")

    def sremove(self):                           ###когда удаляем элемент, указатель уходит НАЗАД, т.е. на 1 к меньшему
        self.__permitChecker()
        if self.__current["tail"] == None:
            if self.__current["head"] == None:
                raise Exception("Попытка удалить едиственный элемент числа")
            else:
                self.__number["number"] = self.__current["head"]
                self.__current = self.__current["head"]
                self.__current["tail"] = None
                self.__current["mainHead"] = self.__current
                self.__length -= 1
        elif self.__current["head"] == None:
            if self.__current["tail"] == None:
                raise Exception("Попытка удалить едиственный элемент числа")
            else:
                self.__current["tail"]["head"] = None
                self.__current = self.__current["tail"]
                self.__number["data"]["mainHead"] = self.__current
                self.__length -= 1
        else:
            self.__current["tail"]["head"] = self.__current["head"]
            self.__current["head"]["tail"] = self.__current["tail"]
            self.__current = self.__current["tail"]
            self.__length -= 1

    def isNextAvailable(self):
        self.__permitChecker()
        return int(self.__current["head"] != None)

    def isBeforeAvailable(self):
        self.__permitChecker()
        return int(self.__current["tail"] != None)

    def zeroClear(self):
        self.__permitChecker()
        self.toHead()
        result = 0
        if self.isNextAvailable() == 0 and self.isBeforeAvailable() and self.getN() == 0:
            result = 1
            self.remove()
            if self.getN() == 0 and self.isBeforeAvailable():
                self.zeroClear()
        return result

    def length(self):
        return self.__length

    def getNumberCopy(self):
        return copy.deepcopy(self.__number)

class Polynomial:
    def __init__(self, polynom):
        self.__length = 0
        self.__savedCurrent = {}

        if type(polynom) == str:
            if polynom[:3] == "gen":
                self.__randomPolynomGenerate(int(polynom.split('-')[1]), polynom.split('-')[2])
        elif type(polynom) == list:
            polynom = self.__sortRecievedPolynom(polynom)
            self.__polynom = self.__createPol(polynom)
            self.__current = self.__polynom["polynom"]
        else:
            raise Exception("Попытка создать полином с неподдерживаемым типом аргумента ({})".format(type(polynom)))


    def __randomPolynomGenerate(self, lenPol, maxLenNum):

        if maxLenNum != "misha":
            maxLenNum = int(maxLenNum)

        self.__polynom = self.__createPol([[[Number("1"), Number("1")], 1]])
        self.__current = self.__polynom ["polynom"]
        for i in range(lenPol):
            if maxLenNum == "misha":
                num1 = Number("1")
                num2 = Number("1")
            else:
                num1 = Number("gen-{}".format(random.randint(1, maxLenNum)))
                num2 = Number("gen-{}".format(random.randint(1, maxLenNum)))
            num1.updateSign(random.randint(0, 1))
            if i == 0:
                self.updateN([[num1, num2], i])
            else:
                self.addToHead([[num1, num2], i])


    def __sortRecievedPolynom(self, pol):
        def partition(nums, low, high):
            # Выбираем средний элемент в качестве опорного
            # Также возможен выбор первого, последнего
            # или произвольного элементов в качестве опорного
            pivot = pol[(low + high) // 2]
            i = low - 1
            j = high + 1
            while True:
                i += 1
                while pol[i][1] < pivot[1]:
                    i += 1

                j -= 1
                while nums[j][1] > pivot[1]:
                    j -= 1

                if i >= j:
                    return j

                # Если элемент с индексом i (слева от опорного) больше, чем
                # элемент с индексом j (справа от опорного), меняем их местами
                nums[i], nums[j] = nums[j], nums[i]


        def quick_sort(pol):
            # Создадим вспомогательную функцию, которая вызывается рекурсивно
            def _quick_sort(items, low, high):
                if low < high:
                    # This is the index after the pivot, where our lists are split
                    split_index = partition(items, low, high)
                    _quick_sort(items, low, split_index)
                    _quick_sort(items, split_index + 1, high)

            _quick_sort(pol, 0, len(pol) - 1)

        quick_sort(pol)
        return pol

    def __analyzeSign(self, fraction):
        if fraction[0].getSign() == 0:
            if fraction[1].getSign() == 1:
                sign = 1
            else:
                sign = 0
        else:
            if fraction[1].getSign() == 1:
                sign = 0
            else:
                sign = 1
        return sign


    def __createPol(self, pol):
        polynom = {
            "data": {
                "mainHead": "", #link
            },
            "polynom": {
                "n": "",        #arr [Number, Number]
                "sign": "",     # 0 / 1
                "deg": "",      #int
                "head": "",     #link
                "tail": "",     #link
            }
        }

        current = polynom["polynom"] #указатель на объект со значением первой цифры в числе (мы идём с десятков, т.е. от меньшего к большему)
        current["tail"] = None     #У первого элемента хвоста нет

        for i in range(len(pol)):
            current["n"] = pol[i][0] #идём с начала отсоритрованного массива и присваиваем значению ("n") текущую дробь\
            try:
                current["deg"] = int(pol[i][1])
            except ValueError:
                raise Exception("Попытка установить некорректное значение степени элемента многочлена ({}).".format(pol[i][1]))

            current["sign"] = self.__analyzeSign(pol[i][0])

            self.__length += 1
            if i == len(pol) - 1:
                current["head"] = None
            else:
                current["head"] = {}   #создаём в голове текущего объекта объект.
                current["head"]["tail"] = current #создаём в голове текущего объекта поле хвоста и присваиваем указатель на текущий объект.
                current = current["head"]  #обновляем текущий объект
        polynom["data"]["mainHead"] = current #создаём указатель на главную голову (крайнее левое число, т.е. самый большой разряд)
        return polynom


    def __correctElem(self, el, methodName = ""):
        try:
            int(el[1])
        except ValueError:
            raise Exception("Попытка установить некорректное значение степени элемента многочлена ({}).".format(el[1]))

        if type(el[0]) != list:
            raise Exception(
                "Попытка установить некорректное значение коэффициента многочлена. Ожидается list ([num1, num2]), получен {}".format(type(el[0])))

        if type(el[0][0]) != Number or type(el[0][1]) != Number:
            raise Exception("Попытка установить некорректное значение для коэффицинта многочлена.\nНеобходим класс Number,"
                            "Получен ({} и {])".format(type(el[0][0]), type(el[0][1])))
        if el[0][1].getN() == 0 and el[0][1].isNextAvailable() == 0:
            raise Exception("Попытка установить некорректное значение знаменателя! Не может быть равным нулю")

        if el[0][1].getSign() == 1:
            raise Exception("Попытка установить отрицательный знаменатель! Равнен {}".format(el[0][1].show("get")))

    def saveCurPos(self):
        time.sleep(0.000001)
        key = str(time.time())
        self.__savedCurrent[key] = self.__current
        return key

    def recoverCurPos(self, key):
        if key in self.__savedCurrent:
            self.__current = self.__savedCurrent[key]
            del self.__savedCurrent[key]
        else:
            raise Exception("Попытка восстановить значение указателя по несуществующему ключу!")

    def getN(self):
        return self.__current["n"]

    def getDeg(self):
        return self.__current["deg"]

    def getSign(self):
        return self.__current["sign"]

    def show(self, setup=""):
        polynom = ""
        current = self.__polynom["data"]["mainHead"]  # указатель на объект головы числа, т.е. самого большого разряда.
        if setup == "get":
            polynom = []

        isFirstTime = 1

        def inner():
            curElement = ""
            if current["sign"] == 1:
                curElement += " - "
            else:
                if isFirstTime != 1:
                    curElement += " + "
            if setup != "get":
                curElement += "({}/{})*X^{}".format(current["n"][0].show("get_abs"), current["n"][1].show("get_abs"),
                                                    current["deg"])
            else:
                curElement = ([[str(current["n"][0].show("get")), str(current["n"][1].show("get"))], current["deg"]])
            return curElement

        if setup != "get":
            polynom += inner()
        else:
            polynom.append(inner())

        isFirstTime = 0

        while current["tail"] != None:  # Проверяем, если ховст есть, то прибавляем к строке следующую цифру
            current = current["tail"]  # указатель на объект предыдущей цифры.

            if setup != "get":
                polynom += inner()
            else:
                polynom.append(inner())

        if setup != "get":
            print(polynom)
        else:
            return polynom

    def showN(self):
        curElement = ""
        if (self.__current["sign"] == 1):
            curElement += " - "

        curElement += "({}/{})*X^{}".format(self.__current["n"][0].show("get_abs"), self.__current["n"][1].show("get_abs"),
                                            self.__current["deg"])
        print(curElement)

    def next(self, times=1):
        i = 0
        response = 0
        stop = 0
        while i < times and not stop:
            if self.__current["head"] != None:
                self.__current = self.__current["head"]
                response = 1
            else:
                stop = 1
                response = 0
            i += 1
        return response

    def before(self, times=1):
        i = 0
        response = 0
        stop = 0
        while i < times and not stop:
            if self.__current["tail"] != None:
                self.__current = self.__current["tail"]
                response = 1
            else:
                stop = 1
                response = 0
            i += 1
        return response

    def toHead(self):
        self.__current = self.__polynom["data"]["mainHead"]

    def isNextAvailable(self):
        return int(self.__current["head"] != None)

    def isBeforeAvailable(self):
        return int(self.__current["tail"] != None)

    def toTail(self):
        self.__current = self.__polynom["polynom"]

    def length(self):
        return self.__length

    def remove(self):            ###когда удаляем элемент, указатель уходит НАЗАД, т.е. на 1 к меньшему
        if self.__current["tail"] == None:
            if self.__current["head"] == None:
                raise Exception("Попытка удалить едиственный элемент полинома")
            else:
                self.__polynom["polynom"] = self.__current["head"]
                self.__current = self.__current["head"]
                self.__current["tail"] = None
                self.__current["mainHead"] = self.__current
                self.__length -= 1
        elif self.__current["head"] == None:
            if self.__current["tail"] == None:
                raise Exception("Попытка удалить едиственный элемент полинома")
            else:
                self.__current["tail"]["head"] = None
                self.__current = self.__current["tail"]
                self.__polynom["data"]["mainHead"] = self.__current
                self.__length -= 1
        else:
            self.__current["tail"]["head"] = self.__current["head"]
            self.__current["head"]["tail"] = self.__current["tail"]
            self.__current = self.__current["tail"]
            self.__length -= 1


    def updateN(self, el):
        self.__correctElem(el)

        def innerUpdate():
            self.__current["n"] = el[0]
            self.__current["sign"] = self.__analyzeSign(el[0])
            self.__current["deg"] = int(el[1])

        if self.__current["head"] != None:
            if self.__current["tail"] != None:
                if self.__current["tail"]["deg"] <= el[1] and self.__current["head"]["deg"] >= el[1]:
                    innerUpdate()
                else:
                    raise Exception("Невозможно обновить данный элемент. Нарушится сортировка")
            else:
                if self.__current["head"]["deg"] >= el[1]:
                    innerUpdate()
                else:
                    raise Exception("Невозможно обновить данный элемент. Нарушится сортировка")
        else:
            if self.__current["tail"] != None:
                if self.__current["tail"]["deg"] <= el[1]:
                    innerUpdate()
                else:
                    raise Exception("Невозможно обновить данный элемент. Нарушится сортировка")
            else:
                innerUpdate()

    def updateSign(self, sign):
        if sign == 0 or sign == 1:
            self.__current["sign"] = sign
            self.__current["n"][0].updateSign(sign)
        else:
            raise Exception("Попытка установить некорректное значение знака! (0 = '+', 1 = '-')")

    def insert(self, el):
        current = self.__polynom["polynom"]

        if self.__polynom["data"]["mainHead"]["deg"] < el[1]:

            self.addToHead(el)

        else:
            while current != None:
                if(current["deg"] >= el[1]):
                    if current["deg"] > el[1]:
                        tail = current["tail"]
                        if tail != None:
                            current["tail"] = {
                                "n": el[0],
                                "sign": self.__analyzeSign(el[0]),
                                "deg": el[1],
                                "tail": tail,
                                "head": current,
                            }
                            tail["head"] = current["tail"]
                            self.__length += 1
                        else:
                             self.addToTail(el)
                        break
                    else:
                        current["n"] = ADD_QQ_Q(current["n"], el[0])
                        current["sign"] = self.__analyzeSign(current["n"])
                        break
                current = current["head"]

    def addToHead(self, el):
        self.__correctElem(el)
        if(self.__polynom["data"]["mainHead"] != None):
            if (self.__polynom["data"]["mainHead"]["deg"] > el[1] ):
                raise Exception("Добавление элемента многочлена в неположенном месте")

        self.__polynom["data"]["mainHead"]["head"] = {
            "n": el[0],
            "sign": self.__analyzeSign(el[0]),
            "deg": int(el[1]),
            "head": None,
            "tail": self.__polynom["data"]["mainHead"]
        }
        self.__polynom["data"]["mainHead"] = self.__polynom["data"]["mainHead"]["head"]
        self.__length += 1

    def addToTail(self, el):
        self.__correctElem(el)

        if (self.__polynom["polynom"]["deg"] < el[1]):
            raise Exception("Добавление элемента многочлена в неположенном месте")

        self.__polynom["polynom"] = {
            "n": el[0],
            "sign": self.__analyzeSign(el[0]),
            "deg": int(el[1]),
            "head": self.__polynom["polynom"],
            "tail": None,
        }
        self.__polynom["polynom"]["head"]["tail"] = self.__polynom["polynom"]
        self.__length += 1

    def zeroClear(self):
        pos = self.saveCurPos()
        self.toHead()
        result = 0
        for i in range(self.__length):
            if self.getN()[0].getN() == 0 and (self.isBeforeAvailable() or self.isNextAvailable()):
                result = 1
                self.remove()
            else:
                self.before()
        self.recoverCurPos(pos)
        return result


def speedTest(func, setup = ""):
    if setup != "silent":
        print("Test has started...")
    timeStart = time.time()
    func()
    timeEnd = time.time()
    if setup != "silent":
        print("Time is: ", timeEnd - timeStart)
    return timeEnd - timeStart

def compileNum(num):
    number = ""
    current = num["data"]["mainHead"] #указатель на объект головы числа, т.е. самого большого разряда.
    if(num["data"]["sign"] == "-"):  #Если число отрицательное, то добавляем минус. Если положительное, то игнор.
        number += num["data"]["sign"]
    number += str(current["n"])        #Прибавляем к строке значение головы.

    while current["tail"] != None: #Проверяем, если ховст есть, то прибавляем к строке следующую цифру
        current = current["tail"] #указатель на объект предыдущей цифры.
        number += str(current["n"])

    return number

#Функция, которая создаёт число. Поддерживает целые и натуральные. На выходе - указатель на объект обёртки числа.
def createNum(num):
    number = {
        "data": {
            "sign": "+",
            "point": "",    #number
            "mainHead": "", #link
        },
        "number": {
            "n": "",        #int
            "head": "",     #link
            "tail": "",     #link
        }
    }

    current = number["number"] #указатель на объект со значением первой цифры в числе (мы идём с десятков, т.е. от меньшего к большему)
    current["tail"] = None     #У первого элемента хвоста нет

    #обрабатываем наличие знаков.
    if num[0] == '-':
        number["data"]["sign"] = "-"
        isSigned = 1 #поможет нам игнорировать знак при создании объектов с цифрами числа
    elif num[0] == "+":
        isSigned = 1 #поможет нам игнорировать знак при создании объектов с цифрами числа
    else:
        isSigned = 0 #поможет нам игнорировать знак при создании объектов с цифрами числа

    # если в числе есть знак, то нам нужно его проигнорировать, когда мы будем создавать объекты с цифрами.
    # так как мы идём с конца строки (читаем мы слева направо, а самый самый маленький разряд самый правый, т.е. перебор
    # строки идёт справа налево), и если мы хотим проигнорировать последний элемент (знак), то просто сделаем на 1 итерацию меньше.
    # Т.е. для этого и нужен флаг isSigned

    for i in range(len(num) - isSigned):
        current["n"] = int(num[len(num) - i - 1]) #идём с конца строки и присваиваем значению ("n") текущего объекта цифру
        if i == len(num) - 1 - isSigned: # Если число со знаком, то и "отрубить голову" нужно на 1 итерацию раньше.
            current["head"] = None
        else:
            current["head"] = {}   #создаём в голове текущего объекта объект.
            current["head"]["tail"] = current #создаём в голове текущего объекта поле хвоста и присваиваем указатель на текущий объект.
            current = current["head"]  #обновляем текущий объект
    number["data"]["mainHead"] = current #создаём указатель на главную голову (крайнее левое число, т.е. самый большой разряд)
    return number

def numCopy(num):
    return copy.deepcopy(num)


#Является ли число нулём.
def NZER_N_B(num):
    res = 0
    num.toTail()
    if num.getN() == 0 and num.isNextAvailable() == 0:#У нуля в значении ('n') ноль, а головы нет
        res = 1
    return res

#умножает на 10 в степени n
def MUL_Nk_N(num, multiplier):
    for i in range(multiplier):
        num.addToTail(0)
    return num

#Занимает единичку из разрядов выше
def borrow(num):
    response = 0
    if num.next() != 0:
        if num.getN() > 0:
            response = 10
            num.updateN(num.getN() - 1)
            if num.getN() == 0 and num.isNextAvailable() == 0:
                num.remove()
            else:
                num.before()
        else:
            response = borrow(num)
            if response > 0:
                num.updateN(9)
            num.before()
    return response

#сравнение целых чисел
def COM_NN_D(num1, num2):
    res = 0
    if num1.getSign() != num2.getSign():
        if num1.getSign() > num2.getSign():
            res = 1
        else:
            res = 2
    else: #знаки равны
        if num1.length() == num2.length(): #если длины равны
            sign = num1.getSign() #сохраняем знак + или -, - это важно
            isFinish = False
            num1.toHead()
            num2.toHead()
            while not isFinish:
                if num1.getN() != num2.getN():
                    isFinish = True
                    if sign == 0: # если плюс, то какое число больше, то и больше
                        if num1.getN() > num2.getN():
                            res = 2
                        else:
                            res = 1
                    else: # если минус, то какое число меньше, то и меньше
                        if num1.getN() < num2.getN():
                            res = 2
                        else:
                            res = 1

                else:
                    if num1.before() == 0 or num2.before() == 0:
                        isFinish = True

        else:
            sign = num1.getSign()
            if sign == 0:
                if num1.length() > num2.length():
                    res = 2
                else:
                    res = 1
            else:
                if num1.length() < num2.length():
                    res = 2
                else:
                    res = 1
    return res

#Вычитание двух натуральных чисел (первое больше второго)
def SUB_NN_N(num1, num2):
    if COM_NN_D(num1, num2) == 2 or COM_NN_D(num1, num2) == 0:
        lowFlag = 1
        num1.toTail()
        num2.toTail()

        while lowFlag == 1:
            result = num1.getN() - num2.getN()
            if result > 0:
                num1.updateN(result)
            elif result == 0:
                if (num1.isNextAvailable() == 0 and num1.isBeforeAvailable()):
                    num1.remove()
                    num1.zeroClear()
                else:
                    num1.updateN(result)

            else:
                borrRes = borrow(num1)
                if borrRes == 10:
                    num1.updateN(result + 10)
                else:
                    lowFlag = 0
                    highFlag = 0
            next1 = num1.next()
            next2 = num2.next()
            if next1 == 0 or next2 == 0:
                lowFlag = 0
        return num1
    else:
        return -1

#Вычитание из натурального другого натурального, умноженного на цифру для случая с неотрицательным результатом.
#Если мнодитель будет слишком большим (доведёт до отрицательного результата), функция вернёт -1, иначе резульат

def SUB_NDN_N(num1, num2, multiplier):
    error = 0
    for i in range(multiplier):
        if COM_NN_D(num1, num2) == 2:
            SUB_NN_N(num1, num2)
        else:
            error = 1
            break
    if error == 1:
        return -1
    else:
        return num1

#Функция складывает натуральные числа, результат запиываетс в большее из чисел. Вернёт -1, если числа не натуральные
def ADD_NN_N(num1, num2):
    key = COM_NN_D(num1, num2)
    if key == 1 or key == 0:  #0 - если числа равны, 1 - если 2-е больше
        #здесь записываем значение большего числа в num1, а меньшего в num2
        k = num1
        num1 = num2
        num2 = k
    num1.toTail()
    num2.toTail()
    if num1.getSign() == 0 and num2.getSign() == 0:    #проверка на неотрицательность чисел
        m = 0  #здесь будет хранится 1,если сумма цифр будет больше 10, т.е. переход через разряд
        while num1.isNextAvailable() and num2.isNextAvailable():  #пока доступна следующая цифра в двух числах
            sum = (num1.getN()+num2.getN()+m) % 10
            if (num1.getN()+num2.getN()+m) >= 10:
                m = 1
            else:
                m = 0
            num1.updateN(sum)
            num1.next()
            num2.next()
        sum = (num1.getN() + num2.getN() + m) % 10
        if (num1.getN() + num2.getN() + m) >= 10:
            m = 1
        else:
            m = 0
        num1.updateN(sum)
        while num1.isNextAvailable():  #пока доступна следующая цифра в большем числе
            num1.next()
            sum = (num1.getN() + m) % 10
            if (num1.getN()+m) >= 10:
                m = 1
            else:
                m = 0
            num1.updateN(sum)
        if m == 1:
            num1.addToHead(1)
        return num1
    else:
        return -1

#Прибавить единичку
def ADD_1N_N(num):
    count_nine = 0
    len = 1
    while(num.next(1) != 0):
        len += 1
    num.toTail()
    try:
        while num.getN() == 9:
            num.updateN(0)
            count_nine += 1
            if len == count_nine:
                num.addToHead(0)
                num.toHead()
            else:
                num.next()
        my_num = num.getN()
        num.updateN(my_num + 1)
        num.zeroClear()
        return num
    except:
        return -1


#Абсолютная величина числа, результат - натуральное
def ABS_Z_N(nom):
    nom.updateSign(0)
    return nom

# Умножение целого на (-1)
def MUL_ZM_Z(nom):
    f = nom.next()
    if (f == 0):
        if (nom.getN() == 0):
            return nom
    nom.toTail()
    if (nom.getSign() == 0):

        nom.updateSign(1)
        return nom
    else:

        nom.updateSign(0)
        return nom

#Определение положительности числа (2 - положительное, 0 — равное нулю, 1 - отрицательное)
def POZ_Z_D(nom):
    f=nom.next()
    if(f==0):
        if(nom.getN()==0):
            return 0
    nom.toTail()
    if (nom.getSign()==0):
        return 2
    else:
        return 1

__content = {
    "MUL_Nk_N": "Умножает число на 10 в степени n. На вход получает число и n - степень числа 10. Возвращает число",
    "borrow": "Занимает единичку у большего разряда (нужно при вычитании). На вход получает число. "
              "Возвращает 10, если операция удалась, 0, если нет",
    "COM_NN_D": "Сравнивает 2 числа. На вход получает 2 числа. Возвращает 1, если второе число больше, 2, если 1 число больше, 0, если равны",
    "INT_Q_B": "Определяет, является рациональное число целым. На вход получает 2 числа. Возвращает 1, если число целое, 0, если нет",
    "SUB_NN_N": "Вычитает из большего натурального меньшее. На вход получает 2 числа. Возвращает 1 число",
    "NZER_N_B": "Явялется ли число нулём. На вход получает число. Возвращает 1, если число есть ноль, 0, если нет",
    "ADD_NN_N": "Сложение двух натуральных чисел. На вход получает 2 числа. (спорно) Возвращает результат сложения",
    "DIV_NN_N": "Частное от деления большего натурального числа на меньшее или равное с остатком. На вход получает два числа. Возвращает результат",
    "ADD_1N_N": "Прибавляет единичку к натуральному числу. На вход получает число. Возвращает изменённое число",
    "MOD_NN_N": "Остаток от деления целых чисел. На вход принимает 2 числа. Возвращает изменённое первое число - остаток от деления.",
    "ABS_Z_N": "Абсолютная величина числа. На вход принимает число. Возвращает число с обновлённым знаком",
    "MUL_ZM_Z": "Умножение целого на (-1). На вход принимает число. Возвращет число с изменённым знаком",
    "POZ_Z_D": "Определение положительности числа. На вход получает число. Возвращает 2 - положительное, 0 — равное нулю, 1 - отрицательное",
    "SUB_NDN_N": "Вычитание из натурального другого натурального, умноженного на цифру для случая с неотрицательным результатом" +
    "На вход получает 2 числа и третим параметром множитель для второго числа. Если множитель будет слишком большим"
    "(доведёт до отрицательного результата), функция вернёт -1, иначе результат",
    "MUL_ND_N": "Умножение натурального числа на цифру. На вход принимает число и цифру (обычную). Возвращает число, -1, если была передана не цифра",
    "MUL_NN_N": "Умножение натуральных чисел. На вход получает 2 числа. Возвращает новый экземпляр класса числа.",
    "DIV_NN_Dk": " Вычисление первой цифры деления большего натурального на меньшее, домноженное на 10^k,где k - номер позиции этой цифры (номер считается с нуля). "
                 "На вход получает 2 числа. Возвращает новый экземпляр класса, или -1, если хоть один аргумент = 0",
    "GCF_NN_N": "НОД натуральных чисел, на вход получает 2 числа, возвращает результат - число. Изменяет полученные данные",
    "TRANS_N_Z": "Натуральное в целое - пустышка. На вход принимает число, возвращает его же",
    "ADD_ZZ_Z": "Сложение целых чисел. На вход принимает два числа. Изменяет входные данные (1 число). Возворащает число - результат",
    "SUB_ZZ_Z": "Вычитание целых чисел. На вход принимает 2 числа. Изменяет входные данные (1 число). Возвращает число - результат",
    "MUL_ZZ_Z": "Умножение целых чисел. На вход принимает 2 числа. Не изменяет водные данные. Возвращает новый экземпляр числа - роезультат",
    "LCM_NN_N": "НОК натуральных чисел. На вход принимает 2 числа. Изменяет входные данные. Возвращает число типа int",
    "ADD_QQ_Q": "Сложение дробей. На вход принимает 2 дроби. Возвращает дробь",
    "RED_Q_Q": "Сокращение дроби. На вход получает дробь. Возвращает дробь. Изменяет входные данные",
    "TRANS_Q_Z": "Преобразование дробного в целое. На вход получает дробь. Возвращает числитель, если знам == 1, иначе -1",
    "SUB_QQ_Q": "Вычитание дробей. На вход получает 2 дроби. Возвращает новую дробь или -1, если хоть 1 знаменатель отрицательный. НЕ изменяет данные",
    "MUL_QQ_Q":"Умножение дробей. На вход получает 2 дроби. Возвращает изменённую первую дробь или -1. Изменяет данные",
    "DIV_QQ_Q":"Деление дробей. На вход получает 2 дроби. Возвращает новую дробь или int = 0. Изменяет входные данные",
    "ADD_PP_P": "Сложение многочленов. На вход получает 2 многочлена. Возвращает новый многочлен - результат. Не изменяет входные данные",
    "SUB_PP_P":"Сложение многочленов. На вход получает 2 многочлена. Возвращает новый многочлен - результат. Не изменяет входные данные",
    "MUL_PQ_P":"Умножение многочлена на рациональное число. На вход получает многочлен и число. Возвращает новый многочлен. Не изменяет входные данные",
    "MUL_Pxk_P":"Умножение многочлена на x^k. На вход получает многочлен и число - степень x. Возвращает новый многочлен. Не изменяет входные данные",
    "LED_P_Q":"Старший коэффициент многочлена. На вход получает многочлен. Вовзвращает дробь - рациональность типа [Number, Number]. Не изменяет входные данные",
    "DEG_P_N":"Cтепень многочлена. На вход получает многочлен. Возвращает число типа Number. Не изменяет входные данные",
    "FAC_P_Q":"Вынесение из многочлена НОК знаменателей коэффициентов и НОД числителей. На вход получает многочлен. Возвращает массив [рац. число, измененный многочлен]",
    "MUL_PP_P":"Умножение многочленов. На вход получает 2 многочленa. Возвращает новый многочлен. Не изменяет входные данные",
    "DER_P_P":"Производная полинома. На вход получает многочлен. Возвращает новый многочлен. Не изменяет входные данные",
    "DIV_PP_P":"Частное от деления многочлена на многочлен при делении с остатком. На вход два многочлена. Возвращает изменённый многочлен. Изменяет входные данные",
    "MOD_PP_P":"Остаток от деления многочлена на многочлен при делении с остатком. На вход два многочлена. Возвращает изменённый многочлен. Изменяет входные данные",
    "":"",
    "":"",
    "":"",
}

def help():
    for key in __content.keys():
        length = 15 - len(key)
        print(key + ":" + " " * length, __content[key])

def isExist(funcName):
    if funcName in __content.keys():
        print("Функция существует")
    else:
        print("Такой функции нет")

#Функция рассчитывает частное от деления целого на целое (делитель отличен от нуля)
#Результат записывается в num1

#Остаток от деления большего натурального числа на меньшее или равное
def MOD_NN_N(num1, num2):
    if COM_NN_D(num1, num2) == 2:
        times = 0
        while COM_NN_D(num1, num2) == 2:
            num2.addToTail(0)
            times += 1
        if COM_NN_D(num1, num2) == 1:
            num2.toTail()
            num2.remove()
            times -= 1

        for i in range(times):
            while COM_NN_D(num1, num2) == 2:
                SUB_NN_N(num1, num2)
            num2.toTail()
            num2.remove()

    highFlag = 1
    while highFlag == 1:
        lowFlag = 1
        num1.toTail()
        num2.toTail()

        if(COM_NN_D(num1, num2) != 1):
            num1.toTail()
            num2.toTail()

            while lowFlag == 1:
                result = num1.getN() - num2.getN()
                if result > 0:
                    num1.updateN(result)
                elif result == 0:
                    if(num1.isNextAvailable() == 0 and num1.isBeforeAvailable()):
                        num1.remove()
                        num1.zeroClear()
                    else:
                        num1.updateN(result)

                else:
                    borrRes = borrow(num1)
                    if borrRes == 10:
                        num1.updateN(result + 10)
                    else:
                        lowFlag = 0
                        highFlag = 0
                next1 = num1.next()
                next2 = num2.next()
                if next1 == 0 or next2 == 0:
                    lowFlag = 0
        else:
            if num1.getN() == 0 and num1.isNextAvailable() == 0:
                highFlag = 2
            else:
                highFlag = 0

    return num1

def MOD_NN_N_MOD(num1, num2):
    frequent = 0
    if COM_NN_D(num1, num2) == 2:
        times = 0
        while COM_NN_D(num1, num2) == 2:
            num2.addToTail(0)
            times += 1
        if COM_NN_D(num1, num2) == 1:
            num2.toTail()
            num2.remove()
            times -= 1

        for i in range(times):
            while COM_NN_D(num1, num2) == 2:
                SUB_NN_N(num1, num2)
                frequent += 10 ** (times - i)

            num2.toTail()
            num2.remove()
    highFlag = 1
    while highFlag == 1:
        lowFlag = 1
        num1.toTail()
        num2.toTail()

        if(COM_NN_D(num1, num2) != 1):
            num1.toTail()
            num2.toTail()
            frequent += 1
            while lowFlag == 1:
                result = num1.getN() - num2.getN()
                if result > 0:
                    num1.updateN(result)
                elif result == 0:
                    if(num1.isNextAvailable() == 0 and num1.isBeforeAvailable()):
                        num1.remove()
                        num1.zeroClear()
                    else:
                        num1.updateN(result)

                else:
                    borrRes = borrow(num1)
                    if borrRes == 10:
                        num1.updateN(result + 10)
                    else:
                        lowFlag = 0
                        highFlag = 0
                next1 = num1.next()
                next2 = num2.next()
                if next1 == 0 or next2 == 0:
                    lowFlag = 0
        else:
            if num1.getN() == 0 and num1.isNextAvailable() == 0:
                highFlag = 2
            else:
                highFlag = 0

    return frequent

#Частное от деления большего натурального числа на меньшее или равное натуральное с остатком
def DIV_NN_N(num1, num2):
    j = 0
    z = 0
    while num1.getN() == 0 and num2.getN() == 0: #Сокращение нулей
        num1.remove()
        num2.remove()
    if COM_NN_D(num1, num2) == 2:
        times = 0 #Счетчик кол-ва повторов цикла, в котором происходит вычитание num1-num2 и умножение num2 на 10
        while COM_NN_D(num1, num2) == 2:
            MUL_Nk_N(num2, 1)
            times += 1
        if COM_NN_D(num1, num2) == 1:
            num2.toTail()
            num2.remove()
            times -= 1
        j += 10 ** times
        for i in range(times):
            while COM_NN_D(num1, num2) == 2:
                SUB_NN_N(num1, num2)
                z += j
            num2.toTail()
            num2.remove()
            j = j // 10

    while COM_NN_D(num1, num2) == 2 or COM_NN_D(num1, num2) == 0:
        num1.toTail()
        num2.toTail()
        SUB_NN_N(num1, num2)
        z += 1
    return z #функцию возвращает частное от деления (i), num1 становится остатком от деления num1 на num2

#Умножение натурального числа на цифру
def MUL_ND_N(num, multiplier):

    if multiplier > 9 or multiplier < 0:
        res = -1
    else:
        num.toTail()
        over = (num.getN() * multiplier) // 10 #умножаем последнюю цифру числа на данный множитель и берём целое от деления на 10, запоминаем
        num.updateN((num.getN() * multiplier) % 10)  #обновляем последнюю цифру числа умножением последней цифры на множитель и взятием остатка по 10
        while num.isNextAvailable(): #пока в числе есть цифры
            num.next()
            rememb=num.getN()
            num.updateN(((rememb*multiplier)+over)%10)
            over = ((rememb * multiplier)+over)//10
        if over>0:  #если цифры закончились но в over что-то осталось, то создаём следующий разряд и добавляем значение over в него
            num.addToHead(over)
        res = num
    return res

#Она долговата, но я могу её понять..
#Умножение натуральных чисел.
def MUL_NN_N(n1, n2):
    n1.toTail()
    n2.toTail()
    power = 0  # переменная степени
    len = n2.length()  # длина 2 числа
    res = Number("0")  # переменная, в которую будем записывать результат
    for i in range(len):
        mult = n2.getN()   # берём очередную цифру числа, начиная с конца
        m = copy.deepcopy(n1)
        res = ADD_NN_N(res, MUL_Nk_N(MUL_ND_N(m, mult), power)) # основное действие:
        #умножаем второй(m = n2) множитель на очередную цифру числа и на 10 в степени i,
        #добавляем к тому, что уже есть в res
        power += 1  # увеличиваем степень
        n2.next()   # переходим к следующей циферке
    return res


# Вычисление первой цифры деления большего натурального на меньшее,
# домноженное на 10^k,где k - номер позиции этой цифры (номер считается с нуля)
def DIV_NN_Dk(nom1, nom2):
    nom1.toHead()
    nom2.toHead()

    if nom2.getN() == 0 or nom1.getN() == 0:
        return -1

    else:
        f = COM_NN_D(nom1, nom2)
        if f == 1:
            nom = nom1
            nom1 = nom2
            nom2 = nom
        elif f == 0:
            return Number('1')

        a = str(nom1.getN())
        q = Number(a)
        f = 1
        # получаем число, которое будем делить(принцип деление столбиком)
        while f == 1:
            f = COM_NN_D(q, nom2)
            if f == 1:
                f = nom1.before()
                if f == 1:
                    a = (nom1.getN())
                    q.addToTail(a)
        # Вычисление первой цифры деления
        i = 1
        f = 1
        while f == 1:
            q = SUB_NN_N(q, nom2)
            f = COM_NN_D(nom2, q)
            if f == 1 or f == 0:
                i += 1
        # получаем
        f = 1
        k = 0
        while f == 1:
            f = nom1.before()
            if f == 1:
                k += 1
        return MUL_Nk_N(Number(str(i)), k)


#N-13
#НОД натуральных чисел, на вход получает 2 числа, возвращает 1 число. Изменяет полученные данные
def GCF_NN_N(number1, number2):
    number1.toTail()
    number2.toTail()
    if number1.getSign() == 1 or number2.getSign() == 1:
        return -1
    else:
        while not NZER_N_B(number1) and not NZER_N_B(number2): #number1 != 0 and number2 != 0
            if COM_NN_D(number1, number2) == 2: #number1 > number2
                number1 = MOD_NN_N(number1, number2) #number1 % number2
            else:
                number2 = MOD_NN_N(number2, number1) #number2 % number1

        if NZER_N_B(number2):
            gcd = number1
        else:
            gcd = number2
        return gcd

#Натуральное в целое - пустышка для поздняка
def TRANS_N_Z(num):
    return num

#функция подсчета суммы двух целых чисел
def ADD_ZZ_Z(num1, num2):
    num1.toTail()
    num2.toTail()
    s1 = num1.getSign()
    s2 = num2.getSign()

    num1.updateSign(0)
    num2.updateSign(0)

    if s1 == 0 and s2 == 0: # + and +
        res = ADD_NN_N(num1, num2)
    elif s1 == 0 and s2 == 1: # + and -
        if COM_NN_D(num1, num2) == 1:
            res = SUB_NN_N(num2, num1)
            res.updateSign(1)
        else:
            res = SUB_NN_N(num1, num2)
    elif s1 == 1 and s2 == 0: # - and +
        if COM_NN_D(num1, num2) == 2:
            res = SUB_NN_N(num1, num2)
            res.updateSign(1)
        else:
            res = SUB_NN_N(num2, num1)
    else: # - and -
        res = ADD_NN_N(num1, num2)
        res.updateSign(1)

    return res

#нужны SUB_NN_N, COM_NN_D, ADD_NN_N

def SUB_ZZ_Z(n1, n2): #принимает на вход 2 числа, где первое - из чего вычитаем, второе - что вычитаем(!)
    n1.toTail()
    n2.toTail()
    sign1 = n1.getSign()  #получаем знаки чисел
    sign2 = n2.getSign()
    comp = COM_NN_D(n1, n2)   #и переменную сравнения
    len = n1.length()   #ну и длину

    if (comp == 0):     #если равны, просто превращаем 1 число в 0
        n1.updateN(0)
        n1.toHead()
        for i in range(len - 1):
            n1.remove()

    elif (sign1 != sign2):    #для чисел с разными знаками
        if (sign1 == 1):      #когда 1 число отрицательное складываем их модули и добавляем минус
            n1.updateSign(0)
            n1 = ADD_NN_N(n2, n1)
            n1.updateSign(1)
        else:                  #когда 1 число положительное просто складываем их модули
            n2.updateSign(0)
            n1 = ADD_NN_N(n2, n1)

    elif (sign1 == sign2 == 0):  #для положительных чисел
            if (comp == 2):      #если 1 число больше просто вычитаем
                n1 = SUB_NN_N(n1, n2)
            else:                #если 2 число больше вычитаем и добавляем минус
                n1 = SUB_NN_N(n2, n1)
                n1.updateSign(1)

    elif (sign1 == sign2 == 1): #для отрицательных чисел
        if (comp == 1):              #если 2 число больше вычитаем из модуля 1 модуль 2 (знак остаётся -)
            n1.updateSign(0)
            n2.updateSign(0)
            n1 = SUB_NN_N(n1, n2)
            n1.updateSign(1)
        else:
            n1.updateSign(0)
            n2.updateSign(0)
            n1 = SUB_NN_N(n2, n1)    #если 2 число меньше вычитаем из модуля 2 модуль 1 и меняем знак
    return n1      #возвращаем 1 число

# Умножение целых чисел
def MUL_ZZ_Z(num1, num2):

    a = POZ_Z_D(num1)  # проверяем знаки 1 и 2 чисел
    b = POZ_Z_D(num2)
    if a == 1:  # находим абсолютную величину для отрицательных
        num1 = ABS_Z_N(num1)
    if b == 1:
        num2 = ABS_Z_N(num2)
    if (a == 0) or (b == 0):
        res = Number("0")
    if (a == b) and (a != 0):
        res = MUL_NN_N(num1, num2)
    if (a != b) and ((a != 0) and (b != 0)): # минус у произведения только в случае, когда у множителей знаки различны
        res = MUL_NN_N(num1, num2)
        res.updateSign(1)

    return res


#не работает
#Функция рассчитывает частное от деления целого на целое (делитель отличен от нуля)
#Результат записывается в num1

def DIV_ZZ_Z(num1,num2):
    #Первое число - делимое
    #Второе число - делитель( не равен 0)
    s1 = num1.getSign()
    s2 = num2.getSign()
    if POZ_Z_D(num2) == 0:
        q = -1
    else:
        #если модуль делимого меньше делителя то целая часть автоматически 0 (тут сразу уитывается, если делимое 0)
        if COM_NN_D(ABS_Z_N(num1), ABS_Z_N(num2)) == 1:
            q = 0
        else:
            if s1 == 1:
                num1.updateSign(1)
            if s2 == 1:
                num2.updateSign(1)
            #если оба числа положительны или отрицательны
            if (POZ_Z_D(num1) == 2 and POZ_Z_D(num2) == 2) or (POZ_Z_D(num1) == 1 and POZ_Z_D(num2) == 1) :
                q = DIV_NN_N(ABS_Z_N(num1),ABS_Z_N(num2))
            #если числа разных знаков
            elif (POZ_Z_D(num1) == 1 and POZ_Z_D(num2) == 2) or (POZ_Z_D(num1) == 2 and POZ_Z_D(num2) == 1):
                q = DIV_NN_N(ABS_Z_N(num1), ABS_Z_N(num2))
                if num1.show("get") != 0:
                    q +=1
                q = q*-1
    num1 = Number(str(q))
    return num1


#Z-10
#Остаток от деления целого на целое (делитель отличен от нуля),
#на вход получает 2 числа, возвращает 1 число
def MOD_ZZ_Z(num1, num2):
    sign_num1 = POZ_Z_D(num1)
    sign_num2 = POZ_Z_D(num2)
    if sign_num2 == 0:  # деление на 0
        return -1
    else:
        if sign_num1 == 2 and sign_num2 == 2:  # для положительных
            rem = MOD_NN_N(num1, num2)
        elif sign_num1 == 1 and sign_num2 == 1:  # для отрицательных
            mod_num1 = ABS_Z_N(num1)  # |num1|
            mod_num2 = ABS_Z_N(num2)  # |num2|
            rem = MOD_NN_N(mod_num1, mod_num2)
        else:  # для отрицательного и положительного
            num1_copy = copy.deepcopy(num1)  # создание копий
            num2_copy = copy.deepcopy(num2)
            quot = DIV_ZZ_Z(num1_copy, num2_copy)  # num1 // num2
            num1_copy = copy.deepcopy(num1)  # создание копий
            num2_copy = copy.deepcopy(num2)
            prod = MUL_ZZ_Z(num2_copy, quot)  # num2 * quot
            rem = SUB_ZZ_Z(num1_copy, prod)  # num1 - prod
            rem = ABS_Z_N(rem)  # |rem|
        return rem

#N-14 НОК натуральных чисел
def LCM_NN_N(num1, num2):
    num1.toTail()
    num2.toTail()
    while not NZER_N_B(num1) and not NZER_N_B(num2):
        if COM_NN_D(num1, num2) > 0:  # num1 > num2  or num1 < num2
            res = DIV_ZZ_Z(MUL_NN_N(num1, num2), GCF_NN_N(num1, num2))  # НОК
        else:  # num1 = num2
            res = num1
        return res


def ADD_QQ_Q(drob_1, drob_2):
    __correctFraction(drob_1)
    __correctFraction(drob_2)
    drob1 = copy.deepcopy(drob_1)
    drob2 = copy.deepcopy(drob_2)
    znam1 = numCopy(drob1[1])  # копируем
    znam2 = numCopy(drob2[1])  # копируем
    nok = (LCM_NN_N(drob1[1], drob2[1]))
    nok1 = numCopy(nok)  # копируем знаменатель
    nok2 = numCopy(nok)  # копируем знаменатель

    a1 = Number(str(DIV_NN_N(nok1, znam1)))  # множитель1

    a2 = Number(str(DIV_NN_N(nok2, znam2)))  # множитель2

    numerator1 = MUL_ZZ_Z(a1, drob1[0])  # числитель1
    numerator2 = MUL_ZZ_Z(a2, drob2[0])  # числитель2

    numerator = ADD_ZZ_Z(numerator1, numerator2)  # числитель сложения
    drob = [numerator, nok]
    drob = RED_Q_Q(drob)
    return drob

def __correctFraction(frac):
    key1 = frac[0].saveCurPos()
    key2 = frac[1].saveCurPos()
    frac[0].toTail()
    frac[1].toTail()

    if type(frac[0]) != Number:
        raise Exception("Ошибка. Числитель не класса Number. Получен класс {}, Значение {}".format(type(frac[0]), frac[0]))
    if type(frac[1]) != Number:
        raise Exception("Ошибка. Знаменатель не класса Number. Получен класс {}, Значение {}".format(type(frac[1]), frac[1]))
    if frac[1].getN() == 0 and frac[1].isNextAvailable() == 0:
        raise Exception("Ошибка. Нулевой знаменатель")
    if frac[1].getSign() == 1:
        raise Exception("Ошибка. Отрицательный знаменатель")
    frac[0].recoverCurPos(key1)
    frac[1].recoverCurPos(key2)


#Является ли рациональное число целым
def INT_Q_B(fraction = []):   #Если целое, то 1, если рац, то 0
    __correctFraction(fraction)
    fraction[0] = numCopy(fraction[0])
    fraction[1] = numCopy(fraction[1])
    fraction[0].updateSign(0)
    fraction[1].updateSign(0)
    res = -1

    if fraction[0].getN() == 0:
        res = 1

    elif len(fraction) != 0:
        response = MOD_NN_N(fraction[0], fraction[1])

        res = 0
        if NZER_N_B(response) == 1:
            res = 1

    return res


    #print(INT_Q_B([num1, num2]) == (num1.show("get_abs")) % num2.show("get_abs"))

#Сокращение дроби
def RED_Q_Q(fract):
    __correctFraction(fract)
    sign_denum = POZ_Z_D(fract[1])
    if len(fract) != 0 and sign_denum == 2:  # пустой массив и не натуральный знаменатель
        # модуль числителя
        if POZ_Z_D(fract[0]) == 1:  # fract[0] < 0?
            mod_num = ABS_Z_N(copy.deepcopy(fract[0]))
        else:
            mod_num = copy.deepcopy(fract[0])
        gcd = GCF_NN_N(mod_num, copy.deepcopy(fract[1]))  # НОД(|числитель|, знаменатель)
        if type(gcd) != int:
            num = DIV_ZZ_Z(copy.deepcopy(fract[0]), copy.deepcopy(gcd))  # числитель // НОД
            denum = DIV_ZZ_Z(copy.deepcopy(fract[1]), gcd)  # знаменатель // НОД
            return [num, denum]
        else:
            return -1

    else:
        return -1




#Преобразование дробного в целое
def TRANS_Q_Z(fraction = []):
    Num2 = Number("1")
    if COM_NN_D(fraction[1], Num2) == 0:
        return fraction[0]
    else:
        return -1


#Вычитание дробей
def SUB_QQ_Q(f1, f2):
    __correctFraction(f1)
    __correctFraction(f2)
    fun1 = [numCopy(f1[0]), numCopy(f1[1])]
    fun2 = [numCopy(f2[0]), numCopy(f2[1])]
    fun1[0].toTail()
    fun1[1].toTail()
    fun2[0].toTail()
    fun2[1].toTail()
    k1 = numCopy(fun1[1])  # делаем копию потому что f1[1] изменится после функции =(
    k2 = numCopy(fun2[1])  # делаем копию потому что f2[1] изменится после функции =(
    a = LCM_NN_N(fun1[1], fun2[1])  # общий знаменатель
    a1 = numCopy(a)  # делаем копию потому что а потеряется =(
    a2 = numCopy(a)  # делаем копию чтобы не потерять знаменатель
    b1 = Number(str(DIV_NN_N(a, k1)))
    b2 = Number(str(DIV_NN_N(a1, k2)))
    fun1[0] = MUL_ZZ_Z(fun1[0], b1)
    fun2[0] = MUL_ZZ_Z(fun2[0], b2)
    fun1[0] = SUB_ZZ_Z(fun1[0], fun2[0])
    fun1[1] = a2
    fun1 = RED_Q_Q(fun1)
    return fun1

#функция для умножения дробей
def MUL_QQ_Q(fr1, fr2): #функция для умножения дробей
    __correctFraction(fr1)
    __correctFraction(fr2)
    f1 = copy.deepcopy(fr1)
    f2 = copy.deepcopy(fr2)
    f1[0].toTail()
    f1[1].toTail()
    f2[0].toTail()
    f2[1].toTail()
    f1[0] = MUL_ZZ_Z(f1[0], f2[0])  # перемножаем числители
    f1[1] = MUL_ZZ_Z(f1[1], f2[1])  # и знаменатели
    f1 = RED_Q_Q(f1)
    return f1



#Деление дробей
#если передать в функцию в качестве делимого 0, то вернёт 0
def DIV_QQ_Q(drob1,drob2):
    __correctFraction(drob1)
    __correctFraction(drob2)
    f1 = copy.deepcopy(drob1)
    f2 = copy.deepcopy(drob2)
    if f1[1].getSign() == 1:
        f1[1].updateSign(0)
        if f1[0].getSign() == 1:
            f1[0].updateSign(0)
        else:
            f1[0].updateSign(1)
    if f2[0].getSign() == 1:
        f2[0].updateSign(0)
        if f2[1].getSign() == 1:
            f2[1].updateSign(0)
        else:
            f2[1].updateSign(1)
    f = [0, 0]
    f1[0].toHead()
    f2[0].toHead()
    if f2[0].getN==0:
        return -1
    if f1[0].getN==0:
        return Number("0")
    f[0]=f2[1]
    f[1]=f2[0]
    rez_drob=[MUL_ZZ_Z(f1[0],f[0]),MUL_ZZ_Z(f1[1],f[1])]
    rez_drob = RED_Q_Q(rez_drob)
    return rez_drob



#функция сложения полиномов, тесты были проведены
def ADD_PP_P(pol1, pol2):
    pol1.toHead()
    pol2.toHead()
    if pol1.getDeg() >= pol2.getDeg():  #создаём копии полиномов (первым выбираем с наибольшей степенью)
        p1 = copy.deepcopy(pol1)
        p2 = copy.deepcopy(pol2)
    else:
        p1 = copy.deepcopy(pol2)
        p2 = copy.deepcopy(pol1)
    p1.toTail()
    p2.toTail()
    len = p2.length()
    for i in range(len):
        deg2 = p2.getDeg()
        a = p1.getN()
        b = p2.getN()
        if a[1] != 0 or b[1] != 0:  # проверка на нули в знаменателях
            p1.insert([b, deg2])
            p2.next()
            p1.next()
        else:
            return -1
    return p1




#Вычитание многочленов
def SUB_PP_P(pol1, pol2):
    pol1.toHead()
    pol2.toHead()
    if pol1.getDeg() >= pol2.getDeg():  #создаём копии полиномов (первым выбираем с наибольшей степенью)
        p1 = copy.deepcopy(pol1)
        p2 = copy.deepcopy(pol2)
    else:
        p1 = copy.deepcopy(pol2)
        p2 = copy.deepcopy(pol1)
    p1.toTail()
    p2.toTail()
    len = p2.length()   #находим длину 2 многочлена
    for i in range(len):    #меняем все его знаки
        if p2.getSign() == 1:
            p2.updateSign(0)
        else:
            p2.updateSign(1)
        p2.next()
    res = ADD_PP_P(p1, p2)    #используем сложение
    return res


# Умножение многочлена на рациональное число
def MUL_PQ_P(pol, r):
    pol1=copy.deepcopy(pol)
    pol1.toHead()
    while pol1.isBeforeAvailable():  #пока есть следующий элемент в полиноме, то идем по нему
        x = pol1.getN() #коэфф элемента полинома
        deg =pol1.getDeg() #степень элемента полинома
        pol1.updateN([MUL_QQ_Q(x, r), deg]) #обновляем наш полином; умножаем изначальный коэфф на заднный
        pol1.before()

    x = pol1.getN()       #последний элемент полинома
    deg = pol1.getDeg()
    pol1.updateN([MUL_QQ_Q(x, r), deg]) #обновляем соответственно последний элемент многочлена
    return pol1

#Умножение многочлена на x^k
def MUL_Pxk_P(pol, xk):
    pol1=copy.deepcopy(pol)  #создаем копию полинома чтобы начальный не трогать
    pol1.toHead()  #идём в башку
    while pol1.isBeforeAvailable():  #пока есть след элемент то идём по полиному
        a=pol1.getN()
        b=pol1.getDeg()
        pol1.updateN([ [ a[0], a[1] ], b+xk])
        pol1.before()
    a = pol1.getN()       #когда следующего элемента не будет то мы остановимся на последнем
    b = pol1.getDeg()     #и этот последний тоже нужно изменить
    pol1.updateN([[a[0], a[1]], b + xk]) #что мы собственно и делаем
    return pol1  #возвращаем новый полином, а старый - нетронутый

# Старший коэффициент многочлена
def LED_P_Q(pol):
    pol.toHead()
    return pol.getN()

#Cтепень многочлена
def DEG_P_N(pol):
    if not pol.toHead(): #если смогли попасть в голову
        deg = Number(str(pol.getDeg()))  #deg - степень, делаем ее объектом класса Number
        return deg
    else:
        return -1

# Вынесение из многочлена НОК знаменателей коэффициентов и НОД числителей
# принимает многочлен, возвращает массив [рац. число, измененный многочлен]
def FAC_P_Q(pol):
    pol.toHead()
    frac = pol.getN()
    gcd = ABS_Z_N(copy.deepcopy(frac[0]))  # НОД
    lcm = ABS_Z_N(copy.deepcopy(frac[1]))  # НОК
    # Поиск НОД и НОК
    for i in range(pol.length()):
        pol.before()
        frac = pol.getN()
        gcd = GCF_NN_N(ABS_Z_N(copy.deepcopy(frac[0])), copy.deepcopy(gcd))  # НОД(числитель, НОД)
        lcm = LCM_NN_N(ABS_Z_N(copy.deepcopy(frac[1])), copy.deepcopy(lcm)) # НОК(знаменатель, НОК)
    # Вынесение НОД/НОК
    for i in range(pol.length()):
        frac = pol.getN()
        frac[0] = DIV_ZZ_Z(copy.deepcopy(frac[0]), copy.deepcopy(gcd))  # числитель // НОД
        mult = DIV_ZZ_Z(copy.deepcopy(lcm), copy.deepcopy(frac[1]))  # НОК // знаменатель
        frac[0] = MUL_ZZ_Z(copy.deepcopy(frac[0]), copy.deepcopy(mult))  # числитель * mult
        frac[1] = Number("1")  # знаменатель = 1
        pol.next()
    return [[gcd, lcm], pol]

# Умножение многочленов
def MUL_PP_P(pol1, pol2):
    pol1.toHead()
    pol2.toHead()
    if pol1.getDeg() >= pol2.getDeg():  # копии многочленов, p1 - больший по степени
        p1 = copy.deepcopy(pol1)
        p2 = copy.deepcopy(pol2)
    else:
        p1 = copy.deepcopy(pol2) #p1 длиннее
        p2 = copy.deepcopy(pol1)
    p1.toHead()
    p2.toHead()
    res = Polynomial([([Number("0"), Number("1")], 0)])
    while p1.isBeforeAvailable():
        mas=p1.getN()
        deg=p1.getDeg()
        ressum=copy.deepcopy(p2)
        ressum.toHead()
        res2 = Polynomial([([Number("0"), Number("1")], 0)])
        while ressum.isBeforeAvailable():
            mas2 = ressum.getN()
            res2.insert([[MUL_ZZ_Z(mas[0],mas2[0]),MUL_ZZ_Z(mas[1],mas2[1])], ressum.getDeg()+deg])
            ressum.before()
        mas2 = ressum.getN()
        res2.insert([[MUL_ZZ_Z(mas[0], mas2[0]), MUL_ZZ_Z(mas[1], mas2[1])], ressum.getDeg() + deg])
        res2.toHead()
        while res2.isBeforeAvailable():
            res.insert([ res2.getN(), res2.getDeg()])
            res2.before()
        res.insert([res2.getN(), res2.getDeg()])
        p1.before()
    mas = p1.getN()
    deg = p1.getDeg()
    ressum = copy.deepcopy(p2)
    ressum.toHead()
    res2 = Polynomial([([Number("0"), Number("1")], 0)])
    while ressum.isBeforeAvailable():
        mas2 = ressum.getN()
        res2.insert([[MUL_ZZ_Z(mas[0], mas2[0]), MUL_ZZ_Z(mas[1], mas2[1])], ressum.getDeg() + deg])
        ressum.before()
    mas2 = ressum.getN()
    res2.insert([[MUL_ZZ_Z(mas[0], mas2[0]), MUL_ZZ_Z(mas[1], mas2[1])], ressum.getDeg() + deg])
    res2.toHead()
    while res2.isBeforeAvailable():
        res.insert([res2.getN(), res2.getDeg()])
        res2.before()
    res.insert([res2.getN(), res2.getDeg()])
    res.toHead()
    res.zeroClear()
    return res



#функция производной полинома
#на вход полином, на выход полином
def DER_P_P(pol):
    flag = 0
    p = copy.deepcopy(pol)
    if p.getN()[1] != 0:   #проверка на нули знаменателя
        p.toHead()   #идём к большей степени
        while p.isBeforeAvailable():
            flag = 1
            deg = p.getDeg()      #степень текущего
            z = Number(str(deg))  #переменная степени
            p.updateN([MUL_QQ_Q(p.getN(), [z, Number("1")]), deg - 1])  #умножаем числитель на степеь, из степени вычитаем 1
            p.before()      #переходим к следующему
        deg_e = p.getDeg()
        if deg_e == 0 and flag == 1:    #удаляем свободный член, если в полиноме больше одного элемента
            p.remove()
        elif deg_e == 0 and flag == 0:    #выводим 0, если в полиноме только свободный член
            return Polynomial([[[Number("0"), Number("1")], 0]])
        elif deg_e != 0:    #иначе берём производную у последнего элемента
            deg = p.getDeg()  # степень текущего
            z = Number(str(deg))  # переменная степени
            p.updateN([MUL_QQ_Q(p.getN(), [z, Number("1")]), deg - 1])  # умножаем числитель на степень, из степени вычитаем 1
    else:
        return -1
    return p




#Частное от деления многочлена на многочлен при делении с остатком
def DIV_PP_P(pol1, pol2):
    i = 0
    pol1.toHead()
    pol2.toHead()
    check = 0
    w = Number("0")
    if COM_NN_D(DEG_P_N(pol1), DEG_P_N(pol2)) == 2 or COM_NN_D(DEG_P_N(pol1), DEG_P_N(pol2)) == 0:
        while (COM_NN_D(DEG_P_N(pol1), DEG_P_N(pol2)) == 2 or COM_NN_D(DEG_P_N(pol1), DEG_P_N(pol2)) == 0) and check == 0:
            k = SUB_NN_N(DEG_P_N(pol1), DEG_P_N(pol2))
            if ((i == 0) or (COM_NN_D(k, w) != 0)):
                w = copy.deepcopy(k)
                z = DIV_QQ_Q(pol1.getN(), pol2.getN())
                if (COM_NN_D(z[1], Number("0")) == 1):
                    z[0].updateSign(1)
                    z[1].updateSign(0)
                j = k.show("get")
                pol1 = SUB_PP_P(pol1, MUL_Pxk_P(MUL_PQ_P(pol2, z), j))
                pol1.zeroClear()
                if i == 0:
                    pol3 = Polynomial([[z, j]])
                else:
                    pol3.addToTail([z, j])
                i += 1
            else:
                check = 1
        return pol3
    else:
        return Polynomial([[Number("0"), Number("1")], 0])

#Остаток от деления многочлена на многочлен при делении с остатком
def MOD_PP_P(pol1, pol2):
    i = 0
    pol1.toHead()
    pol2.toHead()
    check = 0
    w = Number("0")
    if COM_NN_D(DEG_P_N(pol1), DEG_P_N(pol2)) == 2 or COM_NN_D(DEG_P_N(pol1), DEG_P_N(pol2)) == 0:
        while (COM_NN_D(DEG_P_N(pol1), DEG_P_N(pol2)) == 2 or COM_NN_D(DEG_P_N(pol1),
                                                                       DEG_P_N(pol2)) == 0) and check == 0:
            k = SUB_NN_N(DEG_P_N(pol1), DEG_P_N(pol2))
            if ((i == 0) or (COM_NN_D(k, w) != 0)):
                w = copy.deepcopy(k)
                z = DIV_QQ_Q(pol1.getN(), pol2.getN())
                if (COM_NN_D(z[1], Number("0")) == 1):
                    z[0].updateSign(1)
                    z[1].updateSign(0)
                j = k.show("get")
                pol1 = SUB_PP_P(pol1, MUL_Pxk_P(MUL_PQ_P(pol2, z), j))
                pol1.zeroClear()
                i += 1
            else:
                check = 1
        return pol1
    else:
        return pol1


def foo(pol):  # выдаёт еденицу значит полином не нулевоц
    f = 0
    pol.toHead()
    a = pol.getN()
    if NZER_N_B(a[0]) != 1:
        f = 1
    while (pol.next()):
        a = pol.getN()
        if NZER_N_B(a[0]) != 1:
            f = 1
    pol.toHead()
    return f


def GCF_PP_P(pol1, pol2):
    p1_cop = numCopy(pol1)  # копия первого полинома
    p2_cop = numCopy(pol2)  # копия второго полинома
    # если оба делятся на второй полином без остатка
    r1 = MOD_PP_P(pol1, pol2)
    print("остаток 1")
    r1.show()
    if foo(r1) == 0:
        return p2_cop

    p1_cop = numCopy(r1)  # копируем остаток r1
    # проверяем второй полином на остаток r1
    r2 = MOD_PP_P(p2_cop, r1)
    print("остаток 2")
    r2.show()
    if foo(r2) == 0:
        return p1_cop
    # p1_cop копируем остаток r1
    # r2
    while True:
        p2_cop = copy.deepcopy(r2)
        r1 = MOD_PP_P(copy.deepcopy(p1_cop), r2)
        print("остаток 3")
        r1.show()
        if foo(r1) == 0:
            return p2_cop
        p1_cop = p2_cop
        r2 = copy.deepcopy(r1)


def NMR_P_P(pol):
    if pol.length() != 0:
        der = DER_P_P(copy.deepcopy(pol))
        gcf = GCF_PP_P(copy.deepcopy(pol), copy.deepcopy(der))
        res = DIV_PP_P(copy.deepcopy(pol), copy.deepcopy(gcf))
        return res
    else:
        return -1

__desc = [
    [COM_NN_D, 2, -1, -1],
    [NZER_N_B, 1, -1, -1],
    [ADD_1N_N, 1, -1, -1],
    [ADD_NN_N, 2, -1, -1],
    [SUB_NN_N, 2, -1, -1],
    [MUL_ND_N, 2, ["N", "i+"], ["Число", "Цифра"]],
    [MUL_Nk_N, 2, ["N", "i+"], ["Число", "Степень"]],
    [MUL_NN_N, 2, -1, -1],
    [SUB_NDN_N, 3, ["N", "N", "i+"], ["Число", "Число", "Цифра"]],
    [DIV_NN_Dk, 2, -1, -1],
    [DIV_NN_N, 2, -1, -1],
    [MOD_NN_N, 2, -1, -1],
    [GCF_NN_N, 2, -1, -1],
    [LCM_NN_N, 2, -1, -1],

    [ABS_Z_N, 1, -1, -1],
    [POZ_Z_D, 1, -1, -1],
    [MUL_ZM_Z, 1, -1, -1],
    [TRANS_N_Z, 1, -1, -1],
    ["FakeIt", 1, -1, -1],
    [ADD_ZZ_Z, 2, -1, -1],
    [SUB_ZZ_Z, 2, -1, -1],
    [MUL_ZZ_Z, 2, -1, -1],
    [DIV_ZZ_Z, 2, -1, -1],
    [MOD_ZZ_Z, 2, -1, -1],

    [RED_Q_Q, 2, -1, -1],
    [INT_Q_B, 2, -1, -1],
    ["FakeIt", 2, -1, -1],
    [TRANS_Q_Z, 2, -1, -1],
    [ADD_QQ_Q, 4, -1, -1],
    [SUB_QQ_Q, 4, -1, -1],
    [MUL_QQ_Q, 4, -1, -1],
    [DIV_QQ_Q, 4, -1, -1],

    [ADD_PP_P, 2, -1, -1],
    [SUB_PP_P, 2, -1, -1],
    [MUL_PQ_P, 3, ["P", "Q", "Q"], ["Многочлен", "Числитель", "Знаменатель"]],
    [MUL_Pxk_P, 2, ["P", "i+"], ["Многочлен", "Степень x"]],
    [LED_P_Q, 1, -1, -1],
    [DEG_P_N, 1, -1, -1],
    [FAC_P_Q, 1, -1, -1],
    [MUL_PP_P, 2, -1, -1],
    [DIV_PP_P, 2, -1, -1],
    [MOD_PP_P, 2, -1, -1],
    [GCF_PP_P, 2, -1, -1],
    [DER_P_P,1, -1, -1],
    [NMR_P_P,1, -1, -1],
]




def createContent(data):
    content = {}
    for i in range(len(data)):
        if i < 14:
            current = content["N-{}".format(i + 1)] = {}
            current["link"] = data[i][0]
            current["info"] = {}
            current = current["info"]

            current["args"] = data[i][1]
            if data[i][2] == -1:
                arr = []
                for j in range(current["args"]):
                    arr.append("N")
                current["argsTypes"] = arr
            else:
                current["argsTypes"] = data[i][2]
            if data[i][3] == -1:
                arr = []
                for j in range(current["args"]):
                    arr.append("Число {}".format(j + 1))
                current["argsDesc"] = arr
            else:
                current["argsDesc"] = data[i][3]

        elif i < 24:
            current = content["Z-{}".format(i - 14 + 1)] = {}
            current["link"] = data[i][0]
            current["info"] = {}
            current = current["info"]

            current["args"] = data[i][1]

            if data[i][2] == -1:
                arr = []
                for j in range(current["args"]):
                    arr.append("Z")
                current["argsTypes"] = arr
            else:
                current["argsTypes"] = data[i][2]

            if data[i][3] == -1:
                arr = []
                for j in range(current["args"]):
                    arr.append("Число {}".format(j + 1))
                current["argsDesc"] = arr
            else:
                current["argsDesc"] = data[i][3]
        elif i < 32:
            current = content["Q-{}".format(i - 24 + 1)] = {}
            current["link"] = data[i][0]
            current["info"] = {}
            current = current["info"]
            current["args"] = data[i][1]

            if data[i][2] == -1:
                arr = []
                for j in range(current["args"]):
                    arr.append("Q")
                current["argsTypes"] = arr
            else:
                current["argsTypes"] = data[i][2]

            if data[i][3] == -1:
                arr = []
                for i in range(current["args"]):
                    if i % 2 == 0:
                        arr.append("Числитель")
                    else:
                        arr.append("Знаменатель")
                current["argsDesc"] = arr
            else:
                current["argsDesc"] = data[i][3]
        elif i < 45:
            current = content["P-{}".format(i - 32 + 1)] = {}
            current["link"] = data[i][0]
            current["info"] = {}
            current = current["info"]
            current["args"] = data[i][1]

            if data[i][2] == -1:
                arr = []
                for j in range(current["args"]):
                    arr.append("P")
                current["argsTypes"] = arr
            else:
                current["argsTypes"] = data[i][2]

            if data[i][3] == -1:
                arr = []
                for j in range(current["args"]):
                    arr.append("Многочлен {}".format(j + 1))
                current["argsDesc"] = arr
            else:
                current["argsDesc"] = data[i][3]
    return content

content = createContent(__desc)
