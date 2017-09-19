from customize_website.database import DBUtil


def null_value():
    sql = "select * from article_wechat where link = 'http://mp.weixin.qq.com/s?__biz=MjAzNzMzNTkyMQ==&mid=2653764049&idx=1&sn=cf788ea66b18a79e5b714bcb1f56bc49&chksm=4a8929cf7dfea0d9117aec86adaa198119ffc9b2481c9ae2f316627c6786b9f627f4ee7e0481&scene=27#wechat_redirect '"
    result = DBUtil.select_data(sql)
    print(str(result))


if __name__ == "__main__":
    null_value()