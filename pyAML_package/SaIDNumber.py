
import pandas as pd
import numpy as np


class SaIDNumber:

    def __init__(self, id_field):
        """

        :param id_field: A pandas DataFrame column for a South African ID Number
        """
        self.id_field = str(id_field)

    @classmethod
    def is_valid_sa_id(cls, id_field):

        valid_sa_id = False
        id_field = str(id_field)

        def digits_of(n):
            if str(n).isnumeric():
                return [int(digit) for digit in str(n)]
            else:
                return [-1]

        digits = digits_of(id_field)
        odd_digits = digits[-1::-2]
        even_digits = digits[-2::-2]
        checksum = 0
        checksum += sum(odd_digits)
        for d in even_digits:
            checksum += sum(digits_of(d * 2))

        if checksum % 10 != 0:
            valid_sa_id = False

        if checksum % 10 == 0:
            valid_sa_id = True

        return valid_sa_id

    @classmethod
    def get_gender(cls, id_field):

        id_field = str(id_field)
        if not cls.is_valid_sa_id(id_field):
            return np.nan
        if cls.is_valid_sa_id(id_field) & int(id_field[6]) >= 5:
            return 'Female'
        if cls.is_valid_sa_id(id_field) & int(id_field[6]) < 5:
            return 'Male'

    @classmethod
    def get_date_of_birth(cls, id_field):

        id_field = str(id_field)
        if not cls.is_valid_sa_id(id_field):
            return np.nan

        if cls.is_valid_sa_id(id_field):
            id_field = str(id_field)
            year = id_field[:2]
            month = id_field[2:4]
            day = id_field[4:6]
            # Determine the century based on the first digit or both first and second digits of the year
            if (year == '0') | (year == '00'):
                century = '20'
            else:
                century = '19'

            return century + year + '-' + month + '-' + day

    @classmethod
    def get_citizenship(cls, id_field):

        id_field = str(id_field)

        if not cls.is_valid_sa_id(id_field):
            return np.nan
        if cls.is_valid_sa_id(id_field) & int(id_field[10]) == 0:
            return 'South African'
        if cls.is_valid_sa_id(id_field) & int(id_field[10]) == 1:
            return 'Permanent South African Resident'
        if cls.is_valid_sa_id(id_field) & int(id_field[10]) == 2:
            return 'South African Refugee'

    @classmethod
    def get_genders_from_field(cls, id_field) -> list:
        """

        :return: This function returns a field for Genders that are derived from an ID number.
        """
        gender_field = id_field.apply(SaIDNumber.get_gender)
        return gender_field

    @classmethod
    def get_date_of_births_from_field(cls, id_field) -> list:
        """

        :return: This function returns a field for Date of Births that are derived from an ID number.
        """
        date_of_birth_field = id_field.apply(SaIDNumber.get_date_of_birth)
        return date_of_birth_field

    @classmethod
    def get_citizenship_from_field(cls, id_field) -> list:
        """

        :return: This function returns a field for Citizen Statuses that are derived from an ID number.
        """
        citizenship_field = id_field.apply(SaIDNumber.get_citizenship)
        return citizenship_field

#%%
