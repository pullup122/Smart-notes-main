from PyQt5.QtWidgets import*
import json

try:
    with open("notes_data.json", "r", 
        encoding="utf-8") as file:
        notes = json.load(file)
except:
    notes = {}

app = QApplication([])
app.setStyleSheet("""
    QWidget {
        background-color: black ;
        color : #ffffff;
        font-size: 25px;
    }

    QPushButton {
        background-color: purple;
        color : #aaaaff;
        border-radius: 7px ;
        border-color: #3232ff;
        border-style: hidden;
        border-width: 5px;
        min-height: 20px;
        font-size: 25px;
        font-family: none;

    }
                  
    QPushButton:hover{
        background-color: red;
    }

    QLabel {
        background-color: #3545D5 ;
        color : #ffffff;
        font-size: 25px;
    }
    
    QTextEdit {  
        background-color: #35D59B ;
        color : #ffffff;
        font-size: 25px;
    }
    
    QListWidget {
        background-color: #70D535 ;
        color : #ffffff;
        font-size: 25px;
    }
    
    QLineEdit {
        background-color: #D5C535 ;
        color : #ffffff;
        font-size: 25px;
    }
""")

window = QWidget()
window.resize(750, 400)
mainline = QHBoxLayout()

baton1 = QPushButton('створити замітку')
baton2 = QPushButton('видалити замітку')
baton3 = QPushButton('зберегти замітку')
baton4 = QPushButton('додати до замітки')
baton5 = QPushButton('відкріпити від замітки')
baton6 = QPushButton('Шукати замітки за тегом')
text1 = QLabel('список заміток')
text2 = QLabel('список тегів')
pole1 = QTextEdit()
pole2 = QListWidget() # список записів
pole3 = QListWidget() # список тегів
pole4 = QLineEdit()

linepole = QVBoxLayout()
linemenu = QVBoxLayout()
line1 = QHBoxLayout()
line2 = QHBoxLayout()

mainline.addLayout(linepole)
mainline.addLayout(linemenu)
linepole.addWidget(pole1)
linemenu.addWidget(text1)
linemenu.addWidget(pole2)
line1.addWidget(baton1)
line1.addWidget(baton2)
linemenu.addLayout(line1)
linemenu.addWidget(baton3)
linemenu.addWidget(text2)
linemenu.addWidget(pole3)
linemenu.addWidget(pole4)
line2.addWidget(baton4)
line2.addWidget(baton5)
linemenu.addLayout(line2)
linemenu.addWidget(baton6)

def add_note():
    note_name, ok = QInputDialog.getText(window, "Додати замітку", "Назва замітки")
    if ok and note_name != "":
        notes[note_name] = {
            "текст": "",
            "теги": []
        }
        pole2.clear()
        pole1.clear() 
        pole2.addItems(notes)

        with open("notes_data.json", "w", encoding="utf-8") as file:
            json.dump(notes, file, ensure_ascii=False)

def save_note():
    if pole2.selectedItems():
        key = pole2.selectedItems()[0].text()
        notes[key]["текст"] = pole1.toPlainText()
        with open("notes_data.json", "w", encoding="utf-8") as file:
            json.dump(notes, file, ensure_ascii=False)
    else:
        print("Замітка для збереження не вибрана!")


def show_note():
    # отримуємо текст із замітки з виділеною назвою та відображаємо її в полі редагування
    key = pole2.selectedItems()[0].text()
    print(key)
    pole1.setText(notes[key]["текст"])
    pole3.clear()
    pole3.addItems(notes[key]["теги"])


def del_note():
    if pole2.selectedItems():
        key = pole2.selectedItems()[0].text()
        notes.pop(key)
        pole2.clear()
        pole3.clear()
        pole1.clear()
        pole2.addItems(notes)
        with open("notes_data.json", "w", encoding="utf-8") as file:
            json.dump(notes, file, sort_keys=True, ensure_ascii=False)
        print(notes)
    else:
        print("Замітка для вилучення не обрана!")


def add_tag():  # кнопка добавити тег
    if pole2.selectedItems():
        key = pole2.selectedItems()[0].text()
        tag = pole4.text()
        if not tag in notes[key]["теги"]:
            notes[key]["теги"].append(tag)
            pole3.addItem(tag)
            pole4.clear()
        with open("notes_data.json", "w", encoding="utf-8") as file:
            json.dump(notes, file, ensure_ascii=False)
        print(notes)
    else:
        print("Замітка для додавання тега не обрана!")


def del_tag():  # кнопка видалити тег
    if pole3.selectedItems():
        key = pole2.selectedItems()[0].text()
        tag = pole3.selectedItems()[0].text()
        notes[key]["теги"].remove(tag)
        pole3.clear()
        pole3.addItems(notes[key]["теги"])
        with open("notes_data.json", "w", encoding="utf-8") as file:
            json.dump(notes, file, ensure_ascii=False)
    else:
        print("Тег для вилучення не обраний!")


def search_tag():  # кнопка "шукати замітку за тегом"
    button_text = baton6.text()
    tag = pole4.text()

    if button_text == "Шукати замітки за тегом":
        apply_tag_search(tag)
    elif button_text == "Скинути пошук":
        reset_search()


def apply_tag_search(tag):
    notes_filtered = {}
    for note, value in notes.items():
        if tag in value["теги"]:
            notes_filtered[note] = value

    baton6.setText("Скинути пошук")
    pole2.clear()
    pole3.clear()
    pole2.addItems(notes_filtered)


def reset_search():
    pole4.clear()
    pole2.clear()
    pole4.clear()
    pole2.addItems(notes)
    baton6.setText("Шукати замітки за тегом")


baton1.clicked.connect(add_note)
baton2.clicked.connect(del_note)
baton3.clicked.connect(save_note)
baton4.clicked.connect(add_tag)
baton5.clicked.connect(del_tag)
baton6.clicked.connect(search_tag)
pole2.itemClicked.connect(show_note)

window.setLayout(mainline)
window.show()

pole2.addItems(notes)

app.exec()
