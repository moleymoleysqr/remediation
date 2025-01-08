import pandas as pd
import numpy as np

output2 = pd.read_csv("C:\\Users\\X050096\\OneDrive - Old Mutual\\Documents\\XR Alignment 17122024\\Reverse "
                      "Engineered GCS_ID Golden Flow Output _lessColumns.csv", low_memory=False, encoding="ISO-8859-1")
country_look_up = pd.read_excel(
    "C:\\Users\\X050096\\OneDrive - Old Mutual\\Documents\\XR Alignment 17122024\\Continents & Countries File ES 1.xlsx",
    sheet_name='Country Dashboard')
xr_individuals = output2.merge(country_look_up, how='left', left_on='Overall Physical Postal COUNTRY',
                               right_on='Country')

del output2


class ReportingSubsets:
    def __init__(self, data):
        self.data = xr_individuals

    @property
    def off_books(self) -> list:
        """
        :param df: Output 1 of the Alteryx workflow
        :param subset: the subset of output 1. The default would be the active set of parties. but this can also be changed
        to track any subset that you want. For instance, you can try to account for parties that were sent for rating,
        or identified as duplicates.
        :return: returns a subset of partyid's that make up the set of customers with SA Products, and SA Addresses
        """
        off_books = self.data['partyid'][(self.data['OVERALL_AGREEMENT_STATUS'] == 'Off Books')]
        return off_books

    @property
    def deceased(self) -> list:
        """
        :param df: Output 1 of the Alteryx workflow
        :param excl: this is to exclude the off books population.
        :return: returns a subset of partyid's that make up the set of customers with SA Products, and SA Addresses
        """
        excl = self.off_books
        deceased = self.data['partyid'][(self.data['DHA_DeathStatus'] == 'DECEASED') &
                                        (~self.data['partyid'].isin(excl))]
        return deceased

    @property
    def non_sa_product(self) -> list:
        """
        :param df: Output 1 of the Alteryx workflow
        :param subset: the subset of output 1. The default would be the active set of parties. but this can also be changed
        to track any subset that you want. For instance, you can try to account for parties that were sent for rating,
        or identified as duplicates.
        :return: returns a subset of partyid's that make up the set of customers with SA Products, and SA Addresses
        """
        non_sa_product = self.data['partyid'][(self.data['Product Country'] == 'Namibia') &
                                              (~self.data['partyid'].isin([*self.deceased, *self.off_books]))]

        return non_sa_product

    @property
    def active_parties(self) -> list:
        """
        :param df: Output 1 of the Alteryx workflow :param subset: the subset of output 1. The default would be the
        active set of parties. but this can also be changed to track any subset that you want. For instance, you can try
        to account for parties that were sent for rating, or identified as duplicates. :return: returns a subset of
        partyid's that make up the set of customers with SA Products, and SA Addresses
        """

        excl_offbooks = self.off_books
        excl_deceased = self.deceased
        excl_non_sa = self.non_sa_product

        active_parties = self.data['partyid'][
            ~self.data['partyid'].isin([*excl_offbooks, *excl_deceased, *excl_non_sa])]
        return active_parties

    @property
    def sa_prod_sa_addr(self) -> list:
        """
        :param df: Output 1 of the Alteryx workflow :param subset: the subset of output 1. The default would be the
        active set of parties. but this can also be changed to track any subset that you want. For instance, you can try
        to account for parties that were sent for rating, or identified as duplicates. :return: returns a subset of
        partyid's that make up the set of customers with SA Products, and SA Addresses
        """

        sa_prod_sa_addr = self.data['partyid'][(self.data['Overall Physical Postal COUNTRY'] == 'SOUTH AFRICA')
                                               & (self.data['Product Country'] == 'South Africa')
                                               & (self.data['partyid'].isin(self.active_parties))]
        return sa_prod_sa_addr

    @property
    def sa_prod_non_sa_addr(self) -> list:
        """
        :param df: Output 1 of the Alteryx workflow :param subset: the subset of output 1. The default would be the
        active set of parties. but this can also be changed to track any subset that you want. For instance, you can try
        to account for parties that were sent for rating, or identified as duplicates. :return: returns a subset of
        partyid's that make up the set of customers with SA Products, and non SA Addresses
        """

        sa_prod_non_sa_addr = self.data['partyid'][(self.data['Overall Physical Postal COUNTRY'] != 'SOUTH AFRICA')
                                                   & (~self.data['Overall Physical Postal COUNTRY'].isna())
                                                   & (self.data['Product Country'] == 'South Africa')
                                                   & (self.data['partyid'].isin(self.active_parties))
                                                   ]
        return sa_prod_non_sa_addr

    @property
    def sa_prod_unknown_addr(self) -> list:
        """
        :param df: Output 1 of the Alteryx workflow
        :param subset: the subset of output 1. The default would be the active set of parties. but this can also be changed
        to track any subset that you want. For instance, you can try to account for parties that were sent for rating,
        or identified as duplicates.
        :return: returns a subset of partyid's that make up the set of customers with SA Products, and unknown Addresses
        """

        sa_prod_unknown_addr = self.data['partyid'][(self.data['Overall Physical Postal COUNTRY'].isna())
                                                    & (self.data['Product Country'] == 'South Africa')
                                                    & (self.data['partyid'].isin(self.active_parties))]
        return sa_prod_unknown_addr

    @property
    def unknown_prod_sa_addr(self) -> list:
        """
        :param df: Output 1 of the Alteryx workflow :param subset: the subset of output 1. The default would be the
        active set of parties. but this can also be changed to track any subset that you want. For instance, you can try
        to account for parties that were sent for rating, or identified as duplicates. :return: returns a subset of
        partyid's that make up the set of customers with unknown product countries and SA Addresses.
        """
        unknown_prod_sa_addr = self.data['partyid'][(self.data['Overall Physical Postal COUNTRY'] == 'SOUTH AFRICA')
                                                    & (self.data['Product Country'].isna())
                                                    & (self.data['partyid'].isin(self.active_parties))]
        return unknown_prod_sa_addr

    @property
    def unknown_prod_unknown_addr(self) -> list:
        '''
        :param df: Output 1 of the Alteryx workflow :param subset: the subset of output 1. The default would be the
        active set of parties. but this can also be changed to track any subset that you want. For instance, you can try
        to account for parties that were sent for rating, or identified as duplicates. :return: returns a subset of
        partyid's that make up the set of customers with unknown product countries and SA Addresses.
        '''

        unknown_prod_unknown_addr = self.data['partyid'][(self.data['Overall Physical Postal COUNTRY'].isna())
                                                         & (self.data['Product Country'].isna())
                                                         & (self.data['partyid'].isin(self.active_parties))]
        return unknown_prod_unknown_addr

    @property
    def unknown_prod_non_sa_addr(self) -> list:
        '''
        :param df: Output 1 of the Alteryx workflow :param subset: the subset of output 1. The default would be the
        active set of parties. but this can also be changed to track any subset that you want. For instance, you can try
        to account for parties that were sent for rating, or identified as duplicates. :return: returns a subset of
        partyid's that make up the set of customers with unknown product countries and SA Addresses.
        '''

        unknown_prod_non_sa_addr = self.data['partyid'][(self.data['Overall Physical Postal COUNTRY'] != 'SOUTH AFRICA')
                                                        & (~self.data['Overall Physical Postal COUNTRY'].isna())
                                                        & (self.data['Product Country'].isna())
                                                        & (self.data['partyid'].isin(self.active_parties))]
        return unknown_prod_non_sa_addr

    def add_segment(self):
        self.data['Segment_Ind'] = np.nan
        self.data['Segment_Ind'] = np.select([(self.data.RAF_OWNED_IND.isna() & self.data.RMM_OWNED_IND.isna() &
                                               self.data.NAM_RAF_OWNED_IND.isna() & self.data.NAM_RMM_OWNED_IND.isna()),
                                              ((self.data.RAF_OWNED_IND == 1) | (self.data.NAM_RAF_OWNED_IND == 1)),
                                              ((self.data.RMM_OWNED_IND == 1) | (self.data.NAM_RMM_OWNED_IND == 1))],
                                             [pd.NA, 'PF', 'MFC'], default='MFC')

        self.data['Sub_Segment'] = np.nan
        self.data['Sub_Segment'] = np.select([
            (self.data.Segment_Ind.isna()) & (self.data.UT_CLNT.isna()) & (self.data.GALAXY_CLNT.isna()),
            (self.data.UT_CLNT == 'Y') | (self.data.GALAXY_CLNT == 'Y'),
            (self.data.Segment_Ind == 'MFC') & ((self.data.UT_CLNT != 'Y') | (self.data.GALAXY_CLNT != 'Y')),
            (self.data.Segment_Ind == 'PF') & ((self.data.UT_CLNT != 'Y') | (self.data.GALAXY_CLNT != 'Y'))],
            [pd.NA, 'Wealth', 'MFC', 'PF'], default=np.nan)

    def country_column_split(self):
        non_sa_country_ = (self.data[['partyid', 'Country Category', 'Sub_Segment']][
                               self.data['partyid'].isin(self.sa_prod_non_sa_addr)]
                           .groupby(['Country Category', 'Sub_Segment'], dropna=False).agg('nunique').reset_index())
        non_sa_country_segment = non_sa_country_.pivot(index='Sub_Segment', columns='Country Category',
                                                       values='partyid').fillna('-')
        non_sa_country_segment = non_sa_country_segment.loc[:,
                                 ['Namibia', 'Swaziland', 'Lesotho', 'Rest of Africa', 'USA', 'UK', 'Other']]
        return non_sa_country_segment

    @property
    def non_sa_country_column(self):
        return self.country_column_split()

    def segment_reporting(self, subset: list, grouper: str = 'Sub_Segment', key: str = 'partyid') -> pd.DataFrame:
        '''
        :param df: this is base dataframe
        :param subset: this is a list of party ids for which you want to split by segment. Eg, sa_sa split into segments, or duplicate partyids.
        :param grouper: The default value is the Sub_Segment column. You may want to change it to Segment if required
        :param key: partyid

        usage
        _____
        segment_reporting(output2, subset=sa_sa)
        '''
        df_ = self.data.loc[:, [grouper, key]][self.data[key].isin(subset)]
        df_aggr = df_.groupby(grouper, dropna=False).agg({key: 'nunique'})
        return df_aggr

    @property
    def full_report(self):
        all_groups = [self.off_books, self.deceased, self.non_sa_product, self.active_parties,
                      self.sa_prod_sa_addr, self.sa_prod_non_sa_addr, self.sa_prod_unknown_addr,
                      self.unknown_prod_unknown_addr, self.unknown_prod_sa_addr, self.unknown_prod_non_sa_addr]
        names = ['off_books', 'deceased', 'non_sa', 'active_parties', 'sa_sa', 'sa_non_sa', 'sa_unknown',
                 'unknown_unknown', 'unknown_sa', 'unknown_nonSA']
        final = pd.concat([self.segment_reporting(subset=subsets) for subsets in all_groups], axis=1)
        final.columns = names

        a, b = final.reset_index().align(self.non_sa_country_column.reset_index(), join='left', axis=0)
        final_ = a.merge(b, how='left').drop_duplicates(subset = 'Sub_Segment', keep='first')

        order = ['Sub_Segment', 'off_books', 'deceased', 'non_sa', 'active_parties', 'sa_sa', 'sa_non_sa', 'Namibia',
                 'Swaziland', 'Lesotho', 'Rest of Africa', 'USA', 'UK', 'Other', 'sa_unknown', 'unknown_unknown',
                 'unknown_sa',
                 'unknown_nonSA']
        return final_.loc[:, order]

#%%
