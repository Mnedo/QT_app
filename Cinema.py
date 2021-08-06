import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton
from PyQt5.QtWidgets import QMainWindow, QLabel
from PyQt5 import uic
from PyQt5 import QtGui
from PyQt5.QtWidgets import QGridLayout, QMessageBox
from PyQt5.QtCore import Qt
import sqlite3
from PyQt5.QtGui import QPixmap, QPainter, QColor
from random import randint


class FirstForm(QMainWindow):
    """
    Открытие главного окна приложения
    Включает себя функционал кнопок с последующем открытий других форм
    """

    def __init__(self):
        """
        Инициализация главного окна приложения
        """
        super().__init__()
        uic.loadUi('main.ui', self)
        self.setGeometry(50, 50, 1600, 800)
        self.setFixedSize(1600, 850)
        self.setWindowTitle('Кинотеатр Премьер')
        self.buttonGroup.buttonClicked.connect(self.open_hall_form)
        self.hallname = 0
        self.pixmap = QPixmap('icon.jpg')
        self.image = QLabel(self)
        self.image.move(75, 0)
        self.image.resize(500, 250)
        self.image.setPixmap(self.pixmap)
        self.pixmap1 = QPixmap('icon_of_sites.jpg')
        self.image1 = QLabel(self)
        self.image1.move(1000, 0)
        self.image1.resize(500, 250)
        self.setContentsMargins(45, 100, 50, 0)
        self.image1.setPixmap(self.pixmap1)
        self.setStyleSheet("""QMainWindow { background-color: rgb(22, 41, 66);} """)
        self.set_info()
        self.do_paint = False
        self.paint()

    def set_info(self):
        """
        Заполнение формы информацией из базы данных и отрисовка названия дней недели
        Используется база данных list_of_films.sqlite, в которой систематизированы данные о
        Названии фильма, зале, в котором будет проходить фильм, времени начала фильм
        """
        plabek = QLabel(self)
        plabek.setText('Понедельник')
        plabek.setStyleSheet("color: rgb(240, 41, 194);")
        plabek.move(65, 215)
        vlabel = QLabel(self)
        vlabel.setText('Вторник')
        vlabel.setStyleSheet("color: rgb(240, 41, 194);")
        vlabel.move(365, 215)
        slabel = QLabel(self)
        slabel.setText('Среда')
        slabel.setStyleSheet("color: rgb(240, 41, 194);")
        slabel.move(640, 215)
        chlabel = QLabel(self)
        chlabel.setText('Четверг')
        chlabel.setStyleSheet("color: rgb(240, 41, 194);")
        chlabel.move(930, 215)
        ptlabel = QLabel(self)
        ptlabel.setText('Пятница')
        ptlabel.setStyleSheet("color: rgb(240, 41, 194);")
        ptlabel.move(1215, 215)
        company_label = QLabel(self)
        company_label.resize(200, 25)
        company_label.move(1350, 850)
        company_label.setText('ООО "Премьер"   г. Москва')
        company_label.setStyleSheet("color: rgb(240, 41, 194);")
        con = sqlite3.connect("list_of_films.sqlite")
        cur = con.cursor()
        result = cur.execute("""SELECT * FROM main""").fetchall()
        i = -1
        li = -1
        k = -1
        list_labels = [self.lb1_d1, self.lb2_d1, self.lb3_d1, self.lb4_d1,
                       self.lb1_d2, self.lb2_d2, self.lb3_d2, self.lb4_d2,
                       self.lb1_d3, self.lb2_d3, self.lb3_d3, self.lb4_d3,
                       self.lb1_d4, self.lb2_d4, self.lb3_d4, self.lb4_d4,
                       self.lb1_d5, self.lb2_d5, self.lb3_d5, self.lb4_d5]
        list_film = list(result)
        for el in self.buttonGroup.buttons():
            el.setCheckable(True)
            el.setStyleSheet("color: rgb(132, 199, 249);")
            i += 1
            if i - li == 5:
                k += 1
                list_labels[k].setText(list_film[i][1].lstrip('\n'))
                list_labels[k].setStyleSheet("color: rgb(132, 199, 249);")
                li = i
            el.setText(str(list_film[i][2]))
            el.setObjectName(str(list_film[i]))

    def paint(self):
        """
            Функция начинает отрисовку дизайна
        """
        self.do_paint = True
        self.repaint()

    def paintEvent(self, event):
        """
             Инициализация отрисовщика QPainter
         """
        qp = QPainter()
        qp.begin(self)
        self.draw_design(qp)
        qp.end()

    def draw_design(self, qp):
        """
        Отрисовка линей основного дизайна
        """
        qp.setBrush(QColor(240, 41, 194))
        qp.drawRect(50, 215, 2, 495)
        qp.drawRect(350, 215, 2, 495)
        qp.drawRect(625, 215, 2, 495)
        qp.drawRect(915, 215, 2, 495)
        qp.drawRect(1200, 215, 2, 495)
        qp.drawRect(1475, 215, 2, 495)
        qp.drawRect(50, 245, 1427, 2)
        qp.drawRect(50, 215, 1427, 2)
        qp.drawRect(50, 710, 1427, 2)

    def open_hall_form(self):
        """
        Функция начинает открытие новой формы
        Открывается окно с залом и местами, относящиеся к выбранному фильму
        В переменной inf передается вся информация о фильме, self.hallname содержит информацию о том,
        где будет проходить сеанс
        """

        inf = self.buttonGroup.checkedButton().objectName()
        self.hallname = inf[-2]
        self.hall = SecondForm(inf, self.hallname)
        self.hall.show()

    def keyPressEvent(self, event):
        """
            Закрытие окна по кнопке Esc, открывается окно с предупреждением
        """
        if event.key() == Qt.Key_Escape:
            if 16384 == int(QMessageBox.question(self, 'Предупреждение', "Вы точно хотите закрыть сайт?",
                                                 QMessageBox.Yes | QMessageBox.No)):
                self.close()


