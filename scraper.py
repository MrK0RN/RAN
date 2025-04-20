import json
import os
import re

from bs4 import BeautifulSoup

import science


class Scraper:

    def __init__(self):
        self.all_science = None
        self.file = None
        self.new_science = None
        self.soup = ""
        self.files = os.listdir("/Users/user/PycharmProjects/ran/pers_files")

    @staticmethod
    def clear_text(text):
        if len(text) < 1:
            return ""
        if text is not None:
            text = text.replace("\n", "")
            if text is not None:
                text = text.replace("\t", "")
                while text.find("  ") != -1:
                    text = text.replace("  ", " ")
                if len(text) < 1:
                    return ""
                if text[0] == " ":
                    text = text[1:]
                if len(text) < 1:
                    return ""
                if text[-1] == " ":
                    text = text[:-1]

        return text

    @staticmethod
    def clear_exc_nums(text):
        return re.sub("\D", "", text)

    def array_to_tags(self, cards):
        res = ""
        for card in cards:
            res += ("#" + self.clear_text(card.text))
        return res

    def parse_everybody(self):
        self.all_science = {}
        i = 0
        for file in self.files:
            i+=1
            with open("pers_files/"+file, "r") as f:
                u = f.read()
            self.soup = BeautifulSoup(u, "html.parser")
            #print(file)
            if self.is_404():
                self.file = file
                self.parse_one_person()
                self.all_science[i] = self.new_science.ret_slov()
                with open('data.json', 'w') as f:
                    json.dump(self.all_science, f, indent=4, ensure_ascii=False)
            else:
                with open("empty_person.txt", "a") as f:
                    f.write(file)




    def parse_one_person(self):
        if self.is_404():
            self.new_science = science.science()
            self.parse_name()
            self.parse_tags()
            self.parse_contacts()
            self.parse_block()
            #print(self.new_science.ret_slov())

    def is_404(self):
        res = True
        lst = self.soup.find_all("p", class_="text text_gray")
        lst1 = self.soup.find_all("div", class_="error-code")
        if len(lst) + len(lst1)>0:
            res = False
        return res

    def parse_name(self):
        self.new_science.full_name = self.clear_text(self.soup.find_all("h1", class_="page-title page-title_person")[0].text)
        #print(self.new_science.full_name)
        if len(self.new_science.full_name) == 0:
            pass
            #print(len(self.new_science.full_name))

    def parse_tags(self):
        self.new_science.tags = ""
        stat = self.soup.find("div", class_="person-card__status")
        if stat is not None:
            cards = stat.find_all("span", class_="person-card__status-item text")
            self.new_science.role = self.clear_text(cards[0].text)
            self.new_science.tags = self.array_to_tags(cards)
        #print(self.new_science.tags)

    def parse_contacts(self):
        con_card = self.soup.find("div", class_="person-card__bottom")
        row = con_card.find("div", class_="person-card__info")
        if row is not None:
            rows = row.find_all("div", class_="person-card__info-item row")
            for s in rows:
                sts = s.find_all("div", class_= "col-12 col-sm-4 col-lg-3")
                for st in sts:
                    h = self.clear_text(st.text).split(" ")[0]
                    match h:
                        case "Телефоны":
                            self.new_science.telephone = ""
                            tels = self.clear_text(s.find("div", class_ = "col-12 col-sm-8 col-lg-9").text).split("+")
                            for tel in tels:
                                self.new_science.telephone += (" "+self.clear_exc_nums(tel))
                            self.new_science.telephone = self.clear_text(self.new_science.telephone)
                        case "Адрес":
                            self.new_science.mail = self.clear_text(s.find("div", class_="col-12 col-sm-8 col-lg-9").text)
                        case "Факс":
                            self.new_science.fax = ""
                            tels = self.clear_text(s.find("div", class_="col-12 col-sm-8 col-lg-9").text).split("+")
                            for tel in tels:
                                self.new_science.fax += (" " + self.clear_exc_nums(tel))
                            self.new_science.fax = self.clear_text(self.new_science.fax)
                        case _:
                            print("!#!#!#!#!#!##!!#!##!#!!#!#!#!#!#!##!!#!##!#!!#!#!#!#!#!##!!#!##!#!!#!#!#!#!#!##!!#!##!#!!#!#!#!#!#!##!!#!##!#!!#!#!#!#!#!##!!#!##!#!")
                            print(h)

        #print(self.new_science.telephone)
        #print(self.new_science.fax)
        #print(self.new_science.mail)

    def parse_block(self):
        blocks = self.soup.find_all("div", attrs={"class": {"block", "block_top-b"}})
        for block in blocks:
            h21 = block.find("h2")
            if h21 is None:
                pass
                #print(block)
            else:
                h2 = self.clear_text(h21.text)
                match h2:
                    case "Академические должности":
                        result = []
                        flag = True
                        posts = block.find("div", class_="person-jobs half-accord__content").find_all("div")

                        for post in posts:
                            if flag:
                                flag = False
                                continue
                            res = {}
                            rows = post.find_all("div")
                            for row in rows:
                                #print(row)
                                if row.find("p", class_="person-jobs__text person-jobs__text-gray d-block d-sm-none") is not None:
                                    p = self.clear_text(row.find("p", class_="person-jobs__text person-jobs__text-gray d-block d-sm-none").text)
                                    match p:
                                        case "Должность":
                                            res["role"] = self.clear_text(
                                                row.find_all("p", class_="person-jobs__text")[1].text)
                                            #print(1)

                                        case "Организационная структура":
                                            res["struct"] = self.clear_text(
                                                row.find("div", class_="person-jobs__line").text)
                                            #print(2)

                                        case "Дата активности":
                                            res["date"] = self.clear_text(
                                                row.find_all("p", class_="person-jobs__text")[1].text)
                                            #print(3)

                                        case _:
                                            print("#############")
                                            print(p)
                            if res != {}:
                                result.append(res)
                        self.new_science.positions = result

                    case "Профиль":
                        gg_s = block.find("div", class_="tags mt-xl-10 mt-6")
                        if gg_s is not None:
                            a_s = gg_s.find_all("a")
                            rt = []
                            for a in a_s:
                                rt.append(self.clear_text(a.text))
                            self.new_science.key_words = rt
                            #print(rt)
                        result = {}
                        rte = block.find("div", class_="rte")
                        if rte is not None:
                            p_s = rte.find_all("p")

                            for p in p_s:
                                reims = str(p).replace(" ", "").replace(".", "").replace("•", "").replace("\xa0", "").replace("\u200e", "").lower()
                                if re.search(r"0{4}-0{3}\d-\d{4}-\d{4}", reims):
                                    result["ORCID"] = re.search(r"0{4}-0{3}\d-\d{4}-\d{4}", reims).group(0)
                                if re.search(r"[a-zA-Z]-\d{4}-\d{4}", reims):
                                    result["Web Of Science"] = re.search(r"[a-zA-Z]-\d{4}-\d{4}", reims).group(0)
                                if re.search(r"ринц:\d{4, 5}", reims) or re.search(r"\d{4}-\d{4}", reims):
                                    result["РИНЦ"] = re.search(r"ринц:\d{4, 5}", reims).group(0)[4:] if re.search(r"ринц:\d{4, 5}", reims) else re.search(r"\d{4}-\d{4}", reims).group(0)
                                if re.search(r"\d{10,11}", reims):
                                    result["Scopus"] = re.search(r"\d{10,11}", reims).group(0)
                        sources = list(result.keys())
                        if len(result) > 0:
                            self.new_science.profiles = []
                            for source in sources:
                                self.new_science.profiles.append({"source":source, "id":result[source]})

                        #print(self.new_science.profiles)

