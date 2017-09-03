CREATE TABLE IF NOT EXISTS article_link(
  id INT PRIMARY KEY AUTO_INCREMENT,
  biz VARCHAR(100),
  link varchar(300),
  title varchar(100),
  page_view INT,
  thumb_number INT,
  html_path VARCHAR(300)
);