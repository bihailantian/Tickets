#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

"""
命令行火车票查看器

Usage:
    tickets [-gdtkz] <from> <to> <date>

Options:
    -h,--help   显示帮助菜单
    -g          高铁
    -d          动车
    -t          特快
    -k          快速
    -z          直达
Example:
    tickets 北京 上海 2016-10-10
    tickets -dg 成都 南京 2016-10-10

"""

# 运行 python tickets.py -dg  北京 上海 2019-07-02
#  https://kyfw.12306.cn/otn/leftTicket/query?leftTicketDTO.train_date=2019-07-03&leftTicketDTO.from_station=BJP&leftTicketDTO.to_station=SHH&purpose_codes=ADULT

from docopt import docopt
from stations import stations

from colorama import init, Fore
import requests
from prettytable import PrettyTable

init()


class TrainsCollection:
    # 车次 车站 时间 历时 商务座特等座 一等座 二等座 软卧一等卧
    header = '车次 车站 时间 历时 商务座特等座 一等座 二等座 高级软卧 软卧一等卧 动卧 硬卧 二等卧 软座 硬座 无座 其他'.split()

    def __init__(self, available_trains, options, available_station):
        """查询到的火车班次集合
        :param available_trains: 一个列表, 包含可获得的火车班次, 每个
                                 火车班次是一个字典
        :param options: 查询的选项, 如高铁, 动车, etc...
        """
        self.available_trains = available_trains
        self.options = options
        self.available_station = available_station

    def _get_duration(self, raw_train):
        duration = raw_train.get('lishi').replace(':', '小时') + '分'
        if duration.startswith('00'):
            return duration[4:]
        if duration.startswith('0'):
            return duration[1:]
        return duration

    def _get_station(self, key):
        return self.available_station.get(key)

    @property
    def trains(self):
        for raw_train in self.available_trains:
            arr_train = raw_train.split("|")
            # print("--------------------------------------------")
            # print(raw_train)
            # print(arr_train)
            # print("--------------------------------------------")
            train_no = arr_train[3]
            from_station_name = self._get_station(arr_train[6])
            to_station_name = self._get_station(arr_train[7])

            # if from_station_name is None:
            #    print("arr_train[4]",arr_train[6])
            # if to_station_name is None:
            #    print("arr_train[4]",arr_train[7])
            # print([from_station_name,to_station_name])

            # 用##注释的表示已经确定是正确的数据
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
            yield train

    def pretty_print(self):
        pt = PrettyTable()
        pt._set_field_names(self.header)
        for train in self.trains:
            pt.add_row(train)
        print(pt)


def cli():
    """command-line interface"""
    arguments = docopt(__doc__)
    print(arguments)
    from_station = stations.get(arguments['<from>'])
    to_station = stations.get(arguments['<to>'])
    date = arguments['<date>']
    # 构建URL
    url = 'https://kyfw.12306.cn/otn/leftTicket/query?leftTicketDTO.train_date={}&leftTicketDTO.from_station={}&leftTicketDTO.to_station={}&purpose_codes=ADULT'.format(
        date, from_station, to_station)

    print(url)

    options = ''.join([key for key, value in arguments.items() if value is True])

    # 添加verify=False参数不验证证书
    r = requests.get(url, verify=False)
    # print(r.json())
    available_trains = r.json()['data']['result']
    available_station = r.json()['data']['map']
    TrainsCollection(available_trains, options, available_station).pretty_print()


if __name__ == '__main__':
    cli()
