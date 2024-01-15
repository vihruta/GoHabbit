from dataclasses import dataclass


@dataclass(frozen=True)
class PromocodesInfo:
    promocodes = ['CODEBREAKERS2023', 'CODEBREAKERS2022']

    promocode_date = {
        "CODEBREAKERS2023": [2023, 12, 19],
        "CODEBREAKERS2022": [2022, 10, 19]
    }
