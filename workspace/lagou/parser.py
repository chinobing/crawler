from .user_info import *
from lxml import etree
import re

class Parser(object):
    """解析HTML文件生成用户对象"""
    def __init__(self, html, link_hash):
        self.html = html
        self.user_info = UserInfo()
        self.user_info.link = link_hash

    def parse_single_value(self, html, match):
        list_tmp = html.xpath(match)
        result = None
        if list_tmp.__len__() > 0:
            result = list_tmp[0].text
        else:
            result = ""
        return result

    def parse_basic_info(self):
        base_info_ele = self.html.xpath('//*[@class="mr_baseinfo"]')
        if base_info_ele.__len__() > 0:
            base_info_ele = base_info_ele[0]
        else:
            return
        intro = base_info_ele.xpath('//*[@class="mr_intro"]')
        if intro.__len__() > 0:
            self.user_info.intro = etree.tostring(intro[0], method="text", encoding='utf-8').decode('utf-8')
        job_list = self.html.xpath("//*[@class=\"shenfen\"]")
        if job_list.__len__() > 0:
            split_str = etree.tostring(job_list[0], method='text', encoding='utf-8').decode('utf-8').split("·")
            self.user_info.cur_major = split_str[0]
            self.user_info.cur_company = split_str[1]
        else:
            self.user_info.cur_major = ""
            self.user_info.cur_company = ""

        self.user_info.gender = self.parse_single_value(base_info_ele, '//*[@class="s"]')
        self.user_info.age = self.parse_single_value(base_info_ele, '//*[@class="age"]')
        self.user_info.edu_type = self.parse_single_value(base_info_ele, '//*[@class="x"]')
        self.user_info.work_year = self.parse_single_value(base_info_ele, '//*[@class="job_span"]')
        self.user_info.pos = self.parse_single_value(base_info_ele, '//*[@class="mr0 d"]')

    def parse_work_experience(self):
        xpath_str = '//*[@id="workExperience"]'
        root = self.html.xpath(xpath_str)
        if root.__len__() == 0:
            return
        root = root[0]
        self.user_info.work_type = root.xpath('//*[@id="workExperience"]/div/div[1]/div/div/span[2]')[0].text
        com_list = root.xpath('//*[@id="workExperience"]/div/div[2]/div/div/div[1]/div[1]/div/h4')
        job_list = root.xpath('//*[@id="workExperience"]/div/div[2]/div/div/div[1]/div[1]/div/span')
        time_list = root.xpath('//*[@id="workExperience"]/div/div[2]/div/div/div[1]/div[2]/span')
        desc_list = root.xpath('//*[@id="workExperience"]/div/div[2]/div/div/div[2]')
        for i in range(com_list.__len__()):
            we = WorkExperience()
            we.company = com_list[i].text
            we.job = job_list[i].text
            if desc_list.__len__() > i:
                we.desc = etree.tostring(desc_list[i], method='text', encoding='utf-8').decode().replace(' ', '')
            time = time_list[i].text.split('—')
            if time.__len__() >= 2:
                we.start = time[0]
                if time[1] == '至今':
                    we.end = '2017/07'
                else:
                    we.end = time[1]
            self.user_info.add_work_exp(we)

    def parse_edu_background(self):
        xpath_str = '//*[@id="educationalBackground"]/div/div[2]/div'
        root = self.html.xpath(xpath_str)
        for i in range(root.__len__()):
            data = etree.tostring(root[i], encoding="utf-8", method='text').decode()
            strs = re.sub(r'\s+(.*?)\s+(.*?)\s+([.^\s]*?)\s+', r'\1-\2-\3', data).split('-')
            eb = EducationBackground()
            eb.school_name = strs[0]
            eb.graduated_year = strs[2]
            tm = strs[1].split('·')
            if tm.__len__() == 2:
                eb.type = tm[0]
                eb.major = tm[1]
            self.user_info.add_edu_exp(eb)

    def parse_pro_experience(self):
        xpath_str = '//*[@id="projectExperience"]/div/div[2]/div/div'
        root = self.html.xpath(xpath_str)
        for i in range(root.__len__()):
            pe = ProjectExperience()
            pe.project_name = etree.tostring(root[i].xpath('div/div/div/a')[0], method='text', encoding='utf-8').\
                decode().replace('\n', "").replace(' ', '')
            pe.my_work = self.parse_single_value(root[i], 'div[1]/div[1]/div/p')
            time = self.parse_single_value(root[i], 'div[1]/div[2]/span').split('-')
            if time.__len__() == 2:
                pe.start = time[0]
                pe.end = time[1]
            tmp = root[i].xpath('div[2]')
            if tmp.__len__() > 0:
                pe.desc = etree.tostring(tmp[0], method='text', encoding='utf-8').decode().replace(' ', '')
            self.user_info.add_project_exp(pe)

    def parse_work_show(self):
        xpath_str = '//*[@id="worksShow"]/div/div[2]/div'
        node = self.html.xpath(xpath_str)
        for i in range(node.__len__()):
            ws = WorkShow()
            ws.link = self.parse_single_value(node[i], 'div/div[2]/a')
            ws.desc = self.parse_single_value(node[i], 'div/div[3]/p')
            self.user_info.add_work_show(ws)

    def parse_self_desc(self):
        xpath = '//*[@id="selfDescription"]/div/div[2]/div[2]'
        node = self.html.xpath(xpath)
        if node.__len__() == 0:
            return
        self.user_info.self_des = etree.tostring(node[0], method='text', encoding='utf-8').decode().replace(' ', '')

    def parse_exp_job(self):
        xpath_str = '//*[@id="expectJob"]'
        root = self.html.xpath(xpath_str)
        if root.__len__() == 0:
            return
        root = root[0]
        exp_work = ExpectedWork()
        exp_work.job = self.parse_single_value(root, '//*[@id="expectJob"]/div/div[2]/div/div[1]/ul/li[1]/span')
        exp_work.type = self.parse_single_value(root, '//*[@id="expectJob"]/div/div[2]/div/div[1]/ul/li[2]/span')
        exp_work.location = self.parse_single_value(root, '//*[@id="expectJob"]/div/div[2]/div/div[1]/ul/li[3]/span')
        salary = self.parse_single_value(root, '//*[@id="expectJob"]/div/div[2]/div/div[1]/ul/li[4]/span')
        if salary:
            salary =salary.split('-')
            if salary.__len__() >= 2:
                exp_work.salary_min = salary[0]
                exp_work.salary_max = salary[1]
        sup = root.xpath('//*[@id="expectJob"]/div/div[2]/div/div[2]')
        if sup.__len__() > 0:
            exp_work.sup = etree.tostring(sup[0], method='text', encoding='utf-8').decode().replace(' ', '')
        self.user_info.exp_work = exp_work

    def parse_skill_assess(self):
        xpath_str = '//*[@id="skillsAssess"]/div/div[2]/div'
        root = self.html.xpath(xpath_str)
        for i in range(root.__len__()):
            sa = SkillAssess()
            sa.skill_name = self.parse_single_value(root[i], 'span[1]')
            sa.skill_pro = self.parse_single_value(root[i], 'span[3]')
            self.user_info.add_skill_assess(sa)

    def parse_custom_block(self):
        xpath_str = '//*[@id="customBlock"]'
        root = self.html.xpath(xpath_str)
        if root.__len__() == 0:
            return
        root = root[0]
        cb = CustomBlock()
        cb.item_name = self.parse_single_value(root, '//*[@id="customBlock"]/div/div[1]/div/div/div/span')
        div = root.xpath('//*[@id="customBlock"]/div/div[2]')
        if div.__len__() > 0:
            div = div[0]
            cb.item_desc = etree.tostring(div, method='text', encoding='utf-8').decode().replace(' ', "")
        self.user_info.custom_block = cb

    def parse(self):
        self.parse_basic_info()
        self.parse_custom_block()
        self.parse_edu_background()
        self.parse_exp_job()
        self.parse_self_desc()
        self.parse_pro_experience()
        self.parse_skill_assess()
        self.parse_work_experience()
        self.parse_work_show()
