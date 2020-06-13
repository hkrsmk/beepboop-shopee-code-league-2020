from datetime import datetime, timedelta
import pandas as pd



def oneHourIntervalBrushing(data_hour):
    if len(data_hour['event_time']) == 1:
        # not brushing for sure
        return ""
    else:
#         calculate the concentrate rate
        unique_buyer_list = []
        suspicious_buyer = ""
        highest_order = 0
        unique_buyer_list = data_hour.userid.unique()
        num_orders = len(data_hour['shopid'])
        num_unique_buyers = len(unique_buyer_list)
        concentrate_rate = num_orders / num_unique_buyers
        if float(concentrate_rate) >= 3:
            # need to calculate propotion
            for each_buyer in unique_buyer_list:
                if len(data_hour[data_hour.userid == each_buyer]) > highest_order:
                    highest_order = len(data_hour[data_hour.userid == each_buyer])
                    suspicious_buyer = each_buyer
        return suspicious_buyer

def uniqueShopBrushing(data_shop):
    starting_time = data_shop['event_time'].iloc[0]
    # print(starting_time)
    buyerid_str_list = "0"
    if len(data_shop['event_time']) == 1 :
        buyerid = oneHourIntervalBrushing(data_shop)
        if buyerid == "":
            pass
    for i in range(0, len(data_shop['event_time'])):
        date_str = data_shop['event_time'].iloc[i]
        starting_time_obj = datetime(int(date_str[0:4]), int(date_str[5:7]), int(date_str[8:10]), int(date_str[11:13]),
                                     int(date_str[14:16]), int(date_str[17:19]))

        for j in range(i+1, len(data_shop['event_time'])):

            date_str = data_shop['event_time'].iloc[j]
            ending_time_obj = datetime(int(date_str[0:4]), int(date_str[5:7]), int(date_str[8:10]),
                                         int(date_str[11:13]),
                                         int(date_str[14:16]), int(date_str[17:19]))
            if ending_time_obj > (starting_time_obj + timedelta(hours=1)):
                buyerid = oneHourIntervalBrushing(data_shop[i:j])
                if buyerid == "" :
                    pass
                else:
                    if buyerid_str_list == "0":
                        buyerid_str_list = str(buyerid)
                    else:
                        if str(buyerid) in str(buyerid_str_list):
                            pass
                        else:

                            buyerid_str_list = str(buyerid_str_list) + ("&")
                            buyerid_str_list = str(buyerid_str_list) + (str(buyerid))
                break

    return buyerid_str_list


def brushing():
    data = pd.read_csv("./order_brush_order.csv")

    data = data.sort_values(by=['shopid', 'event_time'])
    # data = data.head(n=10000)
    shopid_list = data.shopid.unique()
    final_shopid = []
    final_buyerid_str_list = []
    for indiv_shop in shopid_list:
        # print(data.loc[data['shopid'] == indiv_shop])

        buyerid_str_list = uniqueShopBrushing(data.loc[data['shopid'] == indiv_shop])
        final_shopid.append(indiv_shop)
        final_buyerid_str_list.append(buyerid_str_list)

    final_dataframe = pd.DataFrame({'shopid':   final_shopid,
                   'userid': final_buyerid_str_list})
    # print(final_shopid)
    # print(final_buyerid_str_list)
    final_dataframe.to_csv("./output.csv", index=False)
if __name__ =="__main__":

    brushing()
