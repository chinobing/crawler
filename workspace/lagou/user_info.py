class UserInfo(object):
    """用户的基本信息"""

    def __init__(self):
        self.link = ''  # 简历的链接hash值
        self.intro = ''  # 自我简介(一句话)
        self.gender = ''  # 性别
        self.age = ''  # 年龄
        self.edu_type = ''  # 学位类别
        self.cur_company = ''  # 当前工作公司
        self.cur_major = ''  # 当前工作类别 (比如UI设计师, java后台等).
        self.work_year = ''  # 工作经验(年)
        self.pos = ''  # 目前所在地
        self.self_des = ''  # 自我描述
        self.work_type = ''  # 实习/工作
        self.work_exp = []  # 工作/实习经历
        self.edu_exp = []  # 教育经历
        self.exp_work = None  # 期望工作
        self.work_show = []  # 作品展示
        self.project_exp = []  # 项目经历
        self.skill_assess = []  # 技能评价
        self.custom_block = None  # 自定义模块

    def add_work_exp(self, exp):
        self.work_exp.append(exp)

    def add_edu_exp(self, exp):
        self.edu_exp.append(exp)

    def add_work_show(self, show):
        self.work_show.append(show)

    def add_skill_assess(self, skill):
        self.skill_assess.append(skill)

    def add_project_exp(self, exp):
        self.project_exp.append(exp)

    def __str__(self):
        if not self.link:
            self.link = ''  # 简历的链接hash值
        if not self.intro:
            self.intro = ''  # 自我简介(一句话)
        if not self.gender:
            self.gender = ''  # 性别
        if not self.age:
            self.age = ''  # 年龄
        if not self.age:
            self.edu_type = ''  # 学位类别
        if not self.age:
            self.cur_company = ''  # 当前工作公司
        if not self.age:
            self.cur_major = ''  # 当前工作类别 (比如UI设计师, java后台等).
        if not self.age:
            self.work_year = ''  # 工作经验(年)
        if not self.age:
            self.pos = ''  # 目前所在地
        if not self.age:
            self.self_des = ''  # 自我描述
        if not self.age:
            self.work_type = ''  # 实习/工作
        work = ""
        for exp in self.work_exp:
            work = exp.to_string() + ";" + work
        edu = ""
        for exp in self.edu_exp:
            edu = exp.to_string() + ";" + edu
        pro = ""
        for exp in self.project_exp:
            pro = exp.to_string() + ";" + pro
        skill = ""
        for s in self.skill_assess:
            skill = s.to_string() + ";" + skill
        show = ""
        for ws in self.work_show:
            show = ws.to_string() + ";" + show
        if not self.custom_block:
            self.custom_block = CustomBlock()
        if self.exp_work is None:
            self.exp_work = ExpectedWork()
        return (self.link + ',' +
                self.intro + "," +
                self.gender + "," +
                self.age + "," +
                self.edu_type + "," +
                self.cur_company + "," +
                self.cur_major + "," +
                self.work_year + "," +
                self.pos + "," +
                self.self_des + "," +
                self.exp_work.to_string() + "," +
                self.custom_block.to_string() + "," +
                "{" + self.work_type + ":" + work + "}," +
                "{" + edu + "}," +
                "{" + pro + "}," +
                "{" + skill + "}," +
                "{" + show + "}").replace('\n', '-')


# 注意实习经历与工作经历只有一个,应届生是实习经历,已经工作则是工作经历
# class InternshipExperience(object):
#     """实习经历"""
#     def __init__(self):
#         self.company = ''            # 实习公司
#         self.pos = ''                # 实习职位
#         self.start = ''              # 开始时间
#         self.end = ''                # 结束时间(至今换算为当前时间)
#         self.desc = ''               # 工作描述
#
#     def to_string(self):
#         return self.company + "," + \
#                self.start + "," + \
#                self.end + "," + self.desc


class WorkExperience(object):
    """工作/实习经历"""

    def __init__(self):
        self.type = ''
        self.company = ''  # 公司名称
        self.start = ''  # 开始时间
        self.end = ''  # 结束时间
        self.job = ''  # 职位
        self.desc = ''  # 工作描述

    def to_string(self):
        return self.company + "," + \
               self.start + "," + \
               self.end + "," + \
               self.job + "," + self.desc


class EducationBackground(object):
    """教育经历"""

    def __init__(self):
        self.school_name = ''  # 学校名称
        self.type = ''  # 学位类别
        self.major = ''  # 专业
        self.graduated_year = ''  # 毕业年份

    def to_string(self):
        return self.school_name + "," + \
               self.type + "," + \
               self.major + "," + \
               self.graduated_year


class ProjectExperience(object):
    """项目经验"""

    def __init__(self):
        self.project_name = ''  # 项目名称
        self.my_work = ''  # 项目职责
        self.start = ''  # 项目开始时间
        self.end = ''  # 项目结束时间
        self.desc = ''  # 对项目的描述

    def to_string(self):
        return self.project_name + "," + \
               self.my_work + "," + \
               self.start + "," + \
               self.end + "," + \
               self.desc


class WorkShow(object):
    """作品展示"""

    def __init__(self):
        self.link = ''  # 作品链接/作品标题
        self.desc = ''  # 作品描述

    def to_string(self):
        return self.link + "," + \
               self.desc


class ExpectedWork(object):
    """期望工作"""

    def __init__(self):
        self.job = ''
        self.type = ''  # 全职/兼职
        self.location = ''  # 工作地点
        self.salary_min = ''  # 最低薪资
        self.salary_max = ''  # 期望薪资
        self.sup = ''  # 补充说明

    def to_string(self):
        return self.job + "," + \
               self.type + "," + \
               self.location + "," + \
               self.salary_min + "," + \
               self.salary_max + "," + \
               self.sup


class SkillAssess(object):
    """技能评价"""

    def __init__(self):
        self.skill_name = ''  # 技能名称
        self.skill_pro = ''  # 技能熟练程度

    def to_string(self):
        return self.skill_name + "," + self.skill_pro


class CustomBlock(object):
    """自定义模块"""

    def __init__(self):
        self.item_name = ''  # 自定义模块名
        self.item_desc = ''  # 自定义模块描述

    def to_string(self):
        return self.item_name + "," + self.item_desc