class SecondForm(QWidget):
    """
    Открытие окна, отображающее зал
    Свободные и занятые места, выбор мест для бронирования
    """

    def __init__(self, inf, name):
        """
        Инициализация главного окна с передачей информации о зале
        """
        super().__init__()
        self.hallname = name
        self.seats = []
        self.info = inf
        self.ordto = [inf, name]
        self.kino = {}
        self.setGeometry(300, 75, 1200, 900)
        self.setFixedSize(1200, 900)
        if self.hallname == '1':
            self.hallname = 'Синий'
        elif self.hallname == '2':
            self.hallname = 'Оранжевый'
        elif self.hallname == '3':
            self.hallname = 'Желтый'
        elif self.hallname == '4':
            self.hallname = 'Красный'
        elif self.hallname == '5':
            self.hallname = 'Белый'
        self.setWindowTitle(str(self.hallname) + ' зал')
        self.grid = QGridLayout(self)
        for i in range(7):
            for j in range(14):
                button = QPushButton(self)
                con = sqlite3.connect("booked_place.sqlite")
                cur = con.cursor()
                result = cur.execute("""SELECT * FROM main""").fetchall()
                for seat in result:
                    if seat[0] == i and seat[1] == j:
                        if seat[-1] == 0:
                            button.setStyleSheet("""QPushButton { background-color: rgb(128, 128, 128);
                                        } """)
                        elif seat[-1] == 1:
                            button.setStyleSheet("""QPushButton { background-color: rgb(15, 15, 128);
                                        } """)
                            button.setEnabled(False)
                button.resize(1000, 1)
                button.setObjectName(str(i) + ' ' + str(j) + ' 0')
                button.clicked.connect(self.book)
                self.grid.addWidget(button, i, j)
        self.grid.rowStretch(3)
        self.setLayout(self.grid)
        self.setContentsMargins(100, 100, 100, 250)
        self.InfoLabel = QLabel(self)
        self.InfoLabel.setText('Выбраны места:' + '\n' + 'Итоговая стоимость:')
        self.InfoLabel.move(100, 700)
        self.InfoLabel.resize(800, 250)
        self.InfoLabel.setFont(QtGui.QFont('SansSerif', 15))
        self.order = QPushButton(self)
        self.order.setText('Заказать')
        self.order.resize(175, 50)
        self.order.move(100, 700)
        self.order.clicked.connect(self.bill)
        self.order.setFont(QtGui.QFont('SansSerif', 15))
        label_laptop = QLabel(self)
        label_laptop.setText('Экран')
        label_laptop.move(565, 33)
        label_laptop.resize(200, 50)
        label_laptop.setFont(QtGui.QFont('Calibri', 18))
        label_laptop.setStyleSheet("""
            font: bold;
        """)
        label_laptop.setStyleSheet("color: rgb(255, 255, 255);")
        self.do_paint = False
        slabel = QLabel(self)
        slabel.setText('- Cвободные места')
        slabel.resize(150, 25)
        slabel.move(935, 725)
        zlabel = QLabel(self)
        zlabel.setText('- Занятые места')
        zlabel.resize(150, 25)
        zlabel.move(935, 775)
        vlabel = QLabel(self)
        vlabel.setText('- Выбранные вами места')
        vlabel.resize(150, 25)
        vlabel.move(935, 825)

    def paint(self):
        """
        Функция начинает отрисовку дизайна
        """
        self.do_paint = True
        self.repaint()

    def paintEvent(self, event):
        """
            Инициализация отрисовщика QPainter
        """
        qp = QPainter()
        qp.begin(self)
        self.draw_design(qp)
        qp.end()

    def draw_design(self, qp):
        """
        Отрисовка дизайна
        """
        qp.setBrush(QColor(56, 56, 56))
        qp.drawRect(150, 25, 900, 65)
        qp.setBrush(QColor(128, 128, 128))
        qp.drawRect(850, 725, 75, 25)
        qp.setBrush(QColor(15, 15, 128))
        qp.drawRect(850, 775, 75, 25)
        qp.setBrush(QColor(255, 0, 0))
        qp.drawRect(850, 825, 75, 25)

    def book(self):
        """
            Выбор мест для бронирования, высчитывание стоимости и передача информации о свободных местах
            Информация о месте, выбранном пользователем содержится в self.seats
        """
        st = 'Выбраны места: '
        allcost = 0
        name = self.sender()
        text = name.objectName()
        if text in self.seats:
            del self.seats[self.seats.index(text)]
            name.setStyleSheet("""QPushButton { background-color: rgb(128, 128, 128);
            } """)
        else:
            self.seats.append(text)
            name.setStyleSheet("""QPushButton { background-color: rgb(255, 0, 0);
            } """)
        i = 0
        for elements in self.seats:
            i += 1
            k = 0
            for letters in elements.split()[:-1]:
                if k == 0:
                    allcost += 280
                st += str(int(letters) + 1)
                k += 1
                if k == 1:
                    st += ' ряд '
                else:
                    st += ' место'
            if len(self.seats) != i:
                st += '; '
            if i == 4:
                st += '\n'
                i = 0
        st += '\n'
        st += 'Стоимость: ' + str(allcost) + ' руб.'
        self.InfoLabel.setText(st)

    def bill(self):
        """
            Открытие новой формы для оплаты выбранных мест
            Передается информация о выбранных местах и об окне, которое инициализирует новое окно
        """

        self.wndord = OrderForm(self.info, self.seats, self, self.ordto)
        self.wndord.show()

    def keyPressEvent(self, event):
        """
            Закрытие окна по кнопке Esc
            Предупреждение отсутствует
        """
        if event.key() == Qt.Key_Escape:
            self.close()


