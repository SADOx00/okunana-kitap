import ast
import datetime
import sqlite3
import sys
import questionary
from termcolor import colored
from rich.console import Console
from rich.panel import Panel
from rich import box
from rich.table import Table
from rich.text import Text
from rich.traceback import install
import os
install()
columns = os.get_terminal_size().columns

class Inter_face:
    def __init__(self):
        self.console = Console()
        self.entrance()

    def centered_text(self, text, width):
        # Metni satır satır ortala
        lines = text.split("\n")
        centered_lines = [line.center(width) for line in lines]
        return "\n".join(centered_lines)

    def entrance(self):
        text = colored( "Proje: db_of_books e hoşgeldiniz efendim.\n\n1)okuduğum kitapları göster\n2)kitabın bilgilerini getir \n3)kitap ekle\n".upper(), "blue",attrs=["bold"])
        text = self.centered_text(text=text, width=columns)

        panel = Panel(
            text,
            box=box.DOUBLE_EDGE,
            title=colored(self.centered_text(text="SADO",width=15), "light_red", on_color="on_black", attrs=["bold"]),
            title_align="center"

        )
        self.console.print(panel)
        while True:

            answer = questionary.select("\nhangi seçenek: ",choices=[
                "quit(çıkış)".upper(),
                "1)okuduğum kitapları göster".upper(),
                "2)kitabın bilgilerini getir".upper(),
                "3)kitap ekle".upper()

            ]).ask()
            if answer == "quit(çıkış)".upper():
                sys.exit()
            elif answer[0] =="3":
                """
                türü sen ekle
                """
                name = questionary.text("the name of the book: ".upper()).ask()
                name = str(name).lower()
                author = questionary.text("the author of the book: ".upper()).ask()
                page = questionary.text("the page of the book: ".upper()).ask()
                kind = questionary.checkbox("kitabın türü: ".upper(),choices=[
                    "OTO-BİYOGRAFİ",
                    "KİŞİSEL GELİŞİM",
                    "PSİKOLOJİ",
                    "LİDERLİK-YÖNETİM",
                    "İŞ DÜNYASI",
                    "SİSTEM DÜŞÜNCESİ"
                ]).ask()
                kind=str(kind)
                summarize = questionary.confirm("summarize.txt dosyasını doldurdunuzmu? ".upper()).ask()
                if not summarize:
                    print(colored("!!! o zaman ilk önce girin sonra gelin !!!".upper(),
                                  color="red", attrs=["bold", "underline"]))
                    sys.exit()

                my_notes = questionary.confirm("my_notes.txt dosyasını doldurdunuzmu? ".upper()).ask()
                if not my_notes:
                    print(colored("!!! o zaman ilk önce girin sonra gelin !!!".upper(),
                                  color="red", attrs=["bold", "underline"]))
                    sys.exit()
                with open("summarize.txt","r",encoding="utf-8") as file:
                    content = file.read()
                summarize =content

                with open("my_notes.txt","r",encoding="utf-8") as file:
                    content = file.read()
                my_notes =content

                db = sqlite3.connect("books.db")
                cr = db.cursor()

                cr.execute('SELECT COUNT(*) FROM books')
                num = cr.fetchone()[0]
                num = num +1


                date = str(datetime.datetime.now().timestamp())
                try:
                    cr.execute("insert into books (name , author, summarize, my_notes, pages, date, kind,id) values(?,?,?,?,?,?,?,?)",
                               (name, author, summarize, my_notes, page, date, kind, num))
                    db.commit()
                except:
                    print(colored("!!! kitap eklenirken bir hata oluştu !!!".upper(),
                                  color="red", attrs=["bold", "underline"]))
                else:
                    print(colored("!!! kitap başarıyla eklendi !!!".upper(),
                                  color="green", attrs=["bold", "underline"]))
                db.close()
            elif answer[0] == "1":
                db = sqlite3.connect("books.db")
                cr = db.cursor()

                cr.execute("select name, author, pages, date,  kind, id from books ")
                rslts = cr.fetchall()

                table = Table(title=colored("Kitaplar: ".upper(), color="red", on_color="on_black",
                                            attrs=["bold", "underline"]), box=box.DOUBLE_EDGE, width=columns)
                table.add_column("ID", style="green")
                table.add_column("NAME", style="blue")
                table.add_column("author".upper(), style="magenta")
                table.add_column("PAGES", style="blue")
                table.add_column("DATE", style="magenta")
                table.add_column("KİNDS", style="blue")



                for i in rslts:
                    name = i[0]
                    author = i[1]
                    page = i[2]
                    date =datetime.datetime.fromtimestamp(float(i[3]))
                    date = f"{date.year}-{date.month}-{date.day}"
                    kinds = i[4]
                    num = i[5]

                    table.add_row(str(num), name.upper(), author.upper(), page, date,kinds)

                self.console.print(table)
                db.close()
            elif answer[0] == "2":
                answer = questionary.text("KİTAP ID: ").ask()
                answer = int(answer)

                db = sqlite3.connect("books.db")
                cr = db.cursor()
                try:
                    cr.execute("select name, author, pages, date, kind, id from books where id=? ",(answer,))
                    rslts = cr.fetchall()
                    if len(rslts) == 0:
                        raise NameError
                except:
                    print(colored("!!! kitap alınırken bir hata oluştu !!!".upper(),
                                  color="red", attrs=["bold", "underline"]))
                else:

                    table = Table(title=colored("Kitap: ".upper(), color="red", on_color="on_black",
                                                attrs=["bold", "underline"]), box=box.DOUBLE_EDGE, width=columns)
                    table.add_column("ID", style="green")
                    table.add_column("NAME", style="blue")
                    table.add_column("author".upper(), style="magenta")
                    table.add_column("PAGES", style="blue")
                    table.add_column("DATE", style="magenta")
                    table.add_column("KİNDS", style="blue")


                    for i in rslts:
                        name = i[0]
                        author = i[1]
                        page = i[2]
                        date = datetime.datetime.fromtimestamp(float(i[3]))
                        date = f"{date.year}-{date.month}-{date.day}"
                        kinds = i[4]
                        num = i[5]

                        table.add_row(str(num), name.upper(), author.upper(), page, date, kinds)

                    self.console.print(table)

                    cr.execute("select summarize, my_notes from books where id = ?",(answer,))
                    rslts = cr.fetchall()

                    table = Table(title=colored("Kitap: ".upper(), color="red", on_color="on_black",
                                                attrs=["bold", "underline"]), box=box.DOUBLE_EDGE, width=columns)

                    table.add_column("SUMMARIZE", style="magenta")
                    table.add_column("MY_NOTES", style="blue")

                    num = 1
                    for i in rslts:


                        table.add_row(i[0].upper(),i[1].upper())
                        num += 1
                    self.console.print(table)

                    db.close()








Inter_face()
