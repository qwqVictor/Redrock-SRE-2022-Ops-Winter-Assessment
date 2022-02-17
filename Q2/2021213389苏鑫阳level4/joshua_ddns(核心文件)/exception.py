# hostname 输入不匹配规定正则或则空
class HostnameError(Exception):
    def __str__(self):
        return 'hostname输入有误，请仔细检查'

# a记录 输入为空
class AError(Exception):
    def __str__(self):
        return 'a记录输入有误，请仔细检查'


# aaaa记录 输入为空
class AAAAError(Exception):
    def __str__(self):
        return 'aaaa记录输入有误，请仔细检查'


class ipv4InputError(Exception):
    def __str__(self):
        return 'ipv4地址输入有误，请仔细检查'

class ipv4GetError(Exception):
    def __str__(self):
        return '由于网络或配置不正确等原因，获取ipv4地址失败'

class ipv6GetError(Exception):
    def __str__(self):
        return '由于网络或配置不正确等原因，获取ipv6地址失败'

class ipv6InputError(Exception):
    def __str__(self):
        return 'ipv6地址输入有误，请仔细检查'


class ipInputError(Exception):
    def __str__(self):
        return '在您同时启用ipv46和指定ip模式后，您在IP参数后输入的指定ip的数量不等于2，请仔细检查'

class ipv6IsNotSupportedError(Exception):
    def __str__(self):
        return '当前设备不支持ipv6，不存在ipv6地址，请更换至ipv4模式'

class dnsConfigError(Exception):
    def __str__(self):
        return 'dns配置文件配置出错，请仔细检查参数是否指定了dns服务商以及所设置的参数是否正确'
class ipGetWayConfigError(Exception):
    def __str__(self):
        return '手动指定ip获取方式的配置文件配置出错，请查看help填入支持的获取方式，如果采取自定义方式获取ip，请确认命令返回值是否是合法的ip格式'

class configReadFail(Exception):
    def __str__(self):
        return '读取config文件失败，请检查是否指定的是有效config文件'
class configSectionError(Exception):
    def __init__(self, content):
        self.content = content
    def __str__(self):
        return 'config文件section部分配置错误，缺少section:'+self.content

class configValueIllegal(Exception):
    def __init__(self,content):
        self.content = content

    def __str__(self):
        return 'config文件'+self.content+'选项参数非法或未填写内容，请按照注释检查配置文件的参数正确性'


