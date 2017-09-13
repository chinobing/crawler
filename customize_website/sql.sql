
# 每篇文章保存到数据库中,表结构如下
CREATE TABLE IF NOT EXISTS article_link(
  id INT PRIMARY KEY AUTO_INCREMENT,
  link varchar(500) NOT NULL,
  item_path VARCHAR(100) NOT NULL,
  title VARCHAR(100) NOT NULL,
  content_path VARCHAR(200) NOT NULL,
  html_path VARCHAR(200) NOT NULL,
  page_view INT NOT NULL DEFAULT 0,
  public_time DATE NOT NULL
);