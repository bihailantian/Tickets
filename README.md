# Tickets
火车票查询工具

- 用##注释的表示已经确定是正确的数据
```python
 train = [
                train_no,  ## 车次
                '\n'.join([Fore.GREEN + from_station_name + Fore.RESET,
                           Fore.RED + to_station_name + Fore.RESET]),  # @ 车站
                '\n'.join([Fore.GREEN + arr_train[8] + Fore.RESET,
                           Fore.RED + arr_train[9] + Fore.RESET]),  ##时间
                arr_train[10],  ##历时
                arr_train[-7],  ##商务座特等座
                arr_train[-8],  ##一等座
                arr_train[-9],  ##二等座
                arr_train[-14],  # 高级软卧
                arr_train[-16],  # 软卧一等座
                arr_train[-12],  # 动卧
                arr_train[-13],  # 硬卧
                arr_train[-11],  # 二等卧
                arr_train[-15],  # 软座
                arr_train[-10],  ##硬座
                arr_train[-17],  # 无座
                arr_train[-18],  # 其他
            ]
```