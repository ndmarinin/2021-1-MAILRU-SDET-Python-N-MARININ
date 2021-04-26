from dataclasses import dataclass

import faker

fake = faker.Faker()



class Builder:

    @staticmethod
    def create_text():
        return fake.bothify(text='?????  ##### ?#?#?#?  #? # ?# ?# ? ? #? #? ?# ??#?')