class CardError(Exception):
    """
    Описывает класс ошибки инициализации карты
    """
    pass


class CardFormatError(CardError):
    """
    Описывает класс ошибки инициализации карты
    """

    pass


class CardLuhnError(CardError):
    """
    Описывает класс ошибки инициализации карты
    """

    pass


class OrderForm(QWidget):
    """
        Инициализация окна с оплатой
        Принимается информация о выбранных местах и об окне, которое инициализирует новое окно
    """

    def __init__(self, inf, seat, wnd, towind):
        """
        Инициализация окна с оплата, передается информация о местах
        """
        super(OrderForm, self).__init__()
        uic.loadUi('pay.ui', self)
        self.wnd = wnd
        self.openinfo = towind
        self.setGeometry(1600, 500, 750, 100)
        self.setFixedSize(750, 100)
        self.info = inf[1:-1].split(', ')
        self.seats = seat
        self.setWindowTitle('Оплата билетов')
        self.hintLabel.setText(
            'Введите номер карты (16 цифр без пробелов):')
        self.payButton.clicked.connect(self.process_data)
        self.uniccode = []

    def finally_book(self, seats):
        """
            Функция, которая вызывается после финального подтверждения оплаты
            Обновление базы данных происходит на основе выбранных билетов
            База данных содержит информацию о ряде, месте, наличии брони
        """
        for el in seats:
            i, j = el.split()[:-1]
            i = int(i)
            j = int(j)
            con = sqlite3.connect("booked_place.sqlite")
            cur = con.cursor()
            req = ''
            params = (1, i, j)
            req = '''UPDATE main SET place = ?  WHERE (xcord = ?) AND (ycord = ?)'''
            res = cur.execute(req, params).fetchall()
            con.commit()
        self.wnd.close()
        self.window = SecondForm(*self.openinfo)
        self.window.show()

    def get_card_number(self):
        """
            Происходит чтение номера карты из окна
        """
        card_num = self.cardData.text()
        if not (card_num.isdigit() and len(card_num) == 16):
            raise CardFormatError("Неверный формат номера")
        return card_num

    def double(self, x):
        """
         Функция для проверки карты
         Основано на условиях, описанных в уроке QT 3. Обработка исключений.
        """
        res = x * 2
        if res > 9:
            res = res - 9
        return res

    def luhn_algorithm(self, card):
        """
             Функция для проверки карты
             Основано на условиях, описанных в уроке QT 3. Обработка исключений.
        """
        odd = map(lambda x: self.double(int(x)), card[::2])
        even = map(int, card[1::2])
        if (sum(odd) + sum(even)) % 10 == 0:
            return True
        else:
            raise CardLuhnError("Недействительный номер карты")

    def process_data(self):
        """
        Выдает финальный вердикт о проверке карты
        Запуск печати текста в файл
        """
        try:
            number = self.get_card_number()
            if self.luhn_algorithm(number):
                self.errorLabel.setText('Оплата успешно прошла! Проверьте ваш репозиторий на наличие чека')
                self.print_bill()
        except CardError as e:
            self.errorLabel.setText('Ошибка! ' + str(e))

    def keyPressEvent(self, event):
        """
        Закрытие окна по нажатию клавиши Esc
        Предупреждение отсутствует
        """
        if event.key() == Qt.Key_Escape:
            self.close()

    def create_code(self):
        """
        Функция генерирует код из рандомных цифр длинной в 15 символов
        """
        code = ''
        for i in range(15):
            code += str(randint(0, 9))
        return code

    def print_bill(self):
        """
        Печать чека в файл bill.txt
        Содержит информацию о:
            Время и Название фильма
            Выбранные места
            Общая стоимость
            Зал, в котором будет показ
            Уникальный код билета
        """
        st = ''
        with open('bill.txt', 'w', encoding='utf-8') as f:
            st += 'Чек о покупке билетов' + '\n'
            st += '----------------------' + '\n'
            st += 'Билеты на ' + self.info[1][1:-1] + ' в ' + self.info[2][1:-1] + '\n'
            st += 'Места '
            k = 0
            allcost = 0
            i = 0
            for el in self.seats:
                i += 1
                k = 0
                for letrs in el.split()[:-1]:
                    if k == 0:
                        allcost += 280
                    st += str(int(letrs) + 1)
                    k += 1
                    if k == 1:
                        st += ' ряд '
                    else:
                        st += ' место '
                if len(self.seats) != i:
                    st += '; '
            st += '\n'
            st += 'Стоимость: ' + str(allcost) + ' руб.'
            st += '\n'
            st += 'Зал ' + self.info[-1] + '\n'
            st += 'Номер брони: '
            code = 0
            while code not in self.uniccode:
                code = self.create_code()
                if code not in self.uniccode:
                    self.uniccode.append(code)
            st += str(code) + '\n'
            st += '----------------------' + '\n'
            st += 'ООО "Кинотеатр Премьер" \n'
            st += '----------------------' + '\n'
            f.write(st)
            f.close()
            self.finally_book(self.seats)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = FirstForm()
    ex.show()
    sys.exit(app.exec())
