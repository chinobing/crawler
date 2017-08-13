CREATE DATABASE IF NOT EXISTS datapro;

USE datapro;

# 以下所有的表不一定所有的值都有



CREATE TABLE IF NOT EXISTS project_background(
  id INT PRIMARY KEY AUTO_INCREMENT,
  project_name VARCHAR(100),
  duty VARCHAR(100),
  start_time VARCHAR(10),
  end_time VARCHAR(10),
  description VARCHAR(3000)
);

CREATE TABLE IF NOT EXISTS work_show(
  id INT PRIMARY KEY  AUTO_INCREMENT,
  link VARCHAR(1000),
  description VARCHAR(3000)
);

CREATE TABLE IF NOT EXISTS custom_block(
  id INT PRIMARY KEY  AUTO_INCREMENT,
  item_name VARCHAR(3000),
  item_desc VARCHAR(3000)
);

CREATE TABLE IF NOT EXISTS skill_assess(
  id INT PRIMARY KEY AUTO_INCREMENT,
  name VARCHAR(100),
  proficiency VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS expected_job(
  id INT PRIMARY KEY AUTO_INCREMENT,
  job_name VARCHAR(100),
  type VARCHAR(10),
  salary_max VARCHAR(10),
  salary_min VARCHAR(10),
  location VARCHAR(50),
  supplement VARCHAR(1000)
);

CREATE TABLE IF NOT EXISTS education_background(
  id INT PRIMARY KEY AUTO_INCREMENT,
  school_name VARCHAR(100),
  degree_type VARCHAR(10),
  majo VARCHAR(100),
  graduated_year VARCHAR(20)
);

CREATE TABLE IF NOT EXISTS work_background(
  id INT PRIMARY KEY AUTO_INCREMENT,
  company_name VARCHAR(100),
  job VARCHAR(100),
  desccription VARCHAR(3000),
  start VARCHAR(10),
  end VARCHAR(10)
);


CREATE TABLE IF NOT EXISTS user_info(
  id INT PRIMARY KEY AUTO_INCREMENT,
  hash_str VARCHAR(40) NOT NULL,    # hash 链接
  introduction VARCHAR(300),        # 一句话的自我介绍
  gender VARCHAR(10),               # 性别
  age VARCHAR(10),                  # 年龄
  degree_type VARCHAR(10),          # 学位类别:本科,硕士,博士
  work_company VARCHAR(200),        # 目前所在公司名称
  work_major VARCHAR(200),          # 目前的工作职位
  work_experience_year VARCHAR(100),    # 几年工作经验
  location VARCHAR(200),            # 目前所在地
  self_desc VARCHAR(1000),          # 自我描述
  work_type VARCHAR(10)             # 工作类型(工作经历/实习经历)
);