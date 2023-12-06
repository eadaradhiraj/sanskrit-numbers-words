from dataclasses import dataclass, field

import sys

if sys.version_info >= (3, 11):
    from typing import Self
else:
    from typing_extensions import Self

HINDU_NUMS = {
    "०": "0",
    "१": "1",
    "२": "2",
    "३": "3",
    "४": "4",
    "५": "5",
    "६": "6",
    "७": "7",
    "८": "8",
    "९": "9",
}

class InvalidInputException(Exception):
    pass

@dataclass
class SktNumToWord:
    number: int | None = None
    skt_num: str | None = None
    def __post_init__(self):
        if not self.skt_num and not self.number:
            raise InvalidInputException(
                "Either integer should be given \
                    as an input or Sanskrit numerals\
                         should be provided."
            )
        if not self.number:
            self.number = int("".join([HINDU_NUMS.get(dig) for dig in skt_num]))
        self.num_dict = {
            0: {
                0: "",
                1: "एक",
                2: "द्वि",
                3: "त्रि",
                4: "चतुर्",
                5: "पञ्च",
                6: "षट्",
                7: "सप्त",
                8: "अष्ट",
                9: "नव",
            },
            1: {
                0: "",
                10: "दश",
                20: "विंशति",
                30: "त्रिंशत्",
                40: "चत्वारिंशत्",
                50: "पञ्चाशत्",
                70: "सप्तति",
                80: "अशीति",
                90: "नवति",
            },
            2: "शत",
            3: "सहस्र",
            4: "अयुत",
            5: "लक्ष",
            6: "प्रयुत",
            7: "कोटि",
            8: "दशकोटि",
            9: "महापद्म",
            10: "सहस्रकोटि",
            11: "लक्षकोटि",
            12: "दशलक्षकोटि",
            13: "शतलक्षकोटि",
            14: "सहस्रलक्षकोटि",
            15: "लक्षलक्षकोटि",
        }

    @property
    def break_down(self) -> tuple:
        """returns tuple as a variable

        Returns:
            tuple: list of numbers that sums up to become the original number
        """
        return self.__break_down()

    def __break_down(self) -> tuple:
        """Divide number into sum of powers of 10

        Returns:
            tuple: list of numbers
        """
        if self.number == 0:
            return 0
        result = []
        divisor = 10
        power = 0
        curr_num = self.number
        while curr_num > 0:
            digit = curr_num % divisor
            result.append(digit * 10**power)
            curr_num //= divisor
            power += 1
        return tuple(result)

    @property
    def words_list(self) -> tuple:
        """return list of sanskrit words for each number

        Returns:
            tuple: returns a tuple of sanskrit
        """
        return self.__words_list()

    def __words_list(self) -> tuple:
        """return list of sanskrit words for each number

        Returns:
            tuple: returns a tuple of sanskrit
        """
        _res = []
        for idx, num in enumerate(self.__break_down()):
            if num == 0:
                return ["शून्य"]
            if idx <= 1:
                _res.append(self.num_dict[idx].get(num))
            else:
                if num == 0:
                    continue
                if idx > 0:
                    _res.append("अधिक")
                _res.append(
                    f"{self.num_dict[0].get(int(str(num)[0]))} {self.num_dict[idx]}"
                )
        return tuple(_res)

    def __add__(self, obj: Self) -> Self:
        """overloading the + operator

        Args:
            obj (Self): takes similar object as additional argument

        Returns:
            Self: returns a another object of the same type
        """
        return self.__class__(number=self.number + obj.number)


print(SktNumToWord(number=123).break_down)
