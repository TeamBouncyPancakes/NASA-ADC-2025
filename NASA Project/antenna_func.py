import pandas as pd
def antenna_prioritize(row_no, filename):
    file = pd.read_csv(str(filename), dtype=int)
    row_data = file.iloc[row_no - 1]
    WPSA_stat = (row_data['WPSA'], 'WPSA')
    DS54_stat = (row_data['DS54'], 'DS54')
    DS24_stat = (row_data['DS24'], 'DS24')
    DS34_stat = (row_data['DS34'], 'DS34')
    availables = []
    for antenna_stat in (WPSA_stat, DS54_stat, DS24_stat, DS34_stat):
        if antenna_stat[0] == 1:
            availables.append(antenna_stat[1])
    if len(availables) > 0:
        link_budgets = {}
        for antenna_name in availables:
            link_budgets[antenna_name] = row_data[f'Link Budget {antenna_name}']
        link_budgets = list({key: value for key, value in sorted(link_budgets.items(), key=lambda item: item[1], reverse=True)}).keys()
        # sorts the dict according to values (highest to lowest)
        # then makes it a list and only takes the keys.
        # now we have a sorted list of antennas.
        return link_budgets