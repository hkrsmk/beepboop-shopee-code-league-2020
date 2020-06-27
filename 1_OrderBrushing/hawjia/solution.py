import numpy as np
import pandas as pd

# low_memory flag to prevent mixed type inference
data = pd.read_csv('../data/order_brush_order.csv', low_memory=False)

# convert datetime string to unix time
import datetime
format_str = '%Y-%m-%d %H:%M:%S'
data['event_time'] = data['event_time'].apply(lambda x: datetime.datetime.strptime(x, format_str))
data['event_time'] = data['event_time'].apply(lambda x: x.timestamp())

# get unique shops
# sort cos ocd
shops = data['shopid'].unique()
shops.sort()
shops = shops.tolist()

# Get all orders per shop sorted by time

# Just a helper function to return orders corresponding to a shopid
def get_shop_orders(shopid):
    return data.loc[lambda df: df['shopid'] == shopid, :]

# This list will contain tuples of (shopid, orders-dataframe)
shop_orders = []

for id in shops:
    orders = get_shop_orders(id)
    orders = orders.sort_values(by=['event_time'])
    shop_orders.append((id, orders))

def get_purchase_count(userid, orders):
    order_count = len(orders[orders.userid == userid])
    return userid, order_count

cases = {}

for shopid, orders in shop_orders:
    if not shopid in cases:
        cases[shopid] = []

    # iterate through all orders
    for i in range(len(orders)):
        order_time = orders['event_time'].iloc[i]
        one_hour_mark = order_time + 3600

        # filter out orders that are within one hour
        within_one_hour = orders[orders.event_time >= order_time]
        within_one_hour = within_one_hour[within_one_hour.event_time < one_hour_mark]

        # Calculate concentration
        order_count = len(within_one_hour)
        unique_buyers = within_one_hour['userid'].unique()

        unique_buyer_count = len(unique_buyers)
        concentration = order_count / unique_buyer_count

        if concentration >= 3:
#             print()
#             print('Order brushing detected')
#             print('Shop id: ' + str(shopid))
#             print('Orders: ')
#             print(within_one_hour)
#             print('Concentration: ' + str(concentration))

            # Find the user with the highest proportion
            buyer_purchase_count = list(map(lambda x: get_purchase_count(x, within_one_hour), unique_buyers.tolist()))
            buyer_purchase_count.sort(key=lambda x: x[1], reverse=True)
#             print(buyer_purchase_count)

            # Add user to order brushing cases
            cases[shopid].append(buyer_purchase_count[0][0])

            # Take into consideration other buyers with some proportion
            for j in range(1, len(buyer_purchase_count)):
                if buyer_purchase_count[j][1] == buyer_purchase_count[0][1]:
                    cases[shopid].append(buyer_purchase_count[j][0])
                else:
                    break

# Remove repeated offenders in cases
for key in cases.keys():
    cases[key] = list(set(cases[key]))


result = {}

# Convert to submission format
for key in cases.keys():
    if len(cases[key]) == 0:
        result[key] = '0'
    else:
        print(cases[key])
        result[key] = '&'.join(list(map(lambda x: str(x), cases[key])))

csv = {}
csv['shopid'] = []
csv['userid'] = []

for key in result.keys():
    csv['shopid'].append(key)
    csv['userid'].append(result[key])

csv = pd.DataFrame.from_dict(csv)

# Export to csv
csv.to_csv('results.csv', columns=['shopid', 'userid'], index=False)
