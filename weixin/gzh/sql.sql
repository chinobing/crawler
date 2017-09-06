# 描述每篇文章的表, 为了统一结构,把实时搜公众号与爬客户端结合起来了
# 实时搜没有biz, 爬客户端没有公众号名称,因此需要建一个映射表,映射biz到公众号名称
# 这样实时爬的链接亦可以放进来了, 还有一个问题就是实时爬的链接是否总是有效 (目前的解决办法是一旦链接失效
# 可以去搜狗中搜索,以题目为关键字,一般而言第一条结果就是目标链接了.

# 注意, 更换环境之前一定注意要运行SQL文件,创建好表.

CREATE TABLE IF NOT EXISTS article(
  id INT PRIMARY KEY AUTO_INCREMENT,
  biz VARCHAR(100),
  link varchar(300),
  title varchar(100),
  page_view INT,
  thumb_number INT,
  html_path VARCHAR(300)
);


CREATE TABLE IF NOT EXISTS article_wechat_map(
  id INT PRIMARY KEY  AUTO_INCREMENT,
  biz VARCHAR(100),
  wechat VARCHAR(100)
);