import argparse

#解析命令行输入，输出成字典，传入option内optionmanager
class Parser(argparse.ArgumentParser):
    def parse_args_dict(self):
        return vars(super().parse_args())

    def __init__(self):
        super().__init__(prog="Joshua's DDNS脚本",
                         description="""
动态自动获取本机IP地址，与DNS解析结果比较，若不同则自动发起更新。
支持多平台DNS，多样化获取本机IP地址,支持从文本解析。顺带支持了下单纯的DNS功能。""",
                         )

        super().add_argument('-H', '--hostname', nargs=1, type=str, required=False, dest='hostname',
                             help='填写域名，注意不要加前缀。')

        super().add_argument('-a', '-A', nargs='*', type=str, required=False, dest='a',
                             help='在开启了ipv4模式后，将会启用此参数并且必须填写。若只开启ipv6模式，可以忽略此值。'
                                  '\n支持同时填写多个A记录，IP会同时记录在填写的多个记录之中。')

        super().add_argument('-aaaa', '-AAAA', nargs='*', type=str, required=False, dest='aaaa',
                             help='在开启了ipv6模式后，将会启用此参数，此时若参数为空，将会选择使用a参数下数据，若a参数也为空，则报错。'
                                  '\n若仅开启ipv4模式，可忽略此值支持。同时填写多个AAAA记录，IP会同时记录在填写的多个记录之中。')

        super().add_argument('-c', '--config', nargs='*', type=argparse.FileType(mode='r', encoding='utf-8' ), required=False, dest='configfile',
                             help='从指定文件中获取配置，格式为json格式。')
        super().add_argument('-i4', '--ipv4', action='store_true', dest='ipv4',
                             help='指定DNS的同步的IP类型为ipv4，默认类型为此值。若参数后填写了ip，则变为单纯dns功能，进行一次性的记录更新')
        super().add_argument('-i6', '--ipv6', action='store_true', dest='ipv6',
                             help='指定DNS的同步的IP类型为ipv6，若参数后填写了ip，则变为单纯dns功能，进行一次性的记录更新。'
                                  '\n指定的记录名应填至aaaa参数中，但开启此参数但把参数写在了a参数中，脚本会使用a参数中的值，但是发出erro警告，若a和aaaa字段都为空，则报错')
        super().add_argument('-i46', '--ipv46', action='store_true', dest='ipv46',
                             help='指定DNS的同步的IP类型为同时同步ipv4和ipv6，默认不填写为此值。若参数后填写了ip，则变为单纯dns功能，进行一次性的记录更新。'
                                  '\n指定的字段名应按照ipv4对应a参数ipv6对应aaaa参数进行填写，但若只设置了a或aaaa一个参数，脚本会自动选取有数据的那个参数并同步到另一个为空的参数。'
                                  '\n若都不填写，报错')
        super().add_argument('--cloudflare', nargs='*', type=str, dest='cloudflare',
                             help='更新域名托管在cloudflare，脚本调用cloudflare api进行操作'
                                  '\n添加此参数后，需依次填入cloudflare api令牌、要操作域名的zone id')
        super().add_argument('--tencentCloud', nargs='*', type=str, dest='tencentCloud',
                             help='更新域名托管在腾讯云(Dnspod)，脚本调用腾讯云 api进行操作'
                                  '\n添加此参数后，需依次填入腾讯云的secret_key_id、secret_key')
        super().add_argument('--aliYun', nargs='*', type=str, dest='aliYun',
                             help='(由于我在阿里云并没有域名，所以api也没办法测试，不保证能用/dog)更新域名托管在阿里云，脚本调用阿里云 api进行操作'
                                  '\n添加此参数后，需依次填入阿里云的access_key_id、access_key')
        super().add_argument('-ip', nargs='*', type=str, dest='ip_get_way_config',
                             help='手动指定脚本ip地址的获取方式，支持参数:\napi\n(默认,从在线api获取地址)'
                                  '\nnic\n(通过命令\'ip addr\'获取本机网卡上信息,不输入默认eth0)'
                                  '\ncmd\n(从输入命令的返回参数获得ip地址，注意返回只能单纯包含ip地址)'
                                  '\npython\n(从自定义pyhon脚本获取ip地址,此python文件应该实现getIP(mode)方法，其中mode传入参数为ipv4、ipv6.python文件若不在当前命令执行目录下,则应该输入绝对路径)'
                                  '\nsetted'
                                  '\n(设置此参数后，脚本将只进行dns功能，ip不再将自动获取，而是直接取该参数所指定ip地址'
                                  '\n若设置的是i4参数，则在此后填写ipv4的ip，反之，填写ipv6的ip'
                                  '\n若设置的是ipv46参数，则在此后按照ipv4、ipv6的顺序填入ip))')


