from lxml import etree


def parse_single_value(html,  match, pos=0):
    list_tmp = html.xpath(match)
    result = None
    if list_tmp:
        result = list_tmp[pos].text
    else:
        result = ""
    return result


def open_file(path):
    with open(path, 'rt') as f:
        data = f.read()
    return data


def cum_blo():
    html = etree.HTML(open_file('./test_parse_resources/custom_block.html'))
    print("title: " + parse_single_value(html, '//*[@id="customBlock"]/div/div[1]/div/div/div/span'))
    div = html.xpath('//*[@id="customBlock"]/div/div[2]')[0]
    data = etree.tostring(div, method='text', encoding='utf-8').decode().replace(' ', "")
    print("desc: " + data)


def work_exp():
    html = etree.HTML(open_file('./test_parse_resources/work_experience.html'))
    print("company: " + parse_single_value(html, '//*[@id="workExperience"]/div/div[2]/div/div/div[1]/div[1]/div/h4'))
    print("job: " + parse_single_value(html, '//*[@id="workExperience"]/div/div[2]/div/div/div[1]/div[1]/div/h4'))
    print('start-end: ' + parse_single_value(html, '//*[@id="workExperience"]/div/div[2]/div/div/div[1]/div[2]/span'))
    print('desc: ' + parse_single_value(html, '//*[@id="workExperience"]/div/div[2]/div/div/div[2]/p'))


def edu_bak():
    html = etree.HTML(open_file('./test_parse_resources/edu_background.html'))
    print("school: " + parse_single_value(html, '//*[@id="educationalBackground"]/div/div[2]/div/div[1]/div[2]/h4'))
    print('type-major: ' + parse_single_value(html, '//*[@id="educationalBackground"]/div/div[2]/div/div[1]/div[2]/span'))
    print('graduated_year: ' + parse_single_value(html, '//*[@id="educationalBackground"]/div/div[2]/div/div[2]/span'))


def expect_job():
    html = etree.HTML(open_file('./test_parse_resources/expect_job.html'))
    print("job: " + parse_single_value(html, '//*[@id="expectJob"]/div/div[2]/div/div[1]/ul/li[1]/span'))
    print('type: ' + parse_single_value(html, '//*[@id="expectJob"]/div/div[2]/div/div[1]/ul/li[2]/span'))
    print('location: ' + parse_single_value(html, '//*[@id="expectJob"]/div/div[2]/div/div[1]/ul/li[3]/span'))
    print('salary: ' + parse_single_value(html, '//*[@id="expectJob"]/div/div[2]/div/div[1]/ul/li[4]/span'))
    print('supplement: ' + parse_single_value(html, '//*[@id="expectJob"]/div/div[2]/div/div[2]/div/p'))


def pro_exp():
    html = etree.HTML(open_file('./test_parse_resources/pro_experience.html'))
    node = html.xpath('//*[@id="projectExperience"]/div/div[2]/div/div')
    data = etree.tostring(node[0].xpath('div/div/div/a')[0], method='text', encoding='utf-8').decode().replace('\n', "")
    print(data)
    print(parse_single_value(node[0], 'div[1]/div[1]/div/p'))
    print(parse_single_value(node[0], 'div[1]/div[2]/span'))
    print(parse_single_value(node[0], 'div[2]/p[1]'))


def sel_desc():
    html = etree.HTML(open_file('./test_parse_resources/self_desc.html'))
    node = html.xpath('//*[@id="selfDescription"]/div/div[2]/div[2]')
    data = etree.tostring(node[0], method='text', encoding='utf-8').decode().replace('\n', "").replace(' ', '')
    print(data)


def skill_assess():
    html = etree.HTML(open_file('./test_parse_resources/skill_assess.html'))
    print(parse_single_value(html, '//*[@id="skillsAssess"]/div/div[2]/div[1]/span[1]'))
    print(parse_single_value(html, '//*[@id="skillsAssess"]/div/div[2]/div[1]/span[3]'))


def work_show():
    html = etree.HTML(open_file('./test_parse_resources/work_show.html'))
    print(parse_single_value(html, '//*[@id="worksShow"]/div/div[2]/div[1]/div/div[2]/a'))
    node = html.xpath('//*[@id="worksShow"]/div/div[2]/div[1]/div/div[3]')
    data = etree.tostring(node[0], method='text', encoding='utf-8').decode().replace(" ", '')
    print(data)


# html = etree.HTML(open_file('./test_parse_resources/test.html'))
# parser = Parser(html)
# parser.parse()
# print(parser.user_info)