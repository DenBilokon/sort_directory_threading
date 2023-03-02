import re


class Checking:
    def check(self, *args):
        raise NotImplementedError


class NameCheck(Checking):
    def check(self, name):
        """Normalize names from cyrillic to latin"""
        cyrillic_symbols = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
        translations = (
            "a",
            "b",
            "v",
            "g",
            "d",
            "e",
            "e",
            "j",
            "z",
            "i",
            "j",
            "k",
            "l",
            "m",
            "n",
            "o",
            "p",
            "r",
            "s",
            "t",
            "u",
            "f",
            "h",
            "ts",
            "ch",
            "sh",
            "sch",
            "",
            "y",
            "",
            "e",
            "yu",
            "ya",
            "je",
            "i",
            "ji",
            "g",
        )
        trans = {}
        for i, j in zip(cyrillic_symbols, translations):
            trans[ord(i)] = j
            trans[ord(i.upper())] = j.upper()
            name_list = name.split(".")
            name_list[0] = name_list[0].translate(trans)
            name_list[0] = re.sub("\W+", "_", name_list[0])
            if len(name_list) > 1:
                name = f"{name_list[0]}.{name_list[1]}"
            else:
                name = f"{name_list[0]}"
        return name
