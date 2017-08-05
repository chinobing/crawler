/*!common/static/js/exposure.js*/
;/*
 * 曝光量统计
 *
 * 接口地址
 * https://a.lagou.com/json
 *
 * 参数 - 值 - 含义
 * lt   - trackshow                              - 日志输出类型 (固定取值)
 * a    - 9R00_idnull_0_id34_1992                - 编码id组（逗号分隔）
 * t    - p                                      - 曝光类型
 * v    - 0                                      - 版本号
 * dl   - http://www.lagou.com/jobs/618831.html  - 当前页URL
 * dr   - http://www.lagou.com                   - referrer
 * time - new Date().getTime()                   - 时间戳
 *
 * 使用方法
 * 1. 同步渲染节点添加如下属性即可
 *    data-tj-exposure="on"   =>   固定取值，开启曝光统计
 *    data-lg-tj-type="gg"    =>   曝光统计类型，自定义
 *    data-lg-tj-id="Sc00"    =>   编码ID，取值唯一。请到 http://meta.lagou.com/code 申请
 *    data-lg-tj-no="0001"    =>   节点位置编号
 *    data-lg-tj-cid="1043"   =>   业务ID
 *
 *  简招控制台通栏广告实例：
 *  <a data-tj-exposure="on" data-lg-tj-type="gg" data-lg-tj-id="Sc00" data-lg-tj-no="0001" data-lg-tj-cid="1043" href="http://activity.lagou.com/topic/rqzmax.html" target="_blank">
 *      <img src="http://www.lagou.com/i/image/M00/65/60/Cgp3O1gHTUyAFdxQAAECVS_3cu4129.JPG" alt="顶部通栏广告" class="a-x-d-banner" />
 *  </a>
 *
 * 2. 异步渲染节点除了添加第一条中的属性，需在节点插入文档DOM之后调用: exposure();
 *
 */

define('common/static/js/exposure', ['require', 'exports', 'module'], function (require, exports, module) {

    exports.exposure = exposure;

    var analyseUri = {
        jsonURL: window.location.protocol + '//a.lagou.com/json'
    };

    var nullVal = 'idnull'; // 字段为空取值

    /**
     * 判断 Array 对象
     */
    function _isArray(arr) {
        return Object.prototype.toString.call(arr) === '[object Array]';
    }

    /**
     * 发送广告曝光量统计
     *
     * @param  {Array} tjCodes  [要统计的编码ID组]
     * @param  {String} type    [曝光统计的类型]
     * @param  {Array} abts     [a/b-test类型，可选]
     */
    function _log(tjCodes, type, abts) {

        if (!_isArray(tjCodes)) {
            return;
        }

        var tjCodesStr = [];
        for (var i = 0; i < tjCodes.length; i++) {
            var tjItem = tjCodes[i];

            if (_isArray(tjItem) && tjItem.length >= 3) {
                tjCodesStr.push(_getTjId(tjItem[0], tjItem[1], tjItem[2]));
            }
        }
        ;

        var imgGet = new Image();
        var params = {
            "lt": 'trackshow',
            "a": tjCodesStr.join(','),
            "t": type,
            "v": 0,
            "dl": encodeURIComponent(window.location.href),
            "dr": encodeURIComponent(window.location.protocol + '//' + window.location.hostname),
            "time": new Date().getTime()
        }

        if (_isArray(abts)) { // A/B Test参数，暂时未使用
            params.abt = abts.join(',');
        }

        var paramsArr = [];
        for (var item in params) {
            paramsArr.push(item + '=' + params[item]);
        }
        imgGet.src = analyseUri.jsonURL + '?' + paramsArr.join('&');
    }

    /**
     * 获取编码统计ID
     */
    function _getTjId(id, no, cid) {
        return [$.trim(id), $.trim(no), 0, $.trim(cid), Math.round(Math.random() * 10000)].join('_');
    }

    function exposure() {
        $(document).ready(function () {
            var cache = {};

            $('[data-tj-exposure=on]').each(function () {
                var $me = $(this);
                var id = $me.attr('data-lg-tj-id');
                var no = $me.attr('data-lg-tj-no') || nullVal;
                var cid = $me.attr('data-lg-tj-cid') || nullVal;
                var group = $me.attr('data-lg-tj-group') || nullVal;
                var type = $me.attr('data-lg-tj-type') || group;

                if (!_isArray(cache[group])) {
                    cache[group] = [];
                    cache[group]['type'] = type;
                }
                cache[group].push([id, no, cid]);
                $me.attr('data-tj-exposure', 'off'); // 避免重复发送
            });

            for (var group in cache) {
                _log(cache[group], cache[group]['type']);
            }
        });
    }

    exposure(); // 统计页面同步节点曝光日志

    /* show日志曝光统计 post jobs id array to plat */
    exports.postoA = function (params) {
        if (!params) return;
        var arr = [];
        var img = new Image();
        for (var i in params) {
            arr.push(i + '=' + params[i]);
        }
        arr.push('time=' + new Date().getTime())
        img.src = document.location.protocol + '//a.lagou.com/show?' + arr.join('&');
    }

});

/*!common/widgets/report_list/main.js*/
;define('common/widgets/report_list/main', ['require', 'exports', 'module', "common/components/jquery-niceScroll/jquery.nicescroll.min", 'dep/artTemplate/dist/template', 'common/static/js/exposure'], function (require, exports, module) {
    // 以后请引用/common/components目录下修复了已知bug的nicescroll插件
    require("common/components/jquery-niceScroll/jquery.nicescroll.min");
    var template = require('dep/artTemplate/dist/template');
    var exposure = require('common/static/js/exposure').exposure;

    if ($('.report_diaglog').length > 0) {
        var report_diaglog = $('.report_diaglog')
        var report_pop = $('#report_pop')
        report_diaglog.show();
        report_pop.show();
        report_pop.animate({marginLeft: "-302px"}, 500)
        getReportList();
    }
    function getReportList() {
        $.ajax({
            url: GLOBAL_DOMAIN.ectx + "/industryReport/reportList.json",
            data: {
                companyId: $('#UserConpanyId').val()
            }
        }).done(function (rs) {
            if (rs.state == 1) {
                var tpl = "{{each reportList as item i}}\n<li class=\"relists\" data-id=\"{{item.id}}\">\n\t<span class=\"sopt\">[</span>\n\t<span class=\"speed_title\">{{item.seedTitle}}</span>\n\t<span class=\"sopt\">]</span>\n\t<a href=\"{{item.url}}\" class=\"title\" target=\"_blank\" data-tj-exposure=\"on\" data-lg-tj-type=\"news\" data-lg-tj-id=\"19aj\" data-lg-tj-no=\"{{if i < 9}}000{{i+1}}{{else}}0010{{/if}}\" data-lg-tj-cid=\"{{item.id}}\">{{item.title}}</a>\n\t<span class=\"delete report_delete\" data-id=\"{{item.id}}\" data-tj-exposure=\"on\" data-lg-tj-type=\"news\" data-lg-tj-id=\"19aj\" data-lg-tj-no=\"idnull\" data-lg-tj-cid=\"{{item.id}}\">不喜欢</span>\n</li>\n{{/each}}\n{{if reportList.length == 0}}\n\t<li class=\"no_report\">暂时没有报道，求职者无法查看，有内容时自动显示。</li>\n{{/if}}\n";
                var dataList = rs.content.data.companyReportList
                var htmlStr = template.compile(tpl)({
                    reportList: dataList
                });
                $('ul.report_list').append(htmlStr);
                $('.report_list').niceScroll({
                    cursorcolor: '#00b38a',
                    cursorborder: "2px solid #f8f8f8",
                    cursorwidth: "3px",
                    scrollspeed: 6,
                    cursorminheight: 60,
                    cursoropacitymax: 0.8

                });
                //曝光埋点
                exposure();
            }
        })
    }

    $(document).on('click', '.try_it', function () {
        $('.step1').hide();
    })
    $(document).on('click', '.think_btn,.is_cancel', function (e) {
        $.ajax({
            url: GLOBAL_DOMAIN.ectx + "/industryReport/cancelPop.json"
        }).done(function (rs) {
            if (rs.state == 1) {
                var report_diaglog = $('.report_diaglog')
                var report_pop = $('#report_pop')
                report_diaglog.hide();
                report_pop.hide();
            }
        })
    })
    $(document).on('click', '.rechecked', function () {
        $(this).addClass('recheck').removeClass('rechecked')
        $(this).data('state', '0')
    })
    $(document).on('click', '.recheck', function () {
        $(this).addClass('rechecked').removeClass('recheck')
        $(this).data('state', '1')
    })

    var arr_ids = [];
    $(document).on('click', '.report_delete', function () {
        arr_ids.push($(this).data('id'))
        $(this).parents('li.relists').remove();
        if ($('.report_list li').length == 0) {
            $('.report_list').append('<li class="no_report">暂时没有报道，求职者无法查看，有内容时自动显示。</li>')
        }
        $(".report_list").getNiceScroll().resize()
    })
    $(document).on('click', '.is_ok', function () {
        var ids = "";
        var updateState = $('.check_update i').data('state');
        ids = arr_ids.join(',')
        $.ajax({
            url: GLOBAL_DOMAIN.ectx + "/industryReport/submitReport.json",
            data: {
                reportIds: ids,
                updateState: updateState
            }
        }).done(function (rs) {
            if (rs.state == 1) {
                var report_diaglog = $('.report_diaglog')
                var report_pop = $('#report_pop')
                report_diaglog.hide();
                report_pop.hide();
                var newTab = window.open('about:blank');
                var url = "https://hr.lagou.com/company/gongsi/" + rs.content.data.lagouCompanyId + ".html"
                // window.open(url);
                newTab.location.href = url;

            }
        })
    })

});

/*!plus/modules/top-queries/main.js*/
;/**
 * plus 人才推荐常用搜索 queries
 *
 * @author fayipan@lagou.com
 */

define('plus/modules/top-queries/main', ['require', 'exports', 'module'], function (require, exports, module) {
    var $topQueries = $('#topQueries');
    var $list = $topQueries.find('.queries-list');
    var $helpTips = $topQueries.find('.help-tips');
    var cache = [];

    /**
     * 常用搜索说明文案
     */
    $topQueries.find('.icon-help-center').hover(function (e) {
        $helpTips.show();
    }, function (e) {
        $helpTips.hide();
    });

    /**
     * 常用搜索链接拼接（使用velocity处理较为麻烦）
     */
    $topQueries.find('.queries-list .query').each(function () {
        var $me = $(this).find('a');
        var data = JSON.parse($me.attr('data-json'));

        if (parseInt(data.pageNo, 10) === 1) { // 去掉 pageNo = 1 的过滤条件
            delete data.pageNo;
        }

        var params = [];
        for (var prop in data) {
            params.push(prop + '=' + encodeURIComponent(data[prop]));
        }

        $me.attr('href', GLOBAL_DOMAIN.ectx + '/search/result.htm?' + params.join('&'));
        cache.push(data); // 记录现有的过滤器
    });

    module.exports = {
        add: function (filters) {
            var params = [];
            var prop = '';

            for (prop in filters) {
                params.push(prop + '=' + encodeURIComponent(filters[prop]));
            }

            var index = -1;
            if (parseInt(filters.pageNo, 10) === 1) { // 去掉 pageNo = 1 的过滤条件
                delete filters.pageNo;
            }
            for (var i = cache.length - 1; i >= 0; i--) {
                var query = cache[i];
                var props = [];
                var match = true;

                for (prop in filters) {
                    props.push(prop);

                    if (query[prop] != filters[prop]) {
                        match = false;
                    }
                }

                for (prop in query) {
                    if (query.hasOwnProperty(prop) && props.indexOf(prop) === -1) {
                        match = false;
                        break;
                    }
                }

                if (match === true) {
                    index = i;
                    break;
                }
            }

            if (index === -1) { // 添加过滤器
                $list.prepend(
                    '<li class="query"><a href="' + GLOBAL_DOMAIN.ectx + '/search/result.htm?' + params.join('&') + '" target="_blank">' + filters.keyword + '</a></li>'
                );
            } else if (index >= 0) { // 前置过滤器
                var elem = $topQueries.find('.queries-list .query')[index];
                $list.prepend(elem);
                cache.splice(index, 1);
            }
            $topQueries.show();
            cache.unshift(filters);
        }
    }
});

/*!common/components/topTips/main.js*/
;/**
 * Created by lagou on 16/3/3.
 */
/**
 * 顶部tips
 */

/**

 lg.Widgets.Controls.TopTips({
 name:'xxx'         //控件实例名字
 hasNoBack:true     //是否含有遮罩层
 needHoverStop:true //鼠标放上去是否停顿
 decoration:'xxx'   //实例定义样式 className
 })

 lg.getxxx().setShow(true|false)             //显示或隐藏弹框

 */
(function (name, definition) {
    if (typeof module != 'undefined' && module.exports) module.exports = definition()
    else if (typeof define == 'function' && define.amd) define('common/components/topTips/main', [], definition)
    else this[name] = definition()
})('TopTips', function () {

    lg.Widgets.Controls.Extend("TopTips", function (controlType) {
        var _shieldChar;
        var control = function (options) {
            this._isValueField = false;
            this._id = lg.Utils.getRandom();
            this._element = this.getTemplete().attr('data-confirm-id', this._id);
            $('body').append(this._element);
            //lg.Widgets.BaseControl.call(this, options);

            this.init(options);
        };
        $.extend(control.prototype, lg.Event);
        control.prototype = new lg.Widgets.BaseControl();
        control.prototype.controlType = controlType;
        control.prototype.init = function (options) {
            //this.getElement().attr('data-id', lg.Utils.getRandom());
            if (options) {
                $.extend(this._option, options)
            }
            var that = this;
            if (this._option) {
                that.setElementHeader(that._option.header || '');

            }
            if (this._option.hasNoBack) {
                setTimeout(function () {
                    that.getElementBack().removeClass('lg-tranparent');
                }, 500);
            }
            this.getElementHeaderClose().on('click', function (e) {
                that.setRemove();
            });
            if (this._option.isBackClose == true) {
                this.getElementBack().on('click', function (e) {
                    that.setRemove();
                });
            }
            this.getElement().addClass('lg-toptips');
            var that = this;
            if (this._option.needHoverStop) {
                that.getElement().on('mouseover', function (e) {
                    clearTimeout(that.timeLine);
                    that.timeLine = setTimeout(function () {
                        that.setRemove();
                    }, 5000);
                });
                /*that.getElement().on('mouseover','.lg-confirm', function (e) {
                 that.setRemove();
                 });*/
                that.getElement().on('click', '.item-click', function (e) {
                    //clearTimeout(that.timeLine);
                    that.trigger('itemClick');
                    that.setRemove();
                });
            }
            if (this._option.decoration) {
                that.getElement().addClass(this._option.decoration);
            }
            this.timeLine = setTimeout(function () {
                that.setRemove();
            }, 5000);
        }
        control.prototype.getCancelBtn = function () {
            return this.getElement().find('.mds-confirm-concel');
        }
        control.prototype.getTemplete = function () {
            var templateStr = '<div class="lg-tranparent"><div class="lg-confirm clearfix" >'
                + '<div class="lg-confirm-title"><span class="title"></span><span class="MDS-icon-modal-close icon-close" aria-hidden="true"></span></div>'
                + '</div></div>';
            return $(templateStr);
        }

        control.prototype.setShow = function (val) {
            var value = false;
            if (val) {
                value = true;
            }
            value ? this.getElement().show() : this.getElement().hide();
        }
        control.prototype.getElementBack = function () {
            return $('[data-confirm-id="' + this._id + '"]') || this._element;
        }
        control.prototype.getElement = function () {
            return this.getElementBack().children('div');
        }
        control.prototype.setRemove = function () {
            this.getElementBack().remove();
        }
        control.prototype.getElementHeader = function () {
            return this.getElement().find('.lg-confirm-title .title');
        }
        control.prototype.setElementHeader = function (val) {
            this.getElement().find('.lg-confirm-title .title').html(val);
        }
        control.prototype.getElementHeaderClose = function () {
            return this.getElement().find('.lg-confirm-title .MDS-icon-modal-close');
        }
        control.prototype.setElementContent = function (val) {
            this.getElement().find('.lg-confirm-content').html(val);
        }
        return control;
    });
});
/*!common/widgets/open-recruit-service-pop/main.js*/
;define('common/widgets/open-recruit-service-pop/main', ['require', 'exports', 'module'], function (require, exports, module) {

    //协作帐号不能直接发布职位
    //
    //用js处理可能会有js没处理到就点击了发布职位的情况
    // if(window.CONST_VARS('user').isMyCompany === false && $('.create-position').length > 0) {
    //     $('.create-position').attr('href','#open-recruit-service-pop').attr('data-toggle','modal');
    // }
    //
    //

    var cache = {
        BUserInfo: {}
    };

    /**
     * [_getBUserInfo description]
     * @param  {Function} callback      /im/chat/getUserInfo.json接口请求成功之后调用的回调函数
     * @param  {[type]}   errorCallback /im/chat/getUserInfo.json接口请求失败之后调用的回调函数
     */
    function _getBUserInfo(callback, errorCallback) {
        if (cache.BUserInfo && cache.BUserInfo.userId) {
            typeof callback === 'function' && callback(cache.BUserInfo);
            return;
        }

        $.get('/im/chat/getUserInfo.json', function (resp) {
            var state = parseInt(resp.state, 10);
            if (state === 1) {
                cache.BUserInfo = resp.content.data;
                typeof callback === 'function' && callback(cache.BUserInfo);
            } else {
                typeof errorCallback === 'function' && errorCallback(state);
            }
        }, 'json');
    }

    /**
     * [judgeOpenServiceState description]
     * @param  {Function} callback 开通招聘服务判断通过之后调用的回调函数
     * @param  {object}   options  开通招聘服务判断通过之后调用的回调函数的参数
     */
    function judgeOpenServiceState(callback, options) {
        _getBUserInfo(function (info) {
            if (!info || !info.userId || !info.hasLagouCompany) {
                if ($('#open-recruit-service-pop').length > 0) {
                    $('#open-recruit-service-pop').modal('show');
                } else {
                    alert('你还没有在拉勾网开通招聘服务');//容错一下，基本用不到这个。
                }
                return;
            } else {
                typeof callback === 'function' && callback(options);
            }
        }, function (state) {
            alert('获取用户信息失败!');
        })
    }

    module.exports = {
        judgeOpenServiceState: judgeOpenServiceState
    }
})

/*!chat/modules/api/chat-api.js*/
;/**
 * Upgrade by fayipan@lagou.com (Created by jinglupeng on 1/11/16.)
 * 2016/09/08
 */
define('chat/modules/api/chat-api', ['require', 'exports', 'module', 'common/components/push/NotifyClient'], function (require, exports, module) {

    var notifyClient = require('common/components/push/NotifyClient');

    var cache = {
        startTime: +new Date(),
        sessions: [],          // 会话列表，顺序展现
        sessionMaps: {},       // 会话Maps，通过 sessionId 查询
        messages: {},          // 会话消息列表
        push: {
            status: false,     // push server 状态
            disConnectTime: -1
        },
        BUserInfo: {},               // B端用户信息，即当前 HR 的用户信息
        sessionListReady: undefined, // 会话列表初始化状态，防止重复请求
        latestReceiveMsg: undefined, // 最新接收到的消息（针对所有会话）
        sessionsMore: {              // 加载更多会话列表
            pageNo: 1,
            pageSize: 10,
            locked: true             // 确保先初始化会话列表，才能执行加载更多
        }
    };

    var _push = Array.prototype.push;
    var _unshift = Array.prototype.unshift;
    var _toString = Object.prototype.toString;

    // 连接上推送服务器
    notifyClient.bind('connect', function () {
        cache.push.status = true; // push server 连接成功
        console.info('connect');

        // 监听 推送断开
        notifyClient.bind('disconnect', function (event, time) {
            console.info('disconnect');

            if (cache.push.status === true) {
                cache.push.status = false; // push server 连接断开
                cache.push.disConnectTime = time;
            }
        });

        // 监听 推送重连成功
        notifyClient.bind('reconnect', function (event, time) {
            console.info('reconnect');

            if (cache.push.status === false) {
                cache.push.status = true; // push server 重连成功
            }
        });

        // WEB 端发送消息（HR使用简招发消息给C端，消息发送成功: 将web端随机生成临时 msgId 更新为正确的 msgId ）
        notifyClient.bind('IM_WEB_SEND_MESSAGE', function (event, resp) {
            resp = _string2JSON(resp);
            if (resp) {
                var message = resp.message;
                message.attach = resp.attach; // 前端发送的原样返回（web端随机生成临时 msgId ）
                _processMessage([message]);
            }
        });

        // APP 端发送消息（可能是B端消息, 也可能是C端消息）
        notifyClient.bind('IM_APP_SEND_MESSAGE', function (event, message) {
            message = _string2JSON(message);
            if (message) {
                _processMessage(message instanceof Array ? message : [message]);
            }
        });

        // 会话更新
        notifyClient.bind('IM_SESSION_UPDATE', function (event, message) {
            message = _string2JSON(message);
            if (message) {
                // {
                //    sessionId: 100011588,
                //    status: 128
                // }
                // 值域：
                // 会话状态被定义为一个short型的变量(2个字节).
                //      0x80:删除状态,二进制的形式是1000 0000;
                //      0x00:普通状态,二进制的形式是0000 0000;
                //      0x10:置顶状态,二进制的形式是0001 0000.
                //      0x100:屏蔽消息状态,二进制的形式是0000 0001 0000 0000
                //      0x200:禁止回复状态,二进制的形式是0000 0010 0000 0000
                //      0x400:非交互模式,二进制的形式是0000 0100 0000 0000
                // 一个用户的会话既可以是置顶状态,同时又是屏蔽消息状态,此时状态值是0x110,二进制形式是0000 0001 0001 0000;
                // 一个用户的会话即可以是置顶状态,又是删除状态,同时又是屏蔽消息状态,还可以是禁止回复状态,此时状态值是0x390,二进制形式是0000 0011 1001 0000.
                // 但是普通状态和置顶状态是互斥的.
                var status = parseInt(message.status, 10);
                var sessionId = String(message.sessionId);
                if (status === 0x80) { // 删除会话
                    $('[data-session-id=' + sessionId + ']').remove();
                    var index = cache.sessionMaps[sessionId];
                    if (typeof index !== 'undefined') { // 删除 cache 数据
                        _updateSessions(cache.sessions[index], 4);
                    }
                } else if (status === 0) { // 新增会话: 通过接口查询 session 对象，将 session 对象推送到回话列表顶端
                    unshiftSessionByQueryAPI(sessionId);
                }
            }
        });

        // 消息已读推送：HR发送的消息C端用户已读
        notifyClient.bind('IM_B_MESSAGE_READ', function (event, message) {

            message = _string2JSON(message);
            if (message && parseInt(message.status, 10) === 1) { // 已读
                _markMessageReaded(message);
            }
        });

        $.ajax('/im/chat/countUnReadMessages.json'); // 推送未读消息数量，推送 IM_UNREAD_MESSAGE_NUM 消息
    });


    // 初始化左侧沟通列表, 仅执行一次
    // 左侧沟通列表的展现不依赖于 push server 的连接
    $.get('/im/session/list.json', {
        pageNo: cache.sessionsMore.pageNo,
        pageSize: cache.sessionsMore.pageSize
    }, function (resp) {
        var state = parseInt(resp.state, 10);
        if (state === 1) { // 请求成功
            var sessions = resp.content.rows || [];
            _updateSessions(sessions, 1, resp.content.data.remainConversationTimes);
            cache.sessionListReady = true;

            if (sessions.length === cache.sessionsMore.pageSize) { // 鼠标向下滚动加载更多回话
                cache.sessionsMore.pageNo += 1;
                cache.sessionsMore.locked = false;
            }
        }
    }, 'json');


    // ------------------------------------------- 会话相关 开始-------------------------------------------

    /**
     * 1) 更新 Cache
     * 包括 sessions, sessionMaps, messages
     *
     * 2) 触发 IM_FE_SESSION_UPDATE 事件更新会话列表
     *
     * @param sessions      需更新的会话数据
     * @param type          更新类型
     * @param remainTimes   剩余沟通次数
     */
    function _updateSessions(sessions, type, remainTimes) {
        sessions = sessions instanceof Array ? sessions : [sessions];

        if (type === 1) {        // 替换 cache.sessions 中的会话列表
            cache.sessions = sessions;
        } else if (type === 2) { // 向 cache.sessions 尾部添加新会话数据
            _push.apply(cache.sessions, sessions.filter(function (session) { // 去重
                return typeof cache.sessionMaps[String(session.sessionId)] === 'undefined';
            }));
        } else if (type === 3) { // 向 cache.sessions 头部添加新会话数据
            _unshift.apply(cache.sessions, sessions.filter(function (session) { // 去重
                return typeof cache.sessionMaps[String(session.sessionId)] === 'undefined';
            }));
        } else if (type === 4) { // 删除 cache.sessions 中指定 sessionId 的数据
            for (var i = sessions.length - 1; i >= 0; i--) {
                var sessionId = String(sessions[i].sessionId);
                var index = cache.sessionMaps[sessionId];
                if (typeof index !== 'undefined' && index > -1) {
                    cache.sessions.splice(index, 1); // 删除 session 对象
                }
                for (var id in cache.sessionMaps) {
                    if (cache.sessionMaps[id] > cache.sessionMaps[sessionId]) {
                        cache.sessionMaps[id]--;
                    }
                }//更新session位置信息
                delete cache.sessionMaps[sessionId]; // 删除 session 位置信息
                delete cache.messages[sessionId];    // 删除 session 对应的消息
            }
        }

        if (type !== 4) { // 更新 cache.sessionMaps 位置信息
            _updateCacheSessionMpas();
        }

        // 更新回话列表前段展现
        if (typeof remainTimes !== 'undefined') {
            notifyClient.trigger('IM_FE_SESSION_UPDATE', {remainTimes: remainTimes});
        } else {
            notifyClient.trigger('IM_FE_SESSION_UPDATE');
        }
    }

    /**
     * 将指定ID的 session 推到顶部
     *
     * @param sessionId
     */
    function unshiftSessionById(sessionId) {
        var index = cache.sessionMaps[String(sessionId)];
        var session = cache.sessions[index];
        if (session) {
            cache.sessions.splice(index, 1);
            cache.sessions.unshift(session);
            _updateCacheSessionMpas();
        }
    }

    /**
     * 更新 cache.sessionMaps 位置信息
     */
    function _updateCacheSessionMpas() {
        cache.sessionMaps = {};
        for (var i = cache.sessions.length - 1; i >= 0; i--) {
            var session = cache.sessions[i];
            cache.sessionMaps[String(session.sessionId)] = i;
        }
    }

    /**
     * 判断 session 是否渲染到会话列表
     *
     * @param message
     */
    function _checkSessionExisted(message) {
        var sessionId = String(message.sessionId);

        if (typeof cache.sessionMaps[sessionId] !== 'undefined') { // 消息对应的会话已加载
            return true;
        }

        notifyClient.trigger('IM_SESSION_UPDATE', [JSON.stringify({
            sessionId: sessionId, // 会话ID
            status: 0 // 状态码: 添加会话
        })]); // 将 sessionId 对应的会话加载添加到会话列表
    }

    /**
     * 新建会话，触发 IM_SESSION_UPDATE 事件
     *
     * @param sessionId
     * @param {object} data 接口所需要的参数
     * @param callback
     */
    function createNewSession(sessionId, data, callback) {
        if (typeof cache.sessionMaps[String(sessionId)] !== 'undefined') { // 会话已加载
            typeof callback === 'function' && callback({
                content: {
                    data: {
                        sessionId: sessionId
                    },
                    rows: []
                },
                message: '\u4f1a\u8bdd\u5df2\u5b58\u5728', // 会话已存在
                state: 4001 // 会话已存在应该与创建成功用一样的状态码1，注意不要与后端给的状态码重复产生歧义
            });

            return true;
        }

        $.post('/im/session/create/' + sessionId + '.json', data, function (resp) {
            typeof callback === 'function' && callback(resp);
        }, 'json').fail(function (error) {
            alert('网络异常，请稍后重试');
        });
    }

    /**
     * 关闭会话
     *
     * @param sessionId
     * @param callback
     */
    function deleteSession(sessionId, callback) {
        sessionId = String(sessionId);

        $.post('/im/session/delete/' + sessionId + '.json', function (resp) {
            if (parseInt(resp.state, 10) === 1) {
                var index = cache.sessionMaps[sessionId];
                if (typeof index !== 'undefined' && index > -1) { // 删除本地缓存的 sessionId 对应的消息
                    var session = cache.sessions[index];
                    _updateSessions(session, 4);
                }
            }

            typeof callback === 'function' && callback(resp);
        }, 'json');
    }

    /**
     * 根据 sessionId 查询 cache.sessions 中的 session
     * @param sessionId
     */
    function getSessionById(sessionId) {
        var index = cache.sessionMaps[String(sessionId)];
        return cache.sessions[index] || {};
    }

    /**
     * 通过 sessionId 查询 API 接口获得 session 对象
     * 同时将 session 添加到会话列表顶部
     *
     * @param sessionId
     * @param callback
     */
    function unshiftSessionByQueryAPI(sessionId, callback) {
        $.post('/im/session/get/' + sessionId + '.json', function (resp) {
            if (parseInt(resp.state) === 1) { // 获取 session 成功
                var session = resp.content.data.session;
                session.sessionId = String(sessionId); // 统一 sessionId 数据类型: {string}
                session.attachment = _string2JSON(session.attachment);
                _updateSessions(session, 3); // 新增 cache 数据并触发 IM_FE_SESSION_UPDATE 事件
            }

            typeof callback === 'function' && callback(resp);
        }, 'json');
    }

    /**
     * 获取 session 中的 positionId
     * @param session
     */
    function _getPositionId(session) {
        return (session && session.attachment && session.attachment.positionId) || '';
    }

    /**
     * 鼠标滚动到底部，自动加载 session 列表
     */
    function loadMoreSessions() {
        if (cache.sessionsMore.locked) { // 滚动加载更多被锁定
            return false;
        }

        cache.sessionsMore.locked = true; // 锁定滚动加载更多

        $.get('/im/session/list.json', {
            pageNo: cache.sessionsMore.pageNo,
            pageSize: cache.sessionsMore.pageSize
        }, function (resp) {
            var state = parseInt(resp.state, 10);
            if (state === 1) { // 请求成功
                var sessions = resp.content.rows || [];
                _updateSessions(sessions, 2);

                if (sessions.length === cache.sessionsMore.pageSize) { // 可继续加载更多
                    cache.sessionsMore.pageNo += 1;
                    cache.sessionsMore.locked = false; // 解锁滚动加载更多
                }
            }
        }, 'json');
    }

    /**
     * 用户名称展现策略
     * @param session   沟通会话
     * @param both      同时显示：真实名称（昵称）
     * @return {string}
     */
    function getUserNameBySession(session, both) {
        var nickName = session.attachment.nickName || ''; // 用户昵称
        var realName = session.attachment.realName || ''; // 真实名称

        if (nickName.length === 0) { // 若用户昵称为空，展示真实姓名
            return realName;
        }

        if (session.attachment.resumeStage && nickName !== realName) { // 用户已投递
            return both ? realName + '(' + nickName + ')' : nickName;
        }

        return nickName;
    }

    // ------------------------------------------- 会话相关 结束-------------------------------------------


    // ------------------------------------------- 消息相关 开始-------------------------------------------

    /**
     * 判断消息类型：自拉勾GoGo消息
     *
     * @param message
     * @return {boolean}
     */
    function isLagouGoGoMessage(message) {
        var session = getSessionById(message.sessionId);
        return session && ( parseInt(session.sessionType, 10) === 2 );
    }

    /**
     * 判断消息类型：C端用户消息
     *
     * @param message
     * @return {boolean}
     */
    function isClientUserMessage(message) {
        return String(message.sessionId) === String(message.senderId);
    }

    /**
     * 判断消息类型：B端HR消息
     *
     * @param message
     * @return {boolean}
     */
    function isCompanyHRMessage(message) { // 记得排除系统消息
        return !( isClientUserMessage(message) || isLagouGoGoMessage(message) || parseInt(message.msgType, 10) === 0x100 );
    }

    /**
     * 标记消息已读：C端消息HR已读
     * @param message
     * @param callback
     */
    function markRead(message, callback) {
        var sessionId = String(message.sessionId);

        $.post('/im/chat/mark_read/' + sessionId + '.json', {
            msgId: message.msgId
        }, function (resp) {
            if (parseInt(resp.state, 10) === 1) {
                var session = getSessionById(sessionId);
                session.unreadCount = 0; // 重置未读消息计数
                typeof callback === 'function' && callback();
            } else {
                console.warn('\u005b\u6807\u8bb0\u6d88\u606f\u5df2\u8bfb\u005d\u64cd\u4f5c\u5931\u8d25'); // 标记失败
            }
        }, 'json');
    }

    /**
     * 分页获取历史消息
     *
     * @param sessionId  会话ID
     * @param maxMsgId   最近的一条消息的ID
     * @param pageSize   单页查询记录数，最大50
     * @param callback   成功回调
     */
    function fetchHistoryMessagesPage(sessionId, maxMsgId, pageSize, callback) {
        var messages = getMessagesBySessionId(sessionId);
        if (messages.length > 0) {
            maxMsgId = messages[0].msgId; // 当前已加载的消息列表中，最老的一条消息，即：msgId 最小
        }

        $.post('/im/chat/fetch_history_messages_page.json', {
            sessionId: sessionId,
            maxMsgId: maxMsgId,
            pageSize: pageSize || 50
        }, function (resp) {
            if (parseInt(resp.state, 10) === 1) {
                var messages = resp.content.rows || [];
                _processMessage(messages, true); // 处理历史消息

                typeof callback === 'function' && callback(messages);
            }
        }, 'json').fail(function (error) {
            console.error(error);
        });
    }

    /**
     * 更新 cache.messages
     *
     * @param sessionId        会话ID
     * @param messages         需更新的消息数据
     */
    function _updateMessagesCache(sessionId, messages) {
        sessionId = String(sessionId);
        messages = messages instanceof Array ? messages : [messages];

        var cMessages = cache.messages[sessionId] || [];
        _unshift.apply(cMessages, messages); // 将消息插入到 cache.messages
        cMessages.sort(function (a, b) { // messages 排序，历史消息在数组前面，新消息在数组后面
            var aMsgId = String(a.msgId);
            var bMsgId = String(b.msgId);

            if (aMsgId.length > bMsgId.length) {
                return 1;
            } else if (aMsgId.length < bMsgId.length) {
                return -1;
            } else {
                return aMsgId > bMsgId ? 1 : -1;
            }
        });
        cache.messages[sessionId] = cMessages;

        var session = getSessionById(sessionId); // 更新会话最新消息
        session.lastMsg = cMessages[cMessages.length - 1];
    }

    /**
     * 删除 cache.messages 中web端发送的临时消息
     *
     * @param sessionId        会话ID
     * @param tmpMsgId         新消息临时ID
     */
    function _removeMessage(sessionId, tmpMsgId) {
        var messages = getMessagesBySessionId(sessionId);
        for (var i = messages.length - 1; i >= 0; i--) {
            var message = messages[i];
            if (String(message.msgId) === String(tmpMsgId)) {
                messages.splice(i, 1);
                break;
            }
        }
    }

    /**
     * 发送消息
     * @param sessionId  会话ID
     * @param content    消息内容
     * @param tmpMsgId   消息临时 msgId
     * @param callback   请求回调
     */
    function sendMessage(sessionId, content, tmpMsgId, callback) {
        var session = getSessionById(sessionId);
        var positionId = _getPositionId(session); // 会话的职位Id
        $.post('/im/chat/send/' + sessionId + '.json', {
            content: content,
            attach: tmpMsgId, // 前端上送的原样返回，消息临时 msgId
            lagouPositionId: positionId
        }, function (resp) {
            if (parseInt(resp.state, 10) === 1) {
                _removeMessage(sessionId, tmpMsgId); // 删除临时消息
                var message = resp.content.data.message;
                _updateMessagesCache(message.sessionId, [message]); // 插入真实消息
            }
            typeof callback === 'function' && callback(resp);
        }, 'json');
    }

    /**
     * 根据 sessionId 获取对话列表
     *
     * @param sessionId
     * @returns {Array}
     */
    function getMessagesBySessionId(sessionId) {
        return cache.messages[String(sessionId)] || [];
    }

    /**
     * 获取最新接收到的消息（针对所有会话）
     *
     * @return {Object}
     */
    function getLatestReceiveMsg() {
        return cache.latestReceiveMsg;
    }

    /**
     * 标记B端消息已读状态：HR发送的消息已被C端用户查看
     *
     * @param message
     */
    function _markMessageReaded(message) {

        var sessionId = String(message.sessionId);
        var session = getSessionById(sessionId);

        var cMessages = getMessagesBySessionId(sessionId) || [];
        var needUpdate = false; // 更新消息
        var msgId = String(message.msgId);

        for (var i = cMessages.length - 1; i >= 0; i--) {
            var cMessage = cMessages[i];
            var cMsgId = String(cMessage.msgId);

            if (cMessage.isRead || !isCompanyHRMessage(cMessage)) { // 只针对HR发出的未读消息
                continue;
            }

            if (cMsgId === msgId
                || msgId.length > cMsgId.length
                || ( msgId.length === cMsgId.length && msgId > cMsgId )
            ) {
                needUpdate = true;
                cMessage.isRead = true;
            }
        }

        if (needUpdate) {
            notifyClient.trigger('IM_FE_MESSAGE_UPDATE', {sessionId: sessionId, isHistoryMsgs: false});

            // 为了更新左侧sessionlist的已读未读状态，更新session.rivalReadMsgId为该推送消息的msgId
            session.rivalReadMsgId = msgId;
            notifyClient.trigger('IM_FE_SESSION_UPDATE');
        }


    }

    /**
     * 消息汇总处理
     * @param messages     消息列表
     * @isHistoryMsgs      是否为历史消息数据
     */
    function _processMessage(messages, isHistoryMsgs) {
        messages = messages || [];

        for (var i = 0, length = messages.length; i < length; i++) {
            var message = messages[i];
            var type = parseInt(message.msgType, 10);
            var sessionId = String(message.sessionId);

            if (isCompanyHRMessage(message)) { // 标记HR消息[已读]状态
                var msgId = String(message.msgId);
                var session = getSessionById(sessionId);
                var rivalReadMsgId = String((session && session.rivalReadMsgId) || '');
                if (rivalReadMsgId === msgId
                    || rivalReadMsgId.length > msgId.length
                    || ( rivalReadMsgId.length === msgId.length && rivalReadMsgId > msgId )) {
                    message.isRead = true;
                } else {
                    message.isRead = false;
                }
            }

            /**
             * type = 0 => 文本消息
             * type = 1 => 图文混合消息
             * type = 2 => 图片消息
             * type = 3 => 语音消息
             *
             * type = 0x100     => 系统消息(文本)
             *
             * type = 0xFFFF+1  => 邀约捎句话
             * type = 0xFFFF+2  => 邀约
             * type = 0xFFFF+3  => 简历状态通知
             * type = 0xFFFF+4  => 面试邀请
             * type = 0xFFFF+5  => 一拍顾问消息
             */
            if (type !== 0 && type !== 0x100) { // 非文本消息，转成对应JSON对象
                message.msgContent = _string2JSON(message.msgContent);
            }

            if (!isHistoryMsgs) { // 如果是历史消息，session 一定存在
                _checkSessionExisted(message);

                if (isClientUserMessage(message)) {
                    cache.latestReceiveMsg = message; // 记录最新一条接收到的消息
                }
            }
        }

        if (messages.length > 0) { // 更新消息列表
            _updateMessagesCache(sessionId, messages);
            notifyClient.trigger('IM_FE_MESSAGE_UPDATE', {sessionId: sessionId, isHistoryMsgs: isHistoryMsgs});

            if (!isHistoryMsgs) { // 如果不是历史消息，更新回话列表，显示最新消息
                notifyClient.trigger('IM_FE_SESSION_UPDATE');
            }
        }
    }

    // ------------------------------------------- 消息相关 结束-------------------------------------------


    // ------------------------------------------- 其他 开始----------------------------------------------

    /**
     * B端开启沟通功能
     */
    function openCommunicateStatus(callback) {
        $.get('/im/chat/status/open.json', function (resp) {
            typeof callback === 'function' && callback(resp);
        }, 'json');
    }

    /**
     * 获取B端用户信息
     * {
     *       content: {
     *           data: {
     *               allPositionCount: 72,
     *               onlinePositionCount: 14,
     *               companyShortName: "智涂",
     *               userId: 5877422,
     *               userName: "airtake.",
     *               companyId: 343125,
     *               companyName: "智涂科技有限公司",
     *               portrait: "i/image/M00/02/92/CgqKkVaUmkeAX2C2AAAb-vBujmE022.jpg",
     *               hasLagouCompany: true
     *           },
     *           rows: [ ]
     *       },
     *       message: "操作成功",
     *       state: 1
     *   }
     */
    function getBUserInfo(callback, errorCallback) {
        if (cache.BUserInfo && cache.BUserInfo.userId) {
            typeof callback === 'function' && callback(cache.BUserInfo);
            return;
        }

        $.get('/im/chat/getUserInfo.json', function (resp) {
            var state = parseInt(resp.state, 10);
            if (state === 1) {
                cache.BUserInfo = resp.content.data;
                typeof callback === 'function' && callback(cache.BUserInfo);
            } else {
                typeof errorCallback === 'function' && errorCallback(state);
            }
        }, 'json');
    }

    /**
     * 格式化输出时间
     *
     * @return {string}
     */
    function formatTime(time, format) {
        var t = new Date(parseInt(time, 10));
        var tf = function (i) {
            return (i < 10 ? '0' : '') + i
        };
        return format.replace(/y{2,4}|MM|dd|HH|mm|ss/g, function (a) {
            switch (a) {
                case 'yyyy':
                    return t.getFullYear();
                    break;
                case 'yy':
                    return String(t.getFullYear()).slice(2);
                    break;
                case 'MM':
                    return tf(t.getMonth() + 1);
                    break;
                case 'mm':
                    return tf(t.getMinutes());
                    break;
                case 'dd':
                    return tf(t.getDate());
                    break;
                case 'HH':
                    return tf(t.getHours());
                    break;
                case 'ss':
                    return tf(t.getSeconds());
                    break;
            }
        })
    }

    /**
     * 有中文截取后两位
     * 英文截取前两位
     * 如果有中文+英文+中文，截取最后一个中文
     *
     * @param name
     * @return {string}
     */
    // function splitName (name) {
    //     if ( !name ) {
    //         return '';
    //     }

    //     name = String(name);
    //     var chinesePart = '';

    //     var matches = name.match(/[\u4E00-\u9FA5\uF900-\uFA2D]+/g);
    //     if ( matches ) {
    //         chinesePart = matches[matches.length - 1];
    //     }

    //     if ( chinesePart.length > 0 ) {
    //         return chinesePart.substr(-2);
    //     } else {
    //         return name.substr(0, 2);
    //     }
    // }
    // len用于处理汉字图像时控制截取的个数，默认为2
    function splitName(name, len) {
        var len = len || 2;
        if (!name) return '';
        var reg = /[\u4E00-\u9FA5\uF900-\uFA2D]+/g;
        name = name + '';
        var rs = name.match(reg);
        if (rs && rs.length > 0) {
            var result = rs[rs.length - 1];
            return result.substr(((result.length - len) < 0 ? 0 : (result.length - len)), len || 2);
        } else {
            return name.substr(0, 2);
        }
    }

    /**
     * 字符串解析为JSON对象
     *
     * @param str
     * @return {object}
     */
    function _string2JSON(str) {
        try {
            var obj = JSON.parse(str);
        } catch (e) {
            console.warn("Can't parse '" + str + "' to JSON");
        }

        return _isObject(obj) ? obj : null;
    }

    /**
     * 判断参数为 object 类型
     *
     * @param obj
     * @return {boolean}
     */
    function _isObject(obj) {
        return ['[object Array]', '[object Object]'].indexOf(_toString.call(obj)) > -1;
    }

    // ------------------------------------------- 其他 结束----------------------------------------------


    module.exports = {
        openCommunicateStatus: openCommunicateStatus,
        createNewSession: createNewSession,
        deleteSession: deleteSession,
        bind: notifyClient.bind,
        unbind: notifyClient.unbind,
        formatTime: formatTime,
        sendMessage: sendMessage,
        fetchHistoryMessagesPage: fetchHistoryMessagesPage,
        getMessagesBySessionId: getMessagesBySessionId,
        markRead: markRead,
        splitName: splitName,
        getBUserInfo: getBUserInfo,
        getUserId: function () {
            return (window.CONST_VARS && CONST_VARS('user') && CONST_VARS('user')['id']) || '';
        },
        getUserName: function () {
            return (window.CONST_VARS && CONST_VARS('user') && CONST_VARS('user')['name']) || '';
        },
        getPortrait: function () {
            var url = (window.CONST_VARS && CONST_VARS('user') && CONST_VARS('user')['portrait']) || '';
            if (url != '') {
                return /^(https?\:\/\/|\/)/i.test(url) ? url : ('https://www.lgstatic.com/thumbnail_50x50/yun/' + url); // 处理 fast_dfs 图片相对路径 url
            } else {
                return '';
            }
        },
        getCUserName: function (sessionId) {
            var session = null;

            if (_isObject(sessionId)) { // sessionId 参数为会话对象
                session = sessionId;
            } else { // sessionId 参数为会话ID
                session = getSessionById(sessionId);
            }

            return (session && session.attachment && session.attachment.nickName) || '';
        },
        getCUserPortrait: function (sessionId) {
            var session = null;

            if (_isObject(sessionId)) { // sessionId 参数为会话对象
                session = sessionId;
            } else { // sessionId 参数为会话ID
                session = getSessionById(sessionId);
            }

            return (session && session.attachment && session.attachment.portrait) || '';
        },
        getCUserPositionId: function (sessionId) {
            var session = null;

            if (_isObject(sessionId)) { // sessionId 参数为会话对象
                session = sessionId;
            } else { // sessionId 参数为会话ID
                session = getSessionById(sessionId);
            }

            return (session && session.attachment && session.attachment.positionId) || '';
        },
        getCUserPositionName: function (sessionId) {
            var session = null;

            if (_isObject(sessionId)) { // sessionId 参数为会话对象
                session = sessionId;
            } else { // sessionId 参数为会话ID
                session = getSessionById(sessionId);
            }

            return (session && session.attachment && session.attachment.positionName) || '';
        },
        getCUserLastPositionName: function (sessionId) {
            var session = null;

            if (_isObject(sessionId)) { // sessionId 参数为会话对象
                session = sessionId;
            } else { // sessionId 参数为会话ID
                session = getSessionById(sessionId);
            }

            return (session && session.attachment && session.attachment.lastPositionName) || '';
        },
        queryConnectStatus: function () {
            return !!cache.push.status;
        },
        getLatestReceiveMsg: getLatestReceiveMsg,
        isLagouGoGoMessage: isLagouGoGoMessage,
        isClientUserMessage: isClientUserMessage,
        isCompanyHRMessage: isCompanyHRMessage,
        getAllSessions: function () {
            return cache.sessions || [];
        },
        getAllSessionMaps: function () {
            return cache.sessionMaps || {};
        },
        unshiftSessionById: unshiftSessionById,
        getSessionById: getSessionById,
        loadMoreSessions: loadMoreSessions,
        getUserNameBySession: getUserNameBySession,
        unshiftSessionByQueryAPI: unshiftSessionByQueryAPI
    };
});


/*!common/widgets/position-filter/main.js*/
;/**
 * @author: julianzeng@lagou.com
 * @data 2017/06/09
 */


/*
 ** @require "common/widgets/position-filter/main.less"
 */
define('common/widgets/position-filter/main', ['require', 'exports', 'module', 'common/components/jquery-niceScroll/jquery.nicescroll.min'], function (require, exports, module) {
    require('common/components/jquery-niceScroll/jquery.nicescroll.min');
    var $slotEle;
    var $body = $('body');
    var filterType = '';
    var filterStartingHtml = '<div class="position-list-filter-wrapper">'
        + '<div class="inputter">'
        + '<i class="icon-middle-search"></i>'
        + '<input type="text" class="filter-input" placeholder="搜索职位">'
        + '</div>'
        + '<div class="list-wrapper">'
        + '<ul class="position-list">';
    var filterEndingHtml = '</ul>'
        + '</div>'
        + '</div>';
    var cache = {
        selectedPositionId: undefined,    // 用于标示已选的职位
        sessionPositionId: undefined      // 存当前职位的positionId用于标示（当前职位）
    };
    /**
     * 职位选择器导出的自定义事件事集对象
     * @type {Object}
     */
    var positionFilterEvents = {
        selectPosSucc: 'selectPosition',    //触发了选择职位
        clearCache: 'clearFilterCache', //清空职位选择器缓存
        P_F_inited: 'positionFilterInited' //职位选择器初始化完成
    };
    var positionFilter = {
        simple: {
            totalPosition: [], //保存原始所有职位的接口
            renderFilter: function (positionSelectorVO, slotDomSelector) {
                //在接口请求成功后调用
                var pos_select_VO = positionSelectorVO;
                // 如果传进selectedPositionId表示需要默认选中的职位的id
                var selectedPosId = pos_select_VO.selectedPositionId;
                cache.sessionPositionId = pos_select_VO.sessionPositionId; //用于标示“（当前职位）”
                $slotEle = _getSlotEle(slotDomSelector);
                var positionArr = _getAllPositionArrFromAPI(pos_select_VO);
                var filterMiddleHtml = '';
                var html = '';
                filterMiddleHtml = _getLisHtmlFromPositionArr(positionArr);
                html = filterStartingHtml + filterMiddleHtml + filterEndingHtml;
                $slotEle.html(html);
                setTimeout(_scrollNicer, 0);//好像是动态插入之后获取到.position-list然后执行.niceScroll()会有点问题，不能立即执行。

                $slotEle.trigger(positionFilterEvents.P_F_inited);
                this.totalPosition = positionArr;  // 缓存数据用于筛选
                // 监听弹窗关闭时触发的清除已选的职位的事件，不应该用on绑定，否则没打开n次就会绑定n次，最后相当于绑定了n个事件处理函数
                $slotEle.one(positionFilterEvents.clearCache, _clearCache);
                if (selectedPosId) {
                    var $selectedPos = $slotEle.find('.position-item[data-id="' + selectedPosId + '"]');
                    if ($selectedPos.length > 0) {
                        $selectedPos.trigger('click');
                    }

                }
            },
            filterPosition: function (keyword) {
                var $listWrapper = $('.position-list-filter-wrapper .list-wrapper');
                var lisHtml = _getLisHtmlFromPositionArr(this.totalPosition, keyword);
                if (lisHtml === '') {
                    $listWrapper.html('<div class="search-no-result"><i class="icon-position-2"></i><p>还没找到<span class="keyword green">' + keyword + '</span>相关职位&emsp;<span class="remove-keyword green">清空搜索</span></p></div>');
                    return;
                }
                $listWrapper.html('<ul class="position-list">' + lisHtml + '</ul>');
                setTimeout(_scrollNicer, 0);

            }
        },
        complex: {
            pos_select_VO: {},
            renderFilter: function (positionSelectorVO, slotDomSelector) {
                var pos_select_VO = positionSelectorVO;
                var selectedPosId = pos_select_VO.selectedPositionId;
                cache.sessionPositionId = pos_select_VO.sessionPositionId;
                var html = '';
                var filterMiddleHtml = _getLisLevel1HtmlFromTypeList(pos_select_VO.typeList);
                html = filterStartingHtml + filterMiddleHtml + filterEndingHtml;
                $slotEle = _getSlotEle(slotDomSelector);
                $slotEle.html(html);
                setTimeout(_scrollNicer, 0);
                $slotEle.trigger(positionFilterEvents.P_F_inited);
                this.pos_select_VO = pos_select_VO; // 缓存数据用于筛选
                // 监听弹窗关闭时触发的清除已选的职位的事件
                $slotEle.one(positionFilterEvents.clearCache, _clearCache);
                if (selectedPosId) {
                    var $selectedPos = $slotEle.find('.position-item[data-id="' + selectedPosId + '"]');
                    if ($selectedPos.length > 0) {
                        $selectedPos.trigger('click');
                    }

                }
            },
            filterPosition: function (keyword) {
                var $listWrapper = $('.position-list-filter-wrapper .list-wrapper');
                var lisHtml = _getLisLevel1HtmlFromTypeList(this.pos_select_VO.typeList, keyword);
                if (lisHtml.indexOf('position-item') === -1) { //这种判断比较脆弱，可以改改
                    $listWrapper.html('<div class="search-no-result"><i class="icon-position-2"></i><p>还没找到<span class="keyword green">' + keyword + '</span>相关职位&emsp;<span class="remove-keyword green">清空搜索</span></p></div>');
                    return;
                }
                $listWrapper.html('<ul class="position-list">' + lisHtml + '</ul>');
                var $selectedPos = $listWrapper.find('.position-item.selected');
                if (keyword === '' && $selectedPos.length > 0) {
                    // 有筛选关键词时，默认二级列表是展开的，清空关键词时应该收拢，如果有选中的职位才展开对应的
                    $selectedPos.trigger('click');
                }
                setTimeout(_scrollNicer, 0);
            }
        },
        empty: {
            renderFilter: function (positionSelectorVO, slotDomSelector) {
                var pos_select_VO = positionSelectorVO;
                $slotEle = _getSlotEle(slotDomSelector);
                $slotEle.html('<div class="position-list-filter-wrapper"><div class="no-position"><i class="icon-position-2"></i><p>你没有任何职位&emsp;<a href="' + window.GLOBAL_DOMAIN.ectx + '/parentposition/createPosition.htm" class="green" target="_blank" data-lg-tj-id="19f9" data-lg-tj-no="idnull" data-lg-tj-cid="' + (window.CONST_VARS('user').id ? window.CONST_VARS('user').id : 'idnull') + '">去发布职位</a></p></div></div>');
                $slotEle.trigger(positionFilterEvents.P_F_inited);
            },
            filterPosition: function (keyword) {
                console.error("没有职位时不应该触发筛选");
            }
        }
    };


    // 这些事件绑定还的确得代理在body上，如果绑在$slotEle上，每次初始化都得绑定，特别是在弹窗场景更不适合了
    //点击一级列表的职位类别
    $body.on('click', '.position-list-filter-wrapper .position-list .li-header', function (e) {
        var $this = $(this);
        // var $closestL2Ul = $this.siblings('.position-list-level2');
        if ($this.hasClass('active')) {
            $this.removeClass('active');
        } else {
            $this.addClass('active');
        }
    })
    // 点击选择职位
    $body.on('click', '.position-list-filter-wrapper .position-item', function (e) {
        var $this = $(this);
        var id = parseInt($this.attr('data-id'));
        var name = $this.attr('data-positionname');
        var $ulPositionListLevel2 = $this.parents('ul.position-list-level2');
        if ($ulPositionListLevel2.length > 0 && $ulPositionListLevel2.is(':hidden')) {
            // 如果是二级列表下的，且列表没展开，应对预选中的职位是二级列表下的情况，这个判断要放在最前面
            $ulPositionListLevel2.siblings('.li-header').trigger('click');
        }
        if ($this.find('.visit-position').is(e.target)) return; // 点击的是查看职位
        if ($this.hasClass('isOffCur') || $this.hasClass('isOff')) return; // 点击的是已下线职位
        $slotEle.trigger(positionFilterEvents.selectPosSucc, {selectedPositionId: id, selectedPositionName: name}); // 代表成功选择了有效职位
        if ($this.hasClass('selected')) return; // 需要在selectPosSucc事件之后
        $('.position-item.selected').removeClass('selected');
        $this.addClass('selected');
        cache.selectedPositionId = id; //缓存选择的职位，等点击确认的时候再用于发请求

    })
    // 点击清空搜索
    $body.on('click', '.position-list-filter-wrapper .search-no-result .remove-keyword', function (e) {
        $slotEle.find('.inputter input').val('').trigger('keyup');
    })
    var delayConfig = {
        delayTime: 200, // 延时，该时间间隔内用户没有输入内容时才进行筛选，减少DOM渲染次数
        lastCompositionTime: 0 // 记录最近的一次输入文本时间的时间戳
    };
    // 监听筛选框
    // keyup事件中文输入时，最后会有一次enter键或者空格键的keyup事件，该keyup事件在compositionend事件之后//后来观测的不是酱紫的啊
    $body.on('keyup', '.position-list-filter-wrapper .inputter input', function (e) {
        var $this = $(this);
        var keyword = $this.val().trim();
        // console.log(e.type + ': '+$this.attr('data-compositionstart'));
        if ($this.attr('data-compositionstart') === 'true') return; //中文输入没结束时不处理
        delayConfig.lastCompositionTime = e.timeStamp;
        setTimeout(function () {
            if (delayConfig.lastCompositionTime - e.timeStamp === 0) {
                positionFilter[filterType].filterPosition(keyword);
            }
        }, delayConfig.delayTime);
    }).on('compositionstart', '.position-list-filter-wrapper .inputter input', function (e) {
        $(this).attr('data-compositionstart', 'true');
        // console.log(e.type + ': '+$(this).attr('data-compositionstart'));

    }).on('compositionend', '.position-list-filter-wrapper .inputter input', function (e) {
        $(this).attr('data-compositionstart', 'false');
        // console.log(e.type + ': '+$(this).attr('data-compositionstart'));
    })

    /**
     * 职位数量不大于20的时候是没有一二级分类，只用处理一维数组，该方法将接口给的复杂数组处理成一维数组
     * @param  {object} pos_select_VO [description]
     * @param  {array} pos_select_VO.typeList 该数组的每个元素为一种职位类别
     * @param  {string} pos_select_VO.typeList[i].name 职位类别名
     * @param  {array} pos_select_VO.typeList[i].positionList 该职位类别下的所有职位
     * @return {array}  包含职位元素的一维数组
     */
    function _getAllPositionArrFromAPI(pos_select_VO) {
        var positionList = [];
        var typeList = pos_select_VO.typeList;
        var typeListLength = typeList.length;
        var positionListI = [];
        var positionListILength = 0;
        for (var i = 0; i < typeListLength; i++) {
            positionListI = typeList[i].positionList;
            positionListILength = positionListI.length;
            for (var j = 0; j < positionListILength; j++) {
                positionList.push(positionListI[j]);
            }
        }
        return positionList;
    }

    /**
     * 根据职位数组positionList的一个元素获得其html
     * @param  {object} item    positionList[i]
     * @param  {number} item.id    职位id   接口给的数据包含positionId和outerPositionId，这里应该使用positionId
     * @param  {string} item.status   职位状态 status: 1(在线职位)， 2（已下线职位）
     * @param  {string} item.name   职位名称
     * @param  {string} keyword   非必选参数，当有的时候表示是在根据关键词筛选职位
     * @return {string}   单个职位元素的html字符串
     */
    function _getLiHtmlFromPositionItem(item, keyword) {
        var id = parseInt(item.id, 10);
        var reg;
        var isOfflined = (parseInt(item.status, 10) === 2) ? true : false;
        var isCurrentPosition = id === cache.sessionPositionId ? true : false;
        var selectedClass = cache.selectedPositionId === id ? ' selected' : '';
        var stateTipsStr = '';
        var maxNameWidthStyle = '';
        var stateClass = '';
        if (isOfflined && isCurrentPosition) {
            stateTipsStr = '<span class="stateTips">(当前职位，已下线)</span>';
            stateClass = ' hasTips isOffCur';
        } else if (isOfflined) {
            stateTipsStr = '<span class="stateTips">(已下线)</span>';
            stateClass = ' hasTips isOff';
        } else if (isCurrentPosition) {
            stateTipsStr = '<span class="stateTips">(当前职位)</span>';
            stateClass = ' hasTips isCur';
        }
        if (typeof keyword === 'undefined') {
            // 初次渲染
            return '<li class="position-item ' + stateClass + selectedClass + '" data-id="' + item.id + '" data-positionname="' + item.name + '">'
                + '<span class="position-name" title="' + item.name + '">' + item.name + '</span>'
                + stateTipsStr
                + '<a class="visit-position" '
                + 'href="' + window.GLOBAL_DOMAIN.ectx + '/position/redirectOriginalPage.htm?positionId=' + item.id + '"'
                + ' target="_blank">查看职位'
                + '</a>'
                + '</li>';
        } else {
            // 根据关键词筛选,keyword === ''表示将关键词清空了
            regex = new RegExp(keyword, "g");
            return '<li class="position-item ' + stateClass + selectedClass + '" data-id="' + item.id + '" data-positionname="' + item.name + '">'
                + '<span class="position-name" title="' + item.name + '">' + item.name.replace(regex, '<span class="green">' + keyword + '</span>') + '</span>'
                + stateTipsStr
                + '<a class="visit-position" '
                + 'href="' + window.GLOBAL_DOMAIN.ectx + '/position/redirectOriginalPage.htm?positionId=' + item.id + '"'
                + ' target="_blank">查看职位'
                + '</a>'
                + '</li>';
        }
    }

    /**
     * 由一维职位数组获得所有职位<li></li>元素的字符串,遍历然后分发给_getLiHtmlFromPositionItem处理
     * @param  {array} PositionArr    一维职位数组,包含所有的职位
     * @param  {string} keyword   非必选参数，当有的时候表示是在根据关键词筛选职位
     * @return {string}   职位元素<li></li>字符串总和
     */
    function _getLisHtmlFromPositionArr(PositionArr, keyword) {
        var str = '';
        if (keyword === '' || typeof keyword === 'undefined') {
            // 筛选词被清空或者为初次渲染时处理数组的所有元素，keyword直接分发给_getLiHtmlFromPositionItem判断
            for (var i = 0; i < PositionArr.length; i++) {
                str += _getLiHtmlFromPositionItem(PositionArr[i], keyword);
            }
        } else {
            // 筛选词不为空的时候筛选出数组中职位名包含keyword的元素再分发给_getLiHtmlFromPositionItem处理
            for (var i = 0; i < PositionArr.length; i++) {
                if (PositionArr[i].name.indexOf(keyword) > -1) {
                    str += _getLiHtmlFromPositionItem(PositionArr[i], keyword);
                }
            }
        }
        return str;
    }

    /**
     * 根据接口返回的带有职位类别信息的复杂数组获得带二级分类的html字符串，在职位数量大于20的时候才会被调用
     * @param  {array} typeList  接口返回的带有职位类别信息的复杂数组
     * @param  {string} keyword    非必选参数，当有的时候表示是在根据关键词筛选职位
     * @return {string}   带二级分类的html字符串
     */
    function _getLisLevel1HtmlFromTypeList(typeList, keyword) {
        var str = '';
        for (var i = 0; i < typeList.length; i++) {
            var positionListHtmlI = _getLisHtmlFromPositionArr(typeList[i].positionList, keyword);
            if (positionListHtmlI && positionListHtmlI !== '') {
                // （筛选结果）职位为空时positionListHtmlI为'',一级分类不应该被渲染出来
                str += '<li class="li-level1">'
                    + '<div class="li-header' + ((keyword && keyword !== '') ? ' active' : '') + '">'
                    + '<i class="icon-directory"></i>'
                    + '<span class="item-level1">' + typeList[i].name + '</span>'
                    + '</div>'
                    + '<ul class="position-list-level2">' + positionListHtmlI + '</ul>'
                    + '</li>';
            }
        }
        return str;
    }

    /**
     * jquery.niceScroll处理职位列表滚动条
     */
    function _scrollNicer() {
        $('.position-list-filter-wrapper .position-list').niceScroll({
            cursorcolor: "#C1C1C1",
            cursorwidth: "5px",
            cursorborderradius: "4px"
        });
    }

    /**
     * 获取职位筛选器的插入节点
     * @param  {selector string or jQuery Object} arg
     * @return {jQuery Object}
     */
    function _getSlotEle(arg) {
        if (typeof arg === 'string') {
            return $(arg);
        } else {
            return arg;
        }
    }

    /**
     * 清空职位筛选器缓存
     */
    function _clearCache() {
        cache = {
            selectedPositionId: undefined,
            sessionPositionId: undefined
        };
    }

    /**
     * 职位选择器组件导出的用于初始渲染的方法
     * @param {object} positionSelectorVO
     *     positionSelectorVO: {
     *         typeList: [
     *             {
     *                 name: "", // 职位类别名
     *                 positionList: [{
     *                     id: 0, // 职位id
     *                     name: "",  // 职位名
     *                     positionStatus: ""  // 职位状态
     *                 }]
     *             }
     *         ],
     *         positionCount: 0, // 职位的总数
     *         sessionPositionId: 0, // 当前职位的id
     *         selectedPositionId: 0 // 预先选中的职位id
     *     }
     * @param {string} slotDomSelector  职位筛选器的插入DOM节点标识符(selector string or jQuery Object)
     *
     */
    function renderPositionFilter(positionSelectorVO, slotDomSelector) {
        var pos_count = positionSelectorVO.positionCount;
        if (pos_count === 0 || typeof pos_count === 'undefined') {
            filterType = 'empty';  // 显示无在线职位
        } else if (pos_count > 20) {
            filterType = 'complex'; // 显示为多级列表
        } else {
            filterType = 'simple'; // 显示为一级列表
        }
        positionFilter[filterType].renderFilter(positionSelectorVO, slotDomSelector);
    }

    module.exports = {
        renderPositionFilter: renderPositionFilter,
        positionFilterEvents: positionFilterEvents

    }
})

/*!common/widgets/chat-with-Ta-pop/main.js*/
;
/**
 * @author: julianzeng@lagou.com
 * @data 2017/06/09
 *
 * 【warning: 如果弹窗中niceScroll滚动条不出现，请确认引入次模块的当前页面只引入了components下面的修复了bug的jquery-niceScroll插件，dep下的该插件有bug】
 *
 * 和ta聊聊组件说明：
 * 使用方式： 直接单独引入此js文件即可
 * 需要注意的是：
 * （1）默认和ta聊聊按钮的class类名需要有"add-chat-list", 继续聊聊的类名要有"chat-continue"，沟通次数的计数器selector为：".LG-chat-remain-times .num"
 * 如需要自定义，可以通过导出的方法initChatWithTa(options)进行配置
 *     @param {option} [object]
 *     @param {option.chatClassName}        和ta聊聊按钮的class类名
 *     @param {option.chatAgainClassName}   继续聊聊的class类名
 *     @param {option.numSeletor}           沟通次数的计数器selector
 * （2）和ta聊聊按钮需要的自定义属性有：
 *     @param data-cuserid ，必选  c端用户id
 *     @param data-selectPosId ，非必选 ，当需要职位选择器预选中职位时要有此职位的职位id
 *  (3) 继续聊聊按钮需要的自定义属性有：
 *     @param data-cuserid ，必选  c端用户id
 *  (4) 成功创建新的聊天窗口的时候触发了自定义事件，如有需要，可以监听
 *      $body.trigger('chatSuccess', {cUserId: chatWithTaCache.cUserId});
 * （5）特别需要留意的是，点击候选人卡片会有相应行为，而点击聊聊按钮的事件代理在body上，事件会先冒泡到候选人卡片上，这种现象不是期望的，所以需要在点击候选人卡片事件函数中判断event.target,避免点击聊聊按钮先触发了点击候选人卡片事件
 */


/**
 * @require "common/widgets/chat-with-Ta-pop/main.less"
 */

define('common/widgets/chat-with-Ta-pop/main', ['require', 'exports', 'module', 'common/static/js/lagou.mini', 'common/components/topTips/main', 'common/components/jquery-niceScroll/jquery.nicescroll.min', 'common/widgets/open-recruit-service-pop/main', 'chat/modules/api/chat-api', 'common/widgets/position-filter/main'], function (require, exports, module) {

    // 拉勾框架
    require('common/static/js/lagou.mini');

    require('common/components/topTips/main');
    require('common/components/jquery-niceScroll/jquery.nicescroll.min');
    var $body = $('body');
    var config = {
        chatClassName: 'add-chat-list',
        chatAgainClassName: 'chat-continue',
        numSeletor: '.LG-chat-remain-times .num'
    };
    var ChatPopInitHtml = '<div class="modal fade" id="chatWithTaPop" aria-hidden="true">'
        + '<div class="modal-dialog">'
        + '<div class="modal-content">'
        + '<div class="modal-header">'
        + '<button type="button" class="close icon-close" data-dismiss="modal"></button>'
        + '</div>'
        + '<div class="modal-body">'
        + '<div class="clearfix">'
        + '<div class="left-filter-wrap fl">'
        + '<h2>第一步：选择要沟通的职位</h2>'
        + '<div class="filter-slot"></div>'
        + '</div>'
        + '<div class="greeting-wrapper fl">'
        + '<h2>第二步：向对方打个招呼</h2>'
        + '<div class="selectTemplate">'
        + '<span class="selectedTemp">'
        + '<span class="name">模板一</span>'
        + '<i class="icon-arrow-down"></i>'
        + '</span>'
        + '<ul class="template-list"></ul>'
        + '</div>'
        + '<div class="no-greeting-tpl">无模板可用</div>'
        + '<div class="greet-words">'
        + '<textarea placeholder="输入打招呼语，提高回应率"></textarea>'
        + '<span class="number-tips">'
        + '<span class="writed-word-num">0</span>/<span class="max">200</span>'
        + '</span>'
        + '</div>'
        + '<div class="invite-or-not">'
        + '<span class="checkbox-item">'
        + '<i class="icon-checkbox"></i>&emsp;<label>顺便邀请对方投递简历</label>'
        + '</span>'
        + '</div>'
        + '</div>'
        + '</div>'
        + '<div class="handle-button-wrapper">'
        + '<span class="ok bottom-btn" data-lg-tj-id="19f8" data-lg-tj-no="idnull" data-lg-tj-cid="idnull">发送</span>'
        + '</div>'
        + '</div>'
        + '</div>'
        + '</div>'
        + '</div>';

    /**
     * 初始化弹窗
     * @param  {object} options 初始化配置选项， 非必选
     * @param  {string} options.chatClassName 和ta聊聊按钮的class类名， 非必选
     * @param  {string} options.chatAgainClassName 继续聊聊按钮的class类名， 非必选
     * @param  {string} options.numSeletor 沟通次数的计数器selector， 非必选
     */
    function initChatWithTa(options) {
        $.extend(config, options);
        if ($('#chatWithTaPop').length === 0) {
            $body.append(ChatPopInitHtml);
            setTimeout(function () {
                $('#chatWithTaPop .greet-words textarea').niceScroll({
                    cursorcolor: "#C1C1C1",
                    cursorwidth: "5px",
                    cursorborderradius: "4px"
                });
                $('#chatWithTaPop .selectTemplate .template-list').niceScroll({
                    cursorcolor: "#C1C1C1",
                    cursorwidth: "5px",
                    cursorborderradius: "4px"
                });
            }, 0)
        }

        //和ta聊聊相关按钮事件绑定
        $body.on('click', '.' + config.chatClassName, function (e) {
            e.stopPropagation();
            var $this = $(this);
            var cUserId = $this.attr('data-cuserid');
            var selectPosId = $this.attr('data-selectPosId');
            chatWithTa({
                cUserId: cUserId,
                selectPosId: selectPosId
            });
        })
        /**
         * 点击继续聊聊，隐私保护屏蔽时弹窗说明
         */
        $body.on('click', '.' + config.chatAgainClassName, function (e) {
            e.stopPropagation();
            var $this = $(this);
            var url = $this.attr('href');
            var cUserId = $this.attr('data-cuserid');
            if (cUserId) {
                $.ajax({
                    url: '/im/session/imBlocked/' + cUserId + '.json',
                    type: 'POST',
                    dataType: 'json',
                    async: false,
                    success: function (res) {
                        if (parseInt(res.state, 10) === 1 && res.content.data.imBlocked) {
                            e.preventDefault();
                            var confirm = new lg.Widgets.Controls.Confirm({
                                content: '晚来了一步，该用户已设置隐私保护，暂无法查看。',
                                submitText: '好的',
                                noCancelBtn: true,
                                SubmitBtn: function (e) {
                                    e.control.setRemove();
                                }
                            });
                        }
                    },
                    error: function (error) {
                        alert('网络错误，稍后再试'); //是这样报错好，还是直接跳转到沟通页好，毕竟这个判断并不是最终判断
                    }
                });
            } else {
                console.error('c端用户id获取不到');
            }

        });
    }

    initChatWithTa();


    /**
     * 和ta聊聊弹窗内部逻辑
     */
    var judgeOpenServiceState = require('common/widgets/open-recruit-service-pop/main').judgeOpenServiceState;
    var createNewSession = require('chat/modules/api/chat-api').createNewSession;
    var positionFilter = require('common/widgets/position-filter/main');
    var P_F_EVENT = positionFilter.positionFilterEvents;
    var $chatWithTaPop = $('#chatWithTaPop');
    var $leftTitle = $chatWithTaPop.find('.left-filter-wrap h2');
    var $rightTitle = $chatWithTaPop.find('.greeting-wrapper h2');
    var $greetTextArea = $chatWithTaPop.find('.greet-words textarea');
    var $inviteCheckboxItem = $chatWithTaPop.find('.invite-or-not .checkbox-item');
    var $inviteCheckbox = $chatWithTaPop.find('.invite-or-not i');
    var $okButton = $chatWithTaPop.find('.handle-button-wrapper .ok');
    var P_FSlotSelector = '#chatWithTaPop .filter-slot';
    var $slotEle = $(P_FSlotSelector);
    var $selectTemplate = $chatWithTaPop.find('.selectTemplate');
    var $selectedTemp = $selectTemplate.find('.selectedTemp');
    var $GreetTplList = $selectTemplate.find('ul.template-list');
    var $tplName = $selectedTemp.find('.name');
    var $noGreetingTpl = $chatWithTaPop.find('.no-greeting-tpl');
    var $hasWritedNum = $chatWithTaPop.find('.number-tips .writed-word-num');
    var $bottomButtonWrap = $chatWithTaPop.find('.handle-button-wrapper');

    /**
     * [chatWithTaCache 弹窗缓存数据]
     * 缓存弹窗中填写的数据，用来判断确认按钮的状态，关闭弹窗时记得重置为undefined,关闭弹窗需要清空选中状态
     */
    var chatWithTaCache = {
        cUserId: undefined,         // [number]和ta聊聊，ta（C端用户）的id
        positionId: undefined,      // [number] 当前选中的职位id
        greetWords: undefined,      // [string] 当前填写的招呼用语
        toInvite: false,            // [boolean] 是否选择“顺便邀请投递”
        greetTplData: []            // [array] 接口返回的招呼模板的数据
    }


    //监听来自positionFilter模块trigger的事件
    // 成功选择了有效职位等情况
    $slotEle.on(P_F_EVENT.selectPosSucc, function (e, data) {
        chatWithTaCache.positionId = data.selectedPositionId;
        if (!$leftTitle.hasClass('green')) {
            $leftTitle.addClass('green')
        }
        ;
        _changeOKbuttonState();
    })


    // 点击招展开呼模板
    $chatWithTaPop.on('click', '.selectedTemp', function (e) {
        e.stopPropagation();
        if ($GreetTplList.is(':visible')) {
            $GreetTplList.hide();
            $selectedTemp.find('i').attr('class', 'icon-arrow-down');
        } else {
            $GreetTplList.show();
            $selectedTemp.find('i').attr('class', 'icon-arrow-up');
        }
    })
    // 点击其他区域收起列表
    $(document).on('click', function (e) {
        if ($GreetTplList.is(':visible')) {
            $GreetTplList.hide();
            $selectedTemp.find('i').attr('class', 'icon-arrow-down');

        }
    })
    // 点击选择招呼模板
    $GreetTplList.on('click', 'li', function (e) {
        var $this = $(this);

        var index = $this.attr('data-index');
        if ($this.hasClass('not-use-tpl')) {
            _setGreetStatus({
                name: '不使用模板',
                id: '',
                content: ''
            });
        } else {
            _setGreetStatus(chatWithTaCache.greetTplData[index]);
        }
        $GreetTplList.hide();
        $selectedTemp.find('i').attr('class', 'icon-arrow-down');
    })
    //监听招呼语的输入框
    $chatWithTaPop.on('keyup input', '.greet-words textarea', function (e) {
        // console.log(e.type);
        var $this = $(this);
        if ($this.attr('data-compositionstart') === 'true') return; //中文输入没结束时不处理
        var value = $this.val().trim();
        var length = value.length;

        if (length > 200) {
            value = value.substr(0, 200);
            $this.val(value);
            length = 200;
        }
        if (length >= 180) {
            $hasWritedNum.addClass('warning-color');
        } else {
            $hasWritedNum.removeClass('warning-color');
        }
        $hasWritedNum.text(length);
        chatWithTaCache.greetWords = value;
        if (length > 0) {
            if (!$rightTitle.hasClass('green')) {
                $rightTitle.addClass('green')
            }
            ;
        } else {
            if ($rightTitle.hasClass('green')) {
                $rightTitle.removeClass('green')
            }
            ;
        }
        _changeOKbuttonState();

    }).on('compositionstart', '.greet-words textarea', function (e) {
        $(this).attr('data-compositionstart', 'true');

    }).on('compositionend', '.greet-words textarea', function (e) {
        $(this).attr('data-compositionstart', 'false');
        // console.log('compositionend');
        $(this).trigger('keyup');
    })

    // 点击勾选邀请投递
    $inviteCheckboxItem.on('click', function (e) {
        var $this = $(this);
        var $checkboxIcon = $this.find('i');
        if ($checkboxIcon.hasClass('icon-checkbox')) {
            $checkboxIcon.removeClass('icon-checkbox').addClass('icon-checkedbox');
            chatWithTaCache.toInvite = true;
        } else {
            $checkboxIcon.removeClass('icon-checkedbox').addClass('icon-checkbox');
            chatWithTaCache.toInvite = false;
        }
    })
    // 关闭弹窗将数据还原为初始状态
    $chatWithTaPop.on('click', '.modal-header .close', function (e) {
        //清空数据
        chatWithTaCache = {
            cUserId: undefined,
            positionId: undefined,
            greetWords: undefined,
            toInvite: false,
            greetTplData: []
        };
        if ($inviteCheckbox.hasClass('icon-checkedbox')) {
            $inviteCheckbox.removeClass('icon-checkedbox').addClass('icon-checkbox');
        }
        $okButton.removeClass('can-click');
        $leftTitle.removeClass('green');
        $rightTitle.removeClass('green');
        $(document).trigger('click');

        $greetTextArea.val('');
        $hasWritedNum.text('0');
        _clearErrTips($bottomButtonWrap);
        $slotEle.trigger(P_F_EVENT.clearCache); //告诉positionFilter模块清除缓存

    })
    // 点击确定按钮
    $okButton.on('click', function (e) {
        var $this = $(this);
        if ($this.hasClass('can-click') && chatWithTaCache.positionId && chatWithTaCache.greetWords) {
            var data = {
                cUserId: chatWithTaCache.cUserId,
                positionId: chatWithTaCache.positionId,
                greetingContent: chatWithTaCache.greetWords,
                inviteDeliver: chatWithTaCache.toInvite
            };//用于传给后端
            createNewSession(chatWithTaCache.cUserId, data, function (resp) {
                var state = parseInt(resp.state, 10) || -1;

                if (state === 1) {
                    // 修改和ta聊聊按钮状态
                    var $chatWithTaButton = $('.' + config.chatClassName + '[data-cuserid=' + chatWithTaCache.cUserId + ']');
                    var $searchBoxDes = $(config.numSeletor); //这个修改页面中沟通次数依赖于页面，看怎么搞
                    if ($chatWithTaButton.length > 0) {
                        $chatWithTaButton.removeClass(config.chatClassName)
                            .addClass(config.chatAgainClassName)
                            .text('继续聊聊')
                            .attr({
                                target: '_blank',
                                href: '/im/chat/index.htm?activeId=' + chatWithTaCache.cUserId
                            });
                    }
                    if ($searchBoxDes.length > 0) {
                        var count = parseInt($searchBoxDes.text(), 10) || 0;
                        if (count > 0) count--;
                        $searchBoxDes.text(count);
                    }
                    $body.trigger('chatSuccess', {cUserId: chatWithTaCache.cUserId});
                    $chatWithTaPop.find('.modal-header .close').trigger('click');

                    var topTips = new lg.Widgets.Controls.TopTips({
                        header: '消息发送成功',
                        hasNoBack: true,
                        needHoverStop: false,
                        decoration: 'chat-with-ta-top-tips'
                    });

                } else {
                    _showErrTips($bottomButtonWrap, resp.message || '创建对话失败');
                }
            })

        } else {
            e.stopPropagation(); // 阻止发送点击埋点统计
            return;
        }

    })
    // // 点击取消按钮
    // $chatWithTaPop.on('click', 'span.cancel', function (e) {
    //     $chatWithTaPop.find('.modal-header .close').trigger('click');
    // })

    /**
     * 判断是否选择了职位及是否填写了招呼模板，改变“确定”按钮的状态
     */
    function _changeOKbuttonState() {
        if (chatWithTaCache.positionId !== undefined && chatWithTaCache.greetWords !== undefined && chatWithTaCache.greetWords !== '') {
            if (!$okButton.hasClass('can-click')) {
                $okButton.addClass('can-click')
            }
        } else {
            if ($okButton.hasClass('can-click')) {
                $okButton.removeClass('can-click')
            }
        }
    }

    /**
     * 和ta聊聊 bootstrap modal 弹窗显示
     */
    function _showPop() {
        if ($chatWithTaPop.length > 0) {
            // 该配置可以保证只能通过点击关闭按钮来关闭弹窗，ESC键和点击阴影区都将不能关闭弹窗，
            // 这样做保证了弹窗关闭的操作的唯一性，便于成功清除缓存
            $chatWithTaPop.modal({
                backdrop: 'static',
                keyboard: false
            });
        }
    }

    function _showErrTips($selector, errMsg) {
        var errHtml = '<span class="error-tips" style="display:inline-block;margin-left:20px;color:#fd5f39;"><i class="icon-beidiao-warn"></i>&ensp;<span class="msg">' + errMsg + '</span></span>';
        var $errTips = $selector.find('.error-tips');
        if ($errTips.length > 0) {
            $errTips.find('.msg').text(errMsg);
        } else {
            $selector.append(errHtml);
        }
    }

    function _clearErrTips($selector) {
        var $errTips = $selector.find('.error-tips');
        if ($errTips.length > 0) {
            $errTips.remove();
        }
    }

    /**
     * 初始化招呼模板
     * @param  {array} tplArr [description]
     * @return {[type]}      [description]
     */
    function _initGreetTpl(tplArr) {
        chatWithTaCache.greetTplData = tplArr;
        var str = '';
        var defaultTplIndex;

        if (tplArr && tplArr.length > 0) {
            // 有模板的时候
            for (var i = 0; i < tplArr.length; i++) {
                if (tplArr[i].defaults) {
                    defaultTplIndex = i;
                }
                str += '<li data-index="' + i + '" title="' + tplArr[i].name + '">' + tplArr[i].name + '</li>';
            }
            str += '<li class="not-use-tpl">不使用模板</li>';
            $GreetTplList.html(str);
            if (typeof defaultTplIndex !== 'undefined') {
                $GreetTplList.find('li[data-index=' + defaultTplIndex + ']').trigger('click');
            } else {
                $GreetTplList.find('.not-use-tpl').trigger('click');
            }
            $selectTemplate.show();
            $noGreetingTpl.hide();
        } else {
            //无模板可用
            $selectTemplate.hide();
            $noGreetingTpl.show();
        }

    }

    /**
     * [选择第i个模板]
     * @param {object} dataI 提供的模板数组的第i项数据
     * 具体接口还没给，咱不写详细注释
     */
    function _setGreetStatus(dataI) {
        $tplName.text(dataI.name);
        $tplName.attr('data-id', dataI.id);
        $greetTextArea.val(dataI.content).trigger('keyup');
    }

    /**
     * [_showChatWithTaPop description]
     * @param  {object} data           和ta聊聊弹窗需要的所有数据，包括/im/session/bootstrap/${cUserId}.json接口返回的data和插入的预先选中职位id
     * @param  {object} data.positionSelectorVO          接口返回的职位选择器的数据
     *  @param  {number} data.positionSelectorVO.selectedPositionId         插入的预先选中职位id
     * @param {array} data.greetingList 招呼模板数据
     */
    function _showChatWithTaPop(data) {
        var positionSelectorVO = data.positionSelectorVO;
        var greetTplData = data.greetingList;

        positionFilter.renderPositionFilter(positionSelectorVO, P_FSlotSelector);  // 调用职位选择器模块提供的渲染选择器的方法
        _initGreetTpl(greetTplData);  // 初始化招呼模板
        $inviteCheckboxItem.trigger('click'); // 初始化“顺便邀请”，默认选中,依赖于关闭时清空了勾选状态
        $okButton.attr('data-lg-tj-cid', chatWithTaCache.cUserId);
        _showPop(); // 显示弹窗
    }

    /**
     * [判断为已开通招聘服务之后调用的方法, 如果不需要判断开通招聘服务的话也可直接导出此方法]
     * @param  {object} options
     * @param  {number} options.cUserId       C端用户id，必选
     * @param  {number} options.selectPosId   聊聊弹窗预先选中的职位id, 非必选
     */
    function getChatWithTaPop(options) {
        $.ajax({
            url: '/im/session/bootstrap/' + options.cUserId + '.json',
            data: {
                cUserId: options.cUserId
            },
            success: function (data) {
                var state = parseInt(data.state, 10);
                if (state === 1) {
                    var _data = data.content.data;
                    if (options.selectPosId) {
                        _data.positionSelectorVO.selectedPositionId = options.selectPosId;
                    }
                    _showChatWithTaPop(_data);
                } else if (state === 40301) {
                    var confirm = new lg.Widgets.Controls.Confirm({
                        content: '主动沟通点数已用完',
                        submitText: '好的',
                        noCancelBtn: true,
                        SubmitBtn: function (e) {
                            e.control.setRemove();
                        }
                    });
                } else if (state === 40302) {
                    var confirm = new lg.Widgets.Controls.Confirm({
                        content: '晚来了一步，该用户已设置隐私保护，暂无法查看。',
                        submitText: '好的',
                        noCancelBtn: true,
                        SubmitBtn: function (e) {
                            e.control.setRemove();
                        }
                    });
                } else {
                    alert(data.message);
                }
            },
            error: function (data) {
                alert('网络错误，稍后再试');
            }
        })
    }


    /**
     * [导出的用于调用和ta聊聊弹窗的方法]
     * @param  {object} options
     * @param  {number} options.cUserId       C端用户id，必选
     * @param  {number} options.selectPosId   聊聊弹窗预先选中的职位id, 非必选
     */
    function chatWithTa(options) {
        chatWithTaCache.cUserId = options.cUserId; // 缓存cUserId，用于最后点击确定按钮时发请求的请求参数
        judgeOpenServiceState(getChatWithTaPop, options); // 先执行是否开通招聘服务判断，然后执行和ta聊聊弹窗回调函数
    }


    module.exports = {
        initChatWithTa: initChatWithTa     // 可选
    }
})

/*!plus/modules/common/js/inputUtils.js*/
;/**
 * 输入框工具集
 *
 * @author fayipan@lagou.com
 */

define('plus/modules/common/js/inputUtils', ['require', 'exports', 'module'], function (require, exports, module) {


    module.exports = {
        /**
         * 弹框组件中 textarea 输入框交互
         * 比如：捎句话
         *
         * @param {Event Object} evt 用户交互事件
         * @param {Number} max 最大输入长度
         * @param {String} tipSelector 提示 DOM 节点选择符
         */
        popboxTextAreaInput: function (evt, max, tipSelector) {
            var $target = $(evt.target);
            var $delegateTarget = $(evt.delegateTarget);

            if ($target.prop('compositionInput') === true) { // 汉字输入法
                return;
            }

            max = max || 100;
            tipSelector = tipSelector || '.message-tip span';

            var value = $.trim($target.val());
            var length = value.length;


            if (max >= length) {
                $target.data('currVal', value); // 存储 textarea 当前有效值
                evt.preventDefault();
            } else {
                $target.val($target.data('currVal'));
            }

            $delegateTarget.find(tipSelector).text(Math.max(0, max - length));
        }
    }
});

/*!common/widgets/phone-call-pop/main.js*/
;/**
 * 电话呼叫弹窗
 *
 * create by steventao@lagou.com
 * update by steventao@lagou.com
 */
define('common/widgets/phone-call-pop/main', ['require', 'exports', 'module', 'common/widgets/open-recruit-service-pop/main'], function (require, exports, module) {
    var judgeOpenServiceState = require('common/widgets/open-recruit-service-pop/main').judgeOpenServiceState;

    var // 公共变量
        popCache = {
            cUserId: undefined, // 登录用户的id
            resumeKey: undefined, // 简历的Key
            phoneNum: undefined, // 登录用户电话号码
            virtualPhone: undefined, // 生成的虚拟手机号码
            recerdStates: 0, // 0：电话呼叫；1：再次呼叫
            expireTime: undefined
        },
        $popClose = $('.pop-close'),
        $popMask = $('#popMask'),
        $popMaskTrans = $('#popMaskTrans'),
        $popContent = $('.pop-content'),

        // 已投递弹窗
        $popDelivered = $('#popDelivered'),
        $popDeliveredButton = $('#popDelivered .button'),
        $popColleDelivered = $('#popColleagueDelivered'),
        $popColleDeliveredButton = $('#popColleagueDelivered .continue'),
        $popColleText = $('#popColleagueDelivered .pop-text'),

        // 电话呼叫功能介绍弹窗
        $popIntroMask = $('#popIntroMask'),
        $popIntro = $('#popIntro'),
        $introContinue = $('#popIntro .continue'),

        // 确认手机号弹窗
        $popPhoneConfirm = $('#popPhoneConfirm'),
        $popPhoneNumber = $('.pop-phone-number'),
        $popPhoneChange = $('#popPhoneChange'),
        $popPhoneConf = $('.pop-phone-conf'),
        $popPhoneConfButton = $('.pop-phone-confirm .button'),
        $popPhoneConfTip = $('.pop-phone-confirm .wrong-tip'),
        $popPhoneConfTipContent = $('.pop-phone-confirm .tip-content'),
        $popPhoneInput = $('.pop-phone-input'),
        $popPhoneInputEle = $('.pop-phone-input .phone-input'),
        $popPhoneI = $('.pop-phone-input i'),

        // 电话呼叫点数相关弹窗
        $popDeductPoints1 = $('#popDeductPoints1'),
        $popDeductPoints2 = $('#popDeductPoints2'),
        $popDeductPoints3 = $('#popDeductPoints3'),

        // 获取候选人动态号码弹窗
        $popVirtualTrumpet = $('#popVirtualTrumpet'),
        $loading = $('#popVirtualTrumpet .loading2'),
        $numberGetSuccess = $('#popVirtualTrumpet .number-get-success'),
        $numberGetFail = $('#popVirtualTrumpet .number-get-fail'),
        $numberGet = $('#popVirtualTrumpet .number-get'),
        $effectTime = $('#popVirtualTrumpet .effect-time'),
        $trumpePopBottom = $('#popVirtualTrumpet .pop-bottom'),
        $trumpePopRefresh = $('#popVirtualTrumpet').find('.icon-yun-refresh'),

        // 搜索框后数值
        $remainTimes = $('.LG-chat-remain-times .remainTimes'),
        $haveCallTimes = $('.LG-chat-remain-times .haveCallTimes'),

        // 其他变量
        re = /^(0|86|17951)?((13[0-9]|15[012356789]|17[0135678]|18[0-9]|14[57])[0-9]{8})$/i,
        bottomTextArr = ['获取中，请稍后', '请使用尾号<span class="green"></span>的手机呼叫', '获取失败，请重新再试<i class="icon-yun-refresh"></i>'],
        callEle = undefined;


    $('.pop-close, #popDeductPoints2 .button').on('click', function () {
        $popMask.fadeOut();
        $popContent.fadeOut();
        $popIntroMask.fadeOut();
    });
    $('#popMaskTrans, #popDelivered .button, #popDelivered .delvered-cancel,#popColleagueDelivered .button, #popColleagueDelivered .button').on('click', function () {
        $popMaskTrans.fadeOut();
        $popContent.fadeOut();
    });

    /**
     * 弹窗路由方法
     * @param  {[Object]} response   [callPhone.json接口返回对象]
     * @param  {[String]} cUserId     [使用系统的hr的id]
     * @param  {[String]} resumeKey  [简历id]
     */
    function _popUp(response, cUserId, resumeKey) {
        if (cUserId) {
            popCache.cUserId = cUserId;
            popCache.resumeKey = resumeKey;
            popCache.phoneNum = response.content.data && response.content.data.result.phone;
            popCache.virtualPhone = response.content.data && response.content.data.result.virtualPhone;
        }
        switch (response.state) {
            case 1:
                _getVritualTrumpe();
                break;
            case 1006:
                _popPhoneConfirmUp(popCache.phoneNum);
                break;
            case 1009:
                _popDeductPoints1Up();
                break;
            case 1010:
                _popDeductPoints3Up();
                break;
            case 1011:
                _popDeliveredUp();
                break;
            case 1019:
                var _remainTimes = response.content.data && response.content.data.result.remainTimes;
                var _haveCallTimes = response.content.data && response.content.data.result.haveCallTimes;
                if (_remainTimes) {
                    $remainTimes.text(_remainTimes);
                    $haveCallTimes.text(_haveCallTimes);
                }
                _popDeductPoints2Up();
                break;
            case 1021:
                _popIntroUp();
                break;
            case 1024:
                _popColleDeliveredUp(response.content.data.result.hrName, response.content.data.result.email);
                break;
        }
    }

    /*
     弹窗函数
     */
    function _popDeliveredUp() {
        $popDeliveredButton.attr('href', '/search/resume/' + popCache.resumeKey + '.htm');
        $popDelivered.fadeIn();
        $popMaskTrans.fadeIn();
    }

    function _popColleDeliveredUp(hrName, email) {
        var _textStr = '您的同事' + hrName + '（' + email + '）' + '已经收到过该候选人的简历，请联系您的同事，并通过简历中的联系方式拨打。';
        $popColleText.text(_textStr);
        $popColleDelivered.fadeIn();
        $popMaskTrans.fadeIn();
    }

    function _popIntroUp() {
        $popColleDelivered.hide();
        $popMaskTrans.hide();
        $popIntroMask.fadeIn();
        // $popIntro.fadeIn();
        $popMask.fadeIn();
    }

    function _popPhoneConfirmUp(phoneNum) {
        $popPhoneConfTip.hide();
        var _shouji = re.test(phoneNum);
        if (_shouji) {
            // 如果是有效的手机号码
            $popPhoneNumber.text(phoneNum);
            $popPhoneConf.show();
            $popPhoneInput.hide();
        }
        else {
            // 如果是无效的手机号码
            popCache.phoneNum = '';
            $popPhoneConf.hide();
            $popPhoneInput.show();
            $popPhoneConfButton.text('保存');
        }
        $popMask.fadeIn();
        $popPhoneConfirm.fadeIn();
    }

    function _popDeductPoints1Up() {
        $popMask.fadeIn();
        $popDeductPoints1.fadeIn();
    }

    function _popDeductPoints2Up() {
        $popMask.fadeIn();
        $popDeductPoints2.fadeIn();
    }

    function _popDeductPoints3Up() {
        $popMask.fadeIn();
        $popDeductPoints3.fadeIn();
    }

    function _popVirtualTrumpetUp(successFlag) {
        if (successFlag) {
            $loading.hide();
            $numberGetSuccess.show();
            $numberGetFail.hide();
            $numberGet.text(popCache.virtualPhone);
            var _timeStr = popCache.expireTime + ' 前有效';
            $effectTime.text(_timeStr);
            bottomTextArr[1] = '请使用尾号<span class="green"> ' + popCache.phoneNum.substr(popCache.phoneNum.length - 4) + ' </span>的手机呼叫'
            $trumpePopBottom.html(bottomTextArr[1]);
        }
        else {
            $loading.hide();
            $numberGetSuccess.hide();
            $numberGetFail.show();
            $trumpePopBottom.html(bottomTextArr[2]);
        }

        $popDeductPoints1.fadeOut();
        $popDeductPoints2.fadeOut();
        $popDeductPoints3.fadeOut();
        $popMask.fadeIn();
        $popVirtualTrumpet.fadeIn();
    }

    /*
     非弹窗工具函数
     */
    function _phoneCheck(phoneNum) {
        if (re.test(phoneNum)) {
            $popPhoneI.attr('class', 'icon-beidiao-right');
            return true;
        }
        else {
            $popPhoneI.attr('class', 'icon-beidiao-wrong');
            return false;
        }
    }

    function _getVritualTrumpe() {
        $.ajax({
            url: '/phonecall/getVirtualNum.json',
            data: {
                'cUserId': popCache.cUserId || '',
            },
            type: 'POST',
            dataType: 'json',
            success: function (res) {
                if (res.success) {
                    if (res.state === 1) {
                        // callEle.html();
                        popCache.phoneNum = res.content.data && res.content.data.result.phone;
                        popCache.virtualPhone = res.content.data && res.content.data.result.virtualPhone;
                        popCache.expireTime = res.content.data && res.content.data.result.expireTime;
                        var _remainTimes = res.content.data && res.content.data.result.remainTimes;
                        var _haveCallTimes = res.content.data && res.content.data.result.haveCallTimes;
                        if (_remainTimes) {
                            $remainTimes.text(_remainTimes);
                            $haveCallTimes.text(_haveCallTimes);
                        }
                        if (callEle) {
                            callEle.html('<i class="icon icon-call-1"></i> 再次呼叫');
                        }
                        $('body').trigger('phoneCallSuccess', {cUserId: popCache.cUserId});
                        _popVirtualTrumpetUp(true);
                    }
                    else {
                        _popUp(res);
                    }
                }
                else {
                    _popVirtualTrumpetUp(false);
                }
            },
            error: function () {
                console.log('弹窗部分/phonecall/callPhone.json请求出错');
            }
        });
    }

    function _loading() {
        $loading.show();
        $numberGetSuccess.hide();
        $numberGetFail.hide();
        $trumpePopBottom.html(bottomTextArr[0]);
    }

    /*
     事件
     */
    $popDeliveredButton.on('click', function () {

    });
    $popColleDeliveredButton.on('click', function () {
        $.ajax({
            url: '/phonecall/getVirtualNumFromOtherHr.json',
            data: {
                'cUserId': popCache.cUserId || '',
            },
            type: 'POST',
            dataType: 'json',
            success: function (res) {

                popCache.phoneNum = res.content.data && res.content.data.result.phone;
                _popUp(res);
            },
            error: function () {
                console.log('/phonecall/getVirtualNumFromOtherHr.json fail');
            }
        });
    });
    $introContinue.on('click', function () {

        // 如果有勾选则请求接口保存数据,否则直接继续弹窗
        var _noTipAgain = $('#noTipAgain').prop('checked');
        $.ajax({
            url: '/phonecall/afterPhoneCallStep.json',
            data: {
                'cUserId': popCache.cUserId || '',
                'noTipAgain': _noTipAgain,
                'recerdStates': popCache.recerdStates
            },
            type: 'POST',
            dataType: 'json',
            success: function (res) {
                if (res.success) {
                    $popIntroMask.fadeOut();
                    popCache.phoneNum = res.content.data && res.content.data.result.phone;
                    _popUp(res);
                }
            },
            error: function () {
            }
        });
    });

    $popPhoneInputEle.on('blur', function () {
        var _phoneNum = $popPhoneInputEle.val();
        _phoneCheck(_phoneNum);
    });
    $popPhoneChange.on('click', function () {
        $popPhoneInputEle.val($popPhoneNumber.text())
        $popPhoneConf.hide();
        $popPhoneInput.show();
        $popPhoneConfButton.text('保存');
    });
    $popPhoneConfButton.on('click', function () {
        var _buttonText = $popPhoneConfButton.text().trim();
        var _phoneNum = $popPhoneInputEle.val();
        if (_buttonText === '确认以继续') {
            $.ajax({
                url: '/phonecall/afterConfirmPhoneNum.json',
                data: {
                    'cUserId': popCache.cUserId || ''
                },
                type: 'POST',
                dataType: 'json',
                success: function (res) {
                    // popCache.phoneNum = res.content.data && res.content.data.result.phone;
                    if (res.success) {
                        $popPhoneConfirm.fadeOut();
                        $popVirtualTrumpet.fadeIn();
                        $popPhoneConfTip.hide();
                        _popUp(res);
                    }
                    else {
                        $popPhoneConfTipContent.text(res.message);
                        $popPhoneConfTip.show();
                    }
                },
                error: function () {
                }
            });
        }
        else if (_buttonText === '保存') {
            var _isPhoneNumber = _phoneCheck(_phoneNum);
            if (_isPhoneNumber) {
                $.ajax({
                    url: '/phonecall/modifyPhone.json',
                    data: {
                        phone: _phoneNum
                    },
                    type: 'POST',
                    dataType: 'json',
                    success: function (res) {
                        if (res.state === 1) {
                            $popPhoneConfButton.text('确认以继续');
                            $popPhoneI.attr('class', '');
                            $popPhoneNumber.text(_phoneNum);
                            popCache.phoneNum = _phoneNum;
                            $popPhoneConf.show();
                            $popPhoneInput.hide();
                        }
                    },
                    error: function () {
                        console.log('/phonecall/modifyPhone.json调用失败');
                    }
                });
            }
        }
    });

    $trumpePopBottom.on('click', '.icon-yun-refresh', function () {
        _loading();
        _getVritualTrumpe();
    });

    $popDeductPoints1.on('click', '.button', function () {
        _loading();
        $popDeductPoints1.fadeOut();
        $popVirtualTrumpet.fadeIn();
        _getVritualTrumpe();
    });

    $popDeductPoints3.on('click', '.button', function () {
        _loading();
        $popDeductPoints3.fadeOut();
        $popVirtualTrumpet.fadeIn();
        _getVritualTrumpe();
    });

    /**
     对外开放电话呼叫弹窗接口
     */
    var isPhoneCalling = false;

    function _phoneCall(options) {
        if (isPhoneCalling === true) {
            return;
        }
        isPhoneCalling = true;
        $.ajax({
            url: '/phonecall/ifGetOrderGetVirtualNum.json',
            data: {
                'cUserId': options.cUserId
            },
            type: 'POST',
            dataType: 'json',
            success: function (res) {
                isPhoneCalling = false;
                popCache.recerdStates = 0;

                // content在这里是电话号码
                _popUp(res, options.cUserId, options.resumeKey);
            },
            error: function () {
                console.log('/phonecall/ifGetOrderGetVirtualNum.json request fail');
            }
        });
    }

    /**
     * 电话呼叫弹窗
     * @param  {[Number]} cUserId   [登录用户ID 必传]
     * @param  {[String]} resumeKey [简历Key 必传]
     * @param  {[]} ele [再次聊聊文本的jq元素]
     */
    function phoneCall(cUserId, resumeKey) {
        callEle = $('.call-ta[data-cuserid = ' + cUserId + ']');
        var callEleText = callEle.text().trim();
        if (callEleText.indexOf('电话呼叫') != -1) {
            var _options = {};
            _options.cUserId = cUserId;
            _options.resumeKey = resumeKey;
            judgeOpenServiceState(_phoneCall, _options);
        }
        else if (callEleText.indexOf('再次呼叫') != -1) {
            callEle = undefined;
            phoneCallAgain(cUserId, resumeKey);
        }
    }

    /**
     * 再次呼叫弹窗
     * @param  {[Number]} cUserId   [登录用户ID 必传]
     * @param  {[String]} resumeKey [简历Key 必传]
     */
    var isPhoneCallAgaing = false;

    function phoneCallAgain(cUserId, resumeKey) {
        if (isPhoneCallAgaing === true) {
            return;
        }
        isPhoneCallAgaing = true;
        $.ajax({
            url: '/phonecall/againPhoneCall.json',
            data: {
                'cUserId': cUserId
            },
            type: 'POST',
            dataType: 'json',
            success: function (res) {
                isPhoneCallAgaing = false;
                popCache.recerdStates = 1;
                popCache.cUserId = cUserId;
                popCache.resumeKey = resumeKey;
                if (res.success) {
                    if (res.state === 1) {

                        popCache.phoneNum = res.content.data && res.content.data.result.phone;
                        popCache.virtualPhone = res.content.data && res.content.data.result.virtualPhone;
                        popCache.expireTime = res.content.data && res.content.data.result.expireTime;
                        _popVirtualTrumpetUp(true);
                    }
                    else {
                        _popUp(res);
                    }
                }
                else {
                    _popVirtualTrumpetUp(false);
                }
            },
            error: function () {
                console.log('/phonecall/againPhoneCall.json request fail');
            }
        });
    }

    /**
     * 暴露接口
     */
    module.exports = {
        phoneCall: phoneCall,
        phoneCallAgain: phoneCallAgain
    }
});
/*!plus/modules/result-list/main.js*/
;define('plus/modules/result-list/main', ['require', 'exports', 'module', 'common/widgets/chat-with-Ta-pop/main', 'chat/modules/api/chat-api', 'plus/modules/common/js/inputUtils', 'common/widgets/phone-call-pop/main'], function (require, exports, module) {
    require('common/widgets/chat-with-Ta-pop/main');
    var api = require('chat/modules/api/chat-api');
    var inputUtils = require('plus/modules/common/js/inputUtils');
    var phone = require('common/widgets/phone-call-pop/main');
    var $container = $('.container');
    var $searchBoxDes = $('.LG-chat-remain-times .num');
    var $floatingChat = $('#floating-chat');
    var $floatingBody = $('#floating-body');
    var $inviteDone = $('#invite-done');
    var $resultList = $('.main-content');
    var $floatingPrechat = $('#floating-prechat');
    var params = window.initialState && window.initialState.params || {};


    /**
     * 简历[展开]/[收起]
     */
    $container.on('click', '.result_list_item', function (e) {
        var $target = $(e.target);
        var inClass = 'spreadIn';
        var outClass = 'spreadOut';
        var $arrow = $(this).find('.user_expr_short');
        if ($target.hasClass('chat_btn') || $target.hasClass('.call-btn') || $target.parents('.chat_btn, .call-btn').length) {
            return;
        }
        if ($arrow.hasClass(inClass)) {
            $arrow.removeClass(inClass).addClass(outClass);
            $(this).find('.info').css('height', 'auto');
        } else {
            $arrow.removeClass(outClass).addClass(inClass);
            $(this).find('.info').css('height', '0');
        }
    });


    // 电话呼叫相关按钮
    $container.on('click', '.call-ta', function (e) {
        e.stopPropagation();
        var $this = $(this);
        var resumeKey = $this.attr('data-resumeKey');
        var cUserId = parseInt($this.attr('data-cuserid'), 10);
        if (cUserId && resumeKey) {
            if ($this.hasClass('phone-disabled')) {
                //不支持呼叫
                return;
            } else if ($this.hasClass('phone-call')) {
                //电话呼叫
                phone.phoneCall(cUserId, resumeKey);
            } else if ($this.hasClass('phone-call-again')) {
                //再次呼叫
                phone.phoneCallAgain(cUserId, resumeKey);
            }
        } else {
            console.error('获取用户id或简历key失败');
        }
    })


    //确认提交沟通
    /**
     * currCompany：$!{userInfoTool.getCompanyName()},
     * companyName: /im/chat/getUserInfo.json  data.content.data.companyName
     * 这段代码是指：在点击原和他聊聊的弹窗中的确认按钮时，先发请求比较两个公司名，如果相同才发起和他聊聊的请求，认为并没有什么用，暂时去掉
     * by Julianzeng@lagou.com 2017/05/18
     */
    /**
     $floatingChat.on('click', '.popup-ensure', function(e) {
        var type = parseInt($floatingChat.attr('data-type'), 10);
        //捎句话存
        sendawordtpl = $('.floating-message-select .icon-checkedbox').is(":visible") ? $floatingChat.find('.floating-message .floating-text').val() : '';

        if (type === 1) { // 聊天(标记data-type为1)
            if (currCompany === companyName) {
                addToChatList();
            } else {
                new lg.Widgets.Controls.Confirm({
                    content: '确认以 ' + companyName + ' 的身份发起聊天?',
                    submitText: "确定",
                    cancelText: "取消",
                    SubmitBtn: function(e) {
                        addToChatList();
                        e.control.setRemove();
                    },
                    CancelBtn: function(e) {}
                });
            }
        } else if (type === 2) { // 发送邀请(标记data-type为2)
            sendRequest();
        }
    **/

})

/*!plus/modules/filter-option/main.js*/
;/**
 * plus 人才推荐：职位搜索过滤器
 *
 * @author fayipan@lagou.com
 */

define('plus/modules/filter-option/main', ['require', 'exports', 'module', 'plus/modules/top-queries/main'], function (require, exports, module) {
    var $filtersOverview = $('.filters-overview');
    var $filterOptions = $('#filterOptions');
    var $allCities = $filterOptions.find('.all-cities');
    var $overviewFilters = $('#overviewFilters');
    var className = 'selected';
    var changeEvt = '__filterChange';
    var goodsInfo = CONST_VARS('goodsInfo') || {};

    /**
     * 更新筛选条件
     *
     * @param {string} prop 筛选项 key
     * @param {mixed} value 筛选项 vaule
     */
    var filterCache = (window.initialState && window.initialState.params) || {};

    function __updateFilterCache(prop, value) {
        var fireChangeEvt = false;

        if (value === undefined && filterCache.hasOwnProperty(prop)) { // 删除 prop
            delete filterCache[prop];
            fireChangeEvt = true;
        } else if (typeof prop === 'string' && prop.length > 0 && filterCache[prop] !== value) {
            if (prop === 'isChat' && parseInt(value, 10) === 0) { // 聊天状态单独处理
                delete filterCache[prop];
            } else {
                filterCache[prop] = value;
            }
            fireChangeEvt = true;
        }

        if (fireChangeEvt === true) {
            if (prop !== 'pageNo') {
                filterCache.pageNo = 1;
            }
            $filterOptions.trigger(changeEvt, [filterCache]);
        }
    }

    /**
     * 城市筛选交互
     */
    $filterOptions.on('click', '.city-filter .city', function (e) {
        var $me = $(this);
        var city = $me.attr('data-value');

        if ($me.hasClass(className) || city === filterCache.city) {
            return;
        }

        __updateFilterCache('city', city);
        $filterOptions.find('.hot-cities .' + className).text($me.text());
        $filterOptions.find('.city-filter .city').show();
        $me.hide();

        try { // 记录用户选择城市，用于全局搜索框搜索
            window.sessionStorage.setItem('__plusFilterCity', city);
        } catch (e) {
        }
    });

    /**
     * hover 显示 "更多" 城市
     */
    $filterOptions.on('mouseenter', '.hot-cities .more', function (e) {
        var $icon = $(this).find('.css-icon-down-arrow');

        if ($allCities.height() === 0) {
            $allCities.css('max-height', '108px');
            $icon.css('transform', 'rotateZ(180deg)');
        }
    });
    $filterOptions.on('mouseleave', '.city-filter', function (e) {
        var $icon = $(this).find('.more .css-icon-down-arrow');

        if ($allCities.height() > 0) {
            $allCities.css('max-height', '0');
            $icon.css('transform', 'rotateZ(0)');
        }
    });

    /**
     * 学历筛选交互
     */
    $filterOptions.on('click', '.education .radio-item', function (e) {
        var $me = $(this);

        if ($me.hasClass(className)) {
            return;
        }

        __updateFilterCache('education', $me.attr('data-value'));
        $me.siblings('.radio-item').removeClass(className);
        $me.addClass(className);
    });

    /**
     * 取消学历筛选
     */
    $filterOptions.on('click', '.education .radio-item .del', function (e) {
        e.stopPropagation();

        $(this).parents('.radio-item').removeClass(className);
        __updateFilterCache('education');
    });

    /**
     * 复选框交互
     */
    $(document).on('click', '.checkbox-item', function (e) {
        var $me = $(this);
        var $icon = $me.find('.checkbox');
        var checkedClass = 'icon-checkedbox';
        var uncheckedClass = 'icon-checkbox';
        var prop = $icon.attr('data-prop');

        if ($icon.hasClass(uncheckedClass)) {
            __updateFilterCache(prop, 1);
            $icon.removeClass(uncheckedClass).addClass(checkedClass);
        } else if ($icon.hasClass(checkedClass)) {
            __updateFilterCache(prop, 0);
            $icon.removeClass(checkedClass).addClass(uncheckedClass);
        }
    });

    /**
     * 横轴滑动交互
     */
    (function () {
        var minWidthAttr = 'data-min-width';
        var maxWidthAttr = 'data-max-width';
        var realWidthAttr = 'data-real-width';
        var startPointerClass = 'axis-start-pointer';
        var endPointerClass = 'axis-end-pointer';

        var pointer = {
            min: undefined, // width 最小取值
            max: undefined  // width 最大取值
        };
        var $elem = null;   // 滑动元素
        var moving = false; // 标记元素处于滑动状态
        var initialWidth = undefined;   // 滑动起点，元素 width 取值
        var initialOffsetX = undefined; // 滑动起点 X 轴偏移
        var stepUnit = undefined;       // 单位刻度长度
        var totalLength = undefined;    // 横轴最大长度
        var valueMaps = {};             // 坐标轴取值 Maps

        /**
         * 点击选中刻度
         *
         * 就近原则，移动距离最近的指针
         */
        $('.axis-list').on('click', '.axis-item', function (e) {
            var $list = $(e.delegateTarget);
            stepUnit = parseInt($list.attr('data-step-unit'), 10);
            totalLength = parseInt($list.attr('data-total-length'), 10);
            $list.find('.axis-item').each(function (i, item) {
                valueMaps[String(i * stepUnit)] = $(item).attr('data-value');
            });

            var $me = $(this);
            var $startPointer = $me.siblings('.' + startPointerClass);
            var $endPointer = $me.siblings('.' + endPointerClass);
            var startPointerVal = $startPointer.width();
            var endPointerVal = totalLength - $endPointer.width();
            var offsetX = e.clientX - ($me.offset()).left; // 鼠标在单个刻度区间的偏移
            var newValue = ($me.position()).left + ( offsetX * 2 > stepUnit ? stepUnit : 0 ); // 命中具体的刻度点
            var result = []; // 选中的区间值

            if (Math.abs(newValue - startPointerVal) <= Math.abs(newValue - endPointerVal)) { // 就近原则，命中起点
                $startPointer.width(newValue);
                $startPointer.attr(realWidthAttr, newValue);
                result.push(valueMaps[String(newValue)]);

                $endPointer.attr(maxWidthAttr, totalLength - newValue - stepUnit);
                result.push(valueMaps[String(totalLength - $endPointer.width())]);
            } else { // 就近原则，命中终点
                result.push(valueMaps[String($startPointer.width())]);
                $startPointer.attr(maxWidthAttr, totalLength - newValue - stepUnit);

                $endPointer.css({
                    left: newValue + 'px',
                    width: (totalLength - newValue) + 'px'
                });
                $endPointer.attr(realWidthAttr, totalLength - newValue);
                result.push(valueMaps[String(newValue)]);
            }
            $list.trigger('complete', [result]); // 滑动完成，触发 complete 事件

            stepUnit = totalLength = undefined;
            valueMaps = {};
        });

        /**
         * 滑动开始
         */
        $('.' + startPointerClass + ', .' + endPointerClass).on('mousedown', function (e) {
            $elem = $(this);
            __initialState($elem, e);

            pointer = {
                min: parseInt($elem.attr(minWidthAttr), 10),
                max: parseInt($elem.attr(maxWidthAttr), 10)
            };
        });

        /**
         * 滚动开始，变量初始化
         */
        function __initialState($pointer, evt) {
            var $parent = $pointer.parents('.axis-list');
            var $items = $parent.find('.axis-item');
            var spanCount = $items.length - 1;

            moving = true;
            initialWidth = $pointer.width();
            initialOffsetX = evt.screenX;
            stepUnit = parseInt($parent.attr('data-step-unit'), 10);
            totalLength = parseInt($parent.attr('data-total-length'), 10);

            var min = parseInt($pointer.attr(minWidthAttr), 10);
            if (isNaN(min)) {
                $pointer.attr(minWidthAttr, 0);
            }

            if ($pointer.hasClass(startPointerClass)) { // 起点元素
                var $endPointer = $parent.find('.' + endPointerClass);
                $pointer.attr(maxWidthAttr, (spanCount - 1) * stepUnit - $endPointer.width());
            } else if ($pointer.hasClass(endPointerClass)) { // 终点元素
                var $startPointer = $parent.find('.' + startPointerClass);
                $pointer.attr(maxWidthAttr, (spanCount - 1) * stepUnit - $startPointer.width());
            }

            $items.each(function (i, item) {
                valueMaps[String(i * stepUnit)] = $(item).attr('data-value');
            });
        }

        /**
         * 滑动结束
         */
        $(document).on('mouseup', function (e) {
            if (moving) {
                var calibrateOffset = 9; // 滚动条两端重合时手动添加偏移，避免覆盖
                var width = $elem.width();
                width = Math.round(width / stepUnit) * stepUnit;
                $elem.width(width);
                $elem.attr(realWidthAttr, width); // 记录准确值(不带偏移)

                var result = [];
                if ($elem.hasClass(startPointerClass)) {
                    var $endPointer = $elem.siblings('.' + endPointerClass);
                    if ((width + $endPointer.width()) === totalLength) {
                        $elem.width(width - calibrateOffset);
                    }

                    var realWidth = parseInt($endPointer.attr(realWidthAttr), 10);
                    if (!isNaN(realWidth) && realWidth !== $endPointer.width()) { // 恢复校正
                        $endPointer.width(realWidth);
                        $endPointer.css({
                            left: totalLength - realWidth
                        });
                    }

                    result.push(valueMaps[String(width)]);
                    result.push(valueMaps[String(totalLength - $endPointer.width())]);
                } else if ($elem.hasClass(endPointerClass)) {
                    var $startPointer = $elem.siblings('.' + startPointerClass);
                    if ((width + $startPointer.width()) === totalLength) {
                        $elem.width(width - calibrateOffset);
                        $elem.css({
                            left: totalLength - width + calibrateOffset
                        });
                    } else {
                        $elem.css({
                            left: totalLength - width
                        });
                    }

                    var realWidth = parseInt($startPointer.attr(realWidthAttr), 10);
                    if (!isNaN(realWidth) && realWidth !== $startPointer.width()) { // 恢复校正
                        $startPointer.width(realWidth);
                    }

                    result.push(valueMaps[String($startPointer.width())]);
                    result.push(valueMaps[String(totalLength - width)]);
                }

                $elem.parents('.axis-list').trigger('complete', [result]); // 滑动完成，触发 complete 事件

                $elem = null;
                moving = false;
                initialWidth = undefined;
                initialOffsetX = undefined;
                stepUnit = undefined;
                totalLength = undefined;
            }
        });

        /**
         * 滑动中
         */
        $(document).on('mousemove', function (e) {
            if ($elem && moving === true) {
                var currOffsetX = e.screenX;
                var offset = $elem.hasClass(startPointerClass) ? (currOffsetX - initialOffsetX) : (initialOffsetX - currOffsetX);
                var width = initialWidth + offset;
                width = Math.max(
                    pointer.min,
                    Math.min(pointer.max, width)
                );

                $elem.width(width);

                if ($elem.hasClass(endPointerClass)) {
                    $elem.css({
                        left: totalLength - width
                    });
                }
            }
        });
    })();
    /**
     * 工作经历筛选条件
     */
    $filterOptions.on('complete', '.experience .axis-list', function (e, data) {
        if (({}).toString.call(data) === '[object Array]' && data.length === 2) {
            __updateFilterCache('workYear', (data[0] === data[1]) ? data[0] : data.join('-'));
        }
    });
    /**
     * 薪酬范围筛选条件
     */
    $filterOptions.on('complete', '.salary .axis-list', function (e, data) {
        if (({}).toString.call(data) === '[object Array]' && data.length === 2) {
            __updateFilterCache('expectSalary', (data[0] === data[1]) ? data[0] : data.join('-'));
        }
    });

    /**
     * 保存筛选条件
     */
    $filterOptions.on('click', '.save-filters', function (e) {
        $.ajax({
            url: GLOBAL_DOMAIN.ectx + '/search/saveFilter.json',
            data: filterCache,
            dataType: 'json'
        }).done(function (res, textStatus, jqXHR) {
            var state = parseInt(res.state, 10);

            if (state === 1) {
                var topQueries = require('plus/modules/top-queries/main');
                topQueries.add(filterCache);
                $filterOptions.find('.dropdown-tool i').click();
            }
        });
    });

    /**
     * 排序方式
     */
    $overviewFilters.on('click', '.order-item', function (e) {
        var $me = $(this);
        var className = 'active';

        __updateFilterCache('orderWay', $me.attr('data-value'));
        $me.siblings('.order-item').removeClass(className);
        $me.addClass(className);
    });

    /**
     * mini 翻页器
     */
    $overviewFilters.on('click', '.tiny-paging', function (e) {
        var $me = $(this);
        var $target = $(e.target);
        var min = parseInt($me.attr('data-min'), 10);
        var max = parseInt($me.attr('data-max'), 10);
        var curr = parseInt($me.attr('data-value'), 10);
        var disableClass = 'disable';
        var prevClass = 'prev-page';
        var nextClass = 'next-page';

        if ($target.hasClass(prevClass) && curr > min) { // 下一页
            curr -= 1;
            __updateFilterCache('pageNo', curr);
            $me.attr('data-value', curr);
            $me.find('.text em').text(curr);

            if (curr === min) {
                $target.addClass(disableClass);
            }
            $me.find('.' + nextClass).removeClass(disableClass);
        } else if ($target.hasClass(nextClass) && curr < max) { // 上一页
            curr += 1;
            __updateFilterCache('pageNo', curr);
            $me.attr('data-value', curr);
            $me.find('.text em').text(curr);

            if (curr === max) {
                $target.addClass(disableClass);
            }
            $me.find('.' + prevClass).removeClass(disableClass);
        }
    });

    /**
     * 过滤器 [展开] / [收起]
     */
    $filterOptions.on('click', '.dropdown-tool i', function (e) {
        var $me = $(this);
        var upClass = 'icon-arrow-up';
        var downClass = 'icon-arrow-down';

        if ($me.hasClass(upClass)) {
            $filterOptions.find('.filter-wrapper').css({
                'max-height': '0'
            }).fadeOut(1000);

            $filtersOverview.find('.city-val').text(filterCache.city ? filterCache.city : '不限');
            $filtersOverview.find('.salary-val').text(filterCache.expectSalary ? filterCache.expectSalary : '不限');

            var education = [];
            if (filterCache.education) {
                education.push(filterCache.education);
            }
            if (parseInt(filterCache.isEliteSchool, 10) === 1) {
                education.push('985/211');
            }
            if (parseInt(filterCache.isOverSea, 10) === 1) {
                education.push('海外');
            }
            $filtersOverview.find('.education-val').text(education.length > 0 ? education.join('、') : '不限');

            var experience = [];
            if (filterCache.workYear) {
                experience.push(filterCache.workYear);
            }
            if (parseInt(filterCache.isBigCompany, 10) === 1) {
                experience.push('名企经历');
            }
            $filtersOverview.find('.experience-val').text(experience.length > 0 ? experience.join('、') : '不限');

            $filtersOverview.css({
                'max-height': '22px'
            }).fadeIn(1000);
            $me.addClass(downClass).removeClass(upClass);
        } else if ($me.hasClass(downClass)) {
            $filterOptions.find('.filter-wrapper').css({
                'max-height': '800px'
            }).fadeIn(1000);
            $filtersOverview.fadeOut(1000);
            $me.addClass(upClass).removeClass(downClass);
        }
    });

    module.exports = {
        change: function (callback) {
            if (({}).toString.call(callback) !== '[object Function]') {
                throw new Error('"change" 方法参数必须是函数类型');
            }

            $filterOptions.on(changeEvt, callback);
        },
        tinyPaging: function (pageNo, pageCount) {
            pageNo = Math.min(pageNo, pageCount);

            var $tinyPaging = $overviewFilters.find('.tiny-paging');
            var prevClass = 'prev-page';
            var nextClass = 'next-page';
            var disableClass = 'disable';
            $tinyPaging.attr('data-value', pageNo);
            $tinyPaging.attr('data-min', 1);
            $tinyPaging.attr('data-max', pageCount);
            $tinyPaging.find('.text').html('<em>' + pageNo + '</em>/' + pageCount);

            if (pageNo <= 1) {
                $tinyPaging.find('.' + prevClass).addClass(disableClass);
            } else {
                $tinyPaging.find('.' + prevClass).removeClass(disableClass);
            }

            if (pageNo >= pageCount) {
                $tinyPaging.find('.' + nextClass).addClass(disableClass);
            } else if (pageNo > 0) {
                $tinyPaging.find('.' + nextClass).removeClass(disableClass);
            }
        },
        page: function (pageNo) {
            __updateFilterCache('pageNo', pageNo);
        },
        updateResultsCount: function (total) {
            var strCount = '';

            if (goodsInfo.lagouJiaCompany) {
                strCount = total > 500 ? '500+' : total;
            } else {
                strCount = total > 15 ? '多个' : total;
            }
            $overviewFilters.find('.result-info .count').text(strCount);
        },
        unfoldFiltersBox: function () {
            $filterOptions.find('.dropdown-tool i.icon-arrow-up').click();
        }
    };
});

/*!plus/modules/common/js/recommend.js*/
;/**
 * plus 人才推荐：相关搜索推荐
 *
 * @author fayipan@lagou.com
 */

define('plus/modules/common/js/recommend', ['require', 'exports', 'module'], function (require, exports, module) {
    var $container = null;
    var _toString = Object.prototype.toString;

    /**
     * 获取 sessionStorage 中的 city 值
     */
    function __getCity() {
        try {
            return window.sessionStorage.getItem('__plusFilterCity') || '不限';
        } catch (e) {
        }

        return '不限';
    }

    module.exports = {
        render: function (keyword, selector) {
            if ($container === null) {
                $container = $(selector || '#recommendQueries');
                /**
                 * 推荐搜索添加城市筛选值
                 */
                $container.on('click', '.rec-query', function (e) {
                    var $me = $(this);
                    var href = $me.attr('href');
                    $me.attr('href', href.replace(/city=([^&#]*)/ig, 'city=' + encodeURIComponent(__getCity())));
                });
            }

            $.ajax({
                url: 'https://relsearch.lagou.com/relquerybusiness',
                data: {
                    query: keyword
                },
                dataType: 'jsonp'
            }).done(function (data, textStatus, jqXHR) {
                var html = '';
                if (_toString.call(data) === '[object Array]' && data.length > 0) {
                    html += '<span class="label">您是不是要找:</span>';

                    for (var i = 0, len = data.length; i < len; i++) {
                        var url = GLOBAL_DOMAIN.ectx + '/search/result.htm?city=' + encodeURIComponent('不限') + '&keyword=' + encodeURIComponent(data[i]);
                        html += '<a class="rec-query" href="' + url + '" target="_blank">' + (data[i]).replace(/>/g, '&gt;').replace(/</g, '&lt;') + '</a>';
                    }
                }
                $container.html(html);
            });
        }
    }
});

/*!plus/modules/common/js/pagination.js*/
;/**
 * plus 人才推荐：搜索结果翻页
 *
 * @author fayipan@lagou.com
 */

define('plus/modules/common/js/pagination', ['require', 'exports', 'module'], function (require, exports, module) {
    var $container = null;

    module.exports = {
        /**
         * 搜索结果分页
         *
         * @param {integer} pageNo 当前页码
         * @param {integer} totalCount 最大页码
         * @param {integer} max 最多显示页码数，默认：15
         * @param {string}  selector 分页父级节点 CSS 选择器，默认：#pagination
         */
        render: function (pageNo, totalCount, max, selector) {
            if ($container === null) {
                $container = $(selector || '#pagination');
            }

            pageNo = parseInt(pageNo, 10);
            totalCount = parseInt(totalCount, 10);
            max = max || 15;

            if (isNaN(pageNo) || isNaN(totalCount)) {
                throw new Error('参数错误：请提供正确的 "pageNo", "totalCount" 参数');
            }

            if (pageNo > totalCount) {
                pageNo = Math.min(pageNo, totalCount);
            }

            if (totalCount <= 0) {
                $container.html('');
            } else if (totalCount === 1) {
                $container.html('<span class="current" data-page="1">1</span>');
            } else {
                var html = '<a href="javascript:;" data-page="1" data-lg-tj-id="27w0" data-lg-tj-no="0001">首页</a>';
                if (pageNo > 1) {
                    html += '<a href="javascript:;" data-page="' + (pageNo - 1) + '" data-lg-tj-id="27w0" data-lg-tj-no="' + ( pageNo > 10 ? '00' : '000' ) + (pageNo - 1) + '">上一页 </a>';
                } else {
                    html += '<span class="disabled" data-page="上一页">上一页 </span>'
                }

                var start = Math.max(1, pageNo - Math.floor(max / 2));
                var end = Math.min(start + max - 1, totalCount);
                for (var page = start; page <= end; page++) {
                    if (page === pageNo) {
                        html += '<span class="current" data-page="' + page + '">' + page + '</span>';
                    } else {
                        html += '<a href="javascript:;" data-page="' + page + '" data-lg-tj-id="27w0" data-lg-tj-no="' + ( page >= 10 ? '00' : '000' ) + page + '">' + page + '</a>';
                    }
                }

                if (pageNo < totalCount) {
                    html += '<a href="javascript:;" data-page="' + (pageNo + 1) + '" data-lg-tj-id="27w0" data-lg-tj-no="' + ( pageNo >= 9 ? '00' : '000' ) + (pageNo + 1) + '">下一页 </a>';
                } else {
                    html += '<span class="disabled" data-page="下一页">下一页 </span>';
                }
                html += '<a href="javascript:;" data-page="' + totalCount + '" data-lg-tj-id="27w0" data-lg-tj-no="' + ( totalCount > 9 ? '00' : '000' ) + totalCount + '">尾页</a>';

                $container.html(html);
            }
        }
    }
});

/*!plus/modules/common/js/proBox.js*/
;/**
 * plus 模块，弹框组件
 *
 * @author fayipan@lagou.com
 */

define('plus/modules/common/js/proBox', ['require', 'exports', 'module'], function (require, exports, module) {
    var selectorID = 'global-promote-box-wrapper';

    /**
     * 渲染全局弹框
     *
     * @param {string} strHtml 弹框内容 html 字符串
     * @param {string} id  可选，弹框 selector ID
     */
    function __render(strHtml, id) {
        id = (typeof id === 'string' && id) ? id : 'global-promote-box-wrapper';

        var $wrapper = $('#' + id);
        var $content = null;

        if ($wrapper.length === 0) {
            $wrapper = $('<div id="' + id + '">'
                + '<div class="fullscreen-cover">&nbsp;</div>'
                + '<div class="content-wrapper">'
                + '<i class="icon-close2"></i>'
                + '<div class="main-content">' + strHtml + '</div>'
                + '</div>'
                + '</div>');
            $wrapper.appendTo('body');

            $wrapper.on('click', '.icon-close2', function (e) {
                $wrapper.hide();
            });

            $wrapper.on('click', function (e) {
                if (!$.contains($content.get(0), e.target)) {
                    $wrapper.hide();
                }
            });

            $wrapper.on('scroll mousewheel', function (e) {
                e.preventDefault();
                e.stopPropagation();
            });
        } else {
            $wrapper.find('.main-content').html(strHtml);
        }

        $wrapper.show();

        $content = $wrapper.find('.content-wrapper');
        $content.css({
            left: Math.floor(($('body').width() - $content.width()) / 2)
        });
    }

    /**
     * 拉勾+ 弹框提醒
     */
    $(document).on('click', '.req-plus-service', function (e) {
        __render(
            '<p style="font-size:24px;">~~(&gt;_&lt;)~~TA的简历信息暂未开放</p>'
            + '<p style="margin:13px 0 0;font-size:16px;color:#999;line-height:30px;">升级为<em style="color:#00b38a;">拉勾+</em>用户即可查看!<br />还有千万简历在<em style="color:#00b38a;">拉勾+</em>等你哟~</p>'
            + '<a id="tryLagouPlus" style="margin:35px auto 0;width:136px;height:46px;line-height:46px;color:#fff;background-color:#00b38a;border-radius:3px;display:block;" href="https://activity.lagou.com/activity/dist/business/index.html#/talent/plus" target="_blank">了解拉勾+</a>',
            selectorID);
    });
    $(document).on('click', '#tryLagouPlus', function (e) {
        $('#' + selectorID).hide();
    });

    module.exports = {
        render: __render
    }
});

/*!plus/page/result-list/main.js*/
;
define('plus/page/result-list/main', ['require', 'exports', 'module', 'common/widgets/header/main', 'common/widgets/navigation/main', 'common/static/js/exposure', 'plus/modules/top-queries/main', 'plus/modules/result-list/main', 'dep/artTemplate/dist/template', 'plus/modules/filter-option/main', 'plus/modules/common/js/recommend', 'plus/modules/common/js/pagination', 'plus/modules/common/js/proBox'], function (require, exports, module) {
    /* 通用头部、导航 */
    require('common/widgets/header/main');
    require('common/widgets/navigation/main');
    var exposure = require('common/static/js/exposure').exposure;

    /* 页面主体交互 */
    require('plus/modules/top-queries/main');
    require('plus/modules/result-list/main');
    var template = require('dep/artTemplate/dist/template');
    var filter = require('plus/modules/filter-option/main');
    var recommend = require('plus/modules/common/js/recommend');
    var pagination = require('plus/modules/common/js/pagination');
    var promoteBox = require('plus/modules/common/js/proBox');
    var listTpl = "{{each result as resume index}}\n    <div class=\"result_list_item\" {{if resume.resumeRestrict}} req-plus-result-item {{/if}}\n         data-tj-exposure=\"on\"\n         data-lg-tj-type=\"pl\"\n         data-lg-tj-id=\"1I10\"\n         data-lg-tj-no=\"{{pageNo < 10 ? ('0' + pageNo) : pageNo}}{{index + 1 < 10 ? ('0' + (index + 1)) : (index + 1)}}\"\n         data-lg-tj-cid=\"{{resume.userid}}\">\n        <div class=\"item_header\">\n            {{if resume.workexperiences && resume.workexperiences.length > 0}}\n               <span class=\"position_name position_name_header\">{{#resume.workexperiences[0].positionname}}</span>{{if resume.workexperiences[0].positionname}} · {{/if}}<span class=\"source\">{{#resume.workexperiences[0].companyname}}</span>\n            {{/if}}\n\n            <div class=\"position_des\">\n                {{if resume.city}}\n                    <span class=\"city\">{{resume.city}} /</span>\n                {{/if}}\n\n                {{if resume.workYear}}\n                    <span class=\"experence\"> {{resume.workYear}}{{if resume.workYear !== '应届毕业生'}}工作经验{{/if}} /</span>\n                {{/if}}\n\n                {{if resume.highesteducation}}\n                    <span class=\"education\"> {{resume.highesteducation}} /</span>\n                {{/if}}\n\n                {{if resume.sex}}\n                    <span class=\"sex\"> {{resume.sex}} /</span>\n                {{/if}}\n\n                {{resume.laestlogintime}}登录\n            </div>\n\n            <span class=\"chat_target clearfix\">\n                最近登录：\n                {{if resume.laestlogintime == '在线'}}\n                    <span class=\"online-tag\">{{resume.laestlogintime}}</span>\n                {{else}}\n                    {{resume.laestlogintime}}\n                {{/if}}\n            </span>\n\n            {{if resume.dealStatus === 'DEAL' || resume.dealStatus === 'DELIVER'}}\n                <i class=\"vertical-bar clearfix\"></i>\n                <span class=\"chat_target clearfix bar-pre\">此人已发简历</span>\n            {{/if}}\n        </div>\n\n        <div class=\"item_body clearfix\">\n            <div class=\"avatar fl\">\n                <a class=\"stop-propagation\" href=\"/search/resume/{{resume.resumeKey}}.htm?outerPositionId={{positionInfo.outerPositionId}}\" target=\"_blank\">\n                    {{if resume.headpic && resume.headpic !== headpic}}\n                        <img src=\"https://www.lgstatic.com/thumbnail_100x100/{{resume.headpic}}\" alt=\"用户头像\" />\n                    {{else}}\n                        <div class=\"bg_{{resume.userid % 4}}\">{{resume.nickName.substr(0, 1).toUpperCase()}}</div>\n                    {{/if}}\n                </a>\n            </div>\n\n            <div class=\"avatar_des clearfix\">\n                <div class=\"user_infos\">\n                    {{if resume.resumeRestrict}}\n                        <h4 class=\"user_name req-plus-name\">{{resume.nickName.substring(0,1).toUpperCase()}}** <span class=\"plus-tag\"><span class=\"smaller-font\">PLUS</span></span></h4>\n                    {{else}}\n                        <h4 class=\"user_name\">{{resume.nickName}}</h4>\n                    {{/if}}\n                    {{if resume.oneWord}}\n                        <span class=\"user_expr_short spreadIn {{if resume.resumeRestrict}} disable-more-icon {{/if}}\">{{resume.oneWord}}</span>\n                    {{else}}\n                        <span class=\"user_expr_short spreadIn {{if resume.resumeRestrict}} disable-more-icon {{/if}}\">Ta还木有一句话介绍哦～</span>\n                    {{/if}}\n                </div>\n\n                {{if resume.resumeRestrict}}\n                    <span class=\"req-plus-service btn\">了解TA</span>\n                {{else}}\n                    <div class=\"chat_btn\">\n                        {{if openedSessionMap.hasOwnProperty(resume.userid)}}\n                            <a class=\"btn btn_green chat-continue\"\n                               data-lg-tj-id=\"19bs\"\n                               data-lg-tj-no=\"{{pageNo < 10 ? ('0' + pageNo) : pageNo}}{{index + 1 < 10 ? ('0' + (index + 1)) : (index + 1)}}\"\n                               data-lg-tj-cid=\"{{resume.userid}}\"\n                               data-lg-tj-type=\"pl\"\n                               data-tj-exposure=\"on\"\n\n                               href=\"/im/chat/index.htm?activeId={{resume.userid}}\"\n                               data-cuserid=\"{{resume.userid}}\"\n                               data-resumeKey=\"{{resume.resumeKey}}\"\n                               data-cname=\"{{resume.name}}\" target=\"_blank\">继续聊聊</a>\n                        {{else}}\n                            <a class=\"btn btn_green add-chat-list\"\n                               data-lg-tj-id=\"1Np0\"\n                               data-lg-tj-no=\"{{pageNo < 10 ? ('0' + pageNo) : pageNo}}{{index + 1 < 10 ? ('0' + (index + 1)) : (index + 1)}}\"\n                               data-lg-tj-cid=\"{{resume.userid}}\"\n                               data-lg-tj-type=\"pl\"\n                               data-tj-exposure=\"on\"\n\n                               href=\"javascript:void(0);\"\n                               data-cuserid=\"{{resume.userid}}\"\n                               data-resumeKey=\"{{resume.resumeKey}}\"\n                               data-cname=\"{{resume.name}}\"\n                               data-type=\"1\"\n                               data-positioninfo-outerpositionid=\"{{positionInfo.outerPositionId}}\"\n                               data-positioninfo-positionname=\"{{positionInfo.positionName}}\"\n                               data-positioninfo-positionid=\"{{positionInfo.positionId}}\">和TA聊聊</a>\n                        {{/if}}\n                    </div>\n                    {{if isGrayPhoneCallUser}}\n                        {{if resume.phoneCallStatus}}\n                            <div class=\"call-btn\">\n                                {{if resume.phoneCallStatus === 'phone_disabled'}}\n                                    <a href=\"javascript:void(0);\" class=\"btn call-ta phone-disabled\"\n                                        data-lg-tj-id=\"19bt\"\n                                        data-lg-tj-no=\"{{pageNo < 10 ? ('0' + pageNo) : pageNo}}{{index + 1 < 10 ? ('0' + (index + 1)) : (index + 1)}}\"\n                                        data-lg-tj-cid=\"{{resume.userid}}\"\n                                        data-lg-tj-type=\"pl\"\n                                        data-tj-exposure=\"on\"\n\n                                        data-resumeKey=\"{{resume.resumeKey}}\"\n                                        data-cuserid=\"{{resume.userid}}\">\n                                        <i class=\"icon-call-1\"></i>&ensp;电话呼叫\n                                    </a>\n                                {{ else if resume.phoneCallStatus === 'phone_call'}}\n                                    <a href=\"javascript:void(0);\" class=\"btn btn_green call-ta phone-call\"\n                                        data-lg-tj-id=\"19bu\"\n                                        data-lg-tj-no=\"{{pageNo < 10 ? ('0' + pageNo) : pageNo}}{{index + 1 < 10 ? ('0' + (index + 1)) : (index + 1)}}\"\n                                        data-lg-tj-cid=\"{{resume.userid}}\"\n                                        data-lg-tj-type=\"pl\"\n                                        data-tj-exposure=\"on\"\n\n                                        data-resumeKey=\"{{resume.resumeKey}}\"\n                                        data-cuserid=\"{{resume.userid}}\">\n                                        <i class=\"icon-call-1\"></i>&ensp;电话呼叫\n                                    </a>\n                                {{ else if resume.phoneCallStatus === 'phone_call_again'}}\n                                    <a href=\"javascript:void(0);\" class=\"btn btn_green call-ta phone-call-again\"\n                                        data-lg-tj-id=\"19bv\"\n                                        data-lg-tj-no=\"{{pageNo < 10 ? ('0' + pageNo) : pageNo}}{{index + 1 < 10 ? ('0' + (index + 1)) : (index + 1)}}\"\n                                        data-lg-tj-cid=\"{{resume.userid}}\"\n                                        data-lg-tj-type=\"pl\"\n                                        data-tj-exposure=\"on\"\n\n                                        data-resumeKey=\"{{resume.resumeKey}}\"\n                                        data-cuserid=\"{{resume.userid}}\">\n                                        <i class=\"icon-call-1\"></i>&ensp;再次呼叫\n                                    </a>\n                                {{/if}}\n                            </div>\n                        {{/if}}\n                    {{/if}}\n\n                {{/if}}\n            </div>\n        {{if !resume.resumeRestrict}}\n            <div class=\"info\">\n                {{if resume.expectJob}}\n                    <dl class=\"info_item clearfix\">\n                        <dt class=\"fl\">期望工作</dt>\n                        <dd class=\"fl\">\n                            {{if resume.expectJob.positionName}}\n                                <span class=\"info_position\">{{#resume.expectJob.positionName}}</span>\n                            {{/if}}\n\n                            {{if resume.expectJob.city}}\n                                {{if resume.expectJob.positionName}}\n                                    /\n                                {{/if}}\n                                <span class=\"info_city\">{{resume.expectJob.city}}</span>\n                            {{/if}}\n\n                            {{if resume.expectJob.salarys}}\n                                {{if resume.expectJob.positionName || resume.expectJob.city}}\n                                    /\n                                {{/if}}\n                                <span class=\"info_salary\">{{resume.expectJob.salarys}}</span>\n                            {{/if}}\n                        </dd>\n                    </dl>\n                {{/if}}\n\n                {{if resume.workexperiences && resume.workexperiences.length > 0}}\n                    <dl class=\"info_item clearfix\">\n                        <dt class=\"fl\">工作经历</dt>\n                        <dd class=\"fl\">\n                            {{each resume.workexperiences as workExp i}}\n                                {{if i <= 2}}\n                                    <div class=\"work_experence_container clearfix\">\n                                        <div class=\"exper_time\">{{workExp.startdate}}-{{workExp.enddate}}</div>\n                                        <div class=\"info-position-container\">\n                                            <div>\n                                                <span class=\"company\">{{#workExp.companyname}}</span> {{if workExp.companyname && workExp.positionname}} ·  {{/if}}<span class=\"position\">{{#workExp.positionname}}</span>\n                                            </div>\n                                            <div class=\"work_experence content_text\">{{#workExp.workcontent}}</div>\n                                        </div>\n                                    </div>\n                                {{/if}}\n                            {{/each}}\n                        </dd>\n                    </dl>\n                {{/if}}\n\n                {{if resume.educationexperiences && resume.educationexperiences.length > 0}}\n                    <dl class=\"info_item clearfix\">\n                        <dt class=\"fl\">教育经历</dt>\n                        <dd class=\"fl\">\n                            {{each resume.educationexperiences as eduExp j}}\n                                {{if j <= 1}}\n                                    <div {{if j===0}} class=\"positions-item\" {{/if}}>\n                                        {{if eduExp.enddate}}\n                                            <span class=\"graduate_date\">{{eduExp.enddate}}年毕业</span>\n                                        {{/if}}\n\n                                        {{if eduExp.education}}\n                                            <span class=\"education_rank\">{{eduExp.education}}</span> ·\n                                        {{/if}}\n\n                                        {{if eduExp.schoolname}}\n                                            <span class=\"collage\">{{#eduExp.schoolname}}</span> ·\n                                        {{/if}}\n\n                                        {{if eduExp.professional}}\n                                            <span class=\"major\">{{eduExp.professional}}</span>\n                                        {{/if}}\n                                    </div>\n                                {{/if}}\n                            {{/each}}\n                        </dd>\n                        <dd class=\"fr\">\n                            <a class=\"more-info stop-propagation\"\n                               href=\"/search/resume/{{resume.resumeKey}}.htm?outerPositionId={{positionInfo.outerPositionId}}\"\n                               target=\"_blank\"\n                               data-lg-tj-id=\"19bm\"\n                               {{if pageNo < 10}}\n                                  {{if index < 9}}\n                                      data-lg-tj-no=\"0{{pageNo}}0{{index+1}}\"\n                                  {{else}}\n                                      data-lg-tj-no=\"0{{pageNo}}{{index+1}}\"\n                                  {{/if}}\n                               {{else}}\n                                  {{if index < 9}}\n                                      data-lg-tj-no=\"{{pageNo}}0{{index+1}}\"\n                                  {{else}}\n                                      data-lg-tj-no=\"{{pageNo}}{{index+1}}\"\n                                  {{/if}}\n                               {{/if}}\n                               data-lg-tj-cid=\"{{resume.userid}}\">查看更多 <i class=\"icon-arrow-right\"></i></a>\n                        </dd>\n                    </dl>\n                {{/if}}\n            </div>\n        {{/if}}\n        </div>\n    </div>\n{{/each}}\n";
    var isGrayPhoneCallUser = $('#isGrayPhoneCallUser').val() === 'true' ? true : false;
    var cache = { // 记录交互中的中间状态
        scrollTop: false // 点击底部翻页，自动滚到顶部
    };
    var initialState = window.initialState || {};

    var $listDOM = $('.result-list');
    var $noResultDOM = $('.no_result');
    var $pagination = $('#pagination');
    var $globalSearchKeyword = $('.global-search-box input[name=keyword]');
    var userCreateTime = parseInt($('#userCreateTime').val(), 10) || 0;

    function _showInviteTips(selector, userCreateTime) {
        var $chatBtn = $(selector);
        var userTimeBoundary = (new Date('2017/06/10')).getTime(); // 1497024000000
        var validTimePoint = (new Date('2017/08/10')).getTime(); // 两个月之后不再显示提示文案
        var now = Date.now();

        if (userCreateTime > userTimeBoundary) return; // 2017-6-10及之后的新B端用户不显示提示
        if (now < validTimePoint) {
            // 2017-8-10之前
            if (window.localStorage.getItem('hideInviteTips') !== 'true' &&
                $chatBtn.length > 0 &&
                $chatBtn.parent('div').find('.invite-tips').length === 0) {

                $chatBtn.parent('div').prepend('<div class="invite-tips">职位邀请整合到这里了<br />点击试试吧～</div>');
            }
        } else {
            // 2017-8-10之后
            if (window.localStorage.getItem('hideInviteTips') !== null) {
                //storage.getItem(keyName). If the key does not exist, null is returned
                window.localStorage.removeItem('hideInviteTips');
            }
        }

    }

    _showInviteTips('.add-chat-list:first', userCreateTime);

    function __obj2URLparams(obj) {
        var params = [];

        if (({}).toString.call(obj) !== '[object Object]') {
            return obj;
        }

        for (var key in obj) {
            if (!obj.hasOwnProperty(key)) {
                continue;
            }
            params.push(key + '=' + encodeURIComponent(obj[key]));
        }

        return params.join('&');
    }

    /**
     * 点击和ta聊聊，邀约提示消失
     */
    $('.main-content').on('click', '.chat_btn', function (e) {
        var $this = $(this);
        var $inviteTips = $this.find('.invite-tips');
        if ($inviteTips.length > 0) {
            $inviteTips.remove();
            window.localStorage.setItem('hideInviteTips', 'true')
        }
    })

    /**
     * 筛选条件变更
     */
    filter.change(function (e, filters) {
        window.__async_dl = window.location.href.replace(/(\?.*|)$/, '?' + __obj2URLparams(filters)); // 异步操作点击日志

        $.ajax({
            url: GLOBAL_DOMAIN.ectx + '/search/result.json',
            data: filters,
            dataType: 'json'
        }).done(function (data, textStatus, jqXHR) {
            var state = parseInt(data.state, 10);

            if (state === 1) {
                var pageData = data.content.data.result;
                var searchResult = pageData.searchResult;
                var pageCount = Math.ceil(searchResult.totalCount / searchResult.pageSize);

                $listDOM.html(template.compile(listTpl)({
                    remainTimes: pageData.remainTimes,
                    openedSessionMap: pageData.openedSessionMap,
                    positionInfo: pageData.positionInfo || {},
                    pageSize: searchResult.pageSize,
                    pageNo: searchResult.pageNo,
                    pageCount: pageCount,
                    result: searchResult.result,
                    headpic: 'https://' + GLOBAL_CDN_DOMAIN + '/mds/static/plus/modules/result-list/img/user_pic_dbad145.jpg',
                    GLOBAL_DOMAIN: GLOBAL_DOMAIN,
                    isGrayPhoneCallUser: isGrayPhoneCallUser
                }));

                filter.tinyPaging(searchResult.pageNo, pageCount);
                filter.updateResultsCount(searchResult.totalCount);
                pagination.render(searchResult.pageNo, pageCount);
                _showInviteTips('.add-chat-list:first', userCreateTime);

                if (pageCount > 0) {
                    $listDOM.show();
                    $noResultDOM.hide();
                } else {
                    $listDOM.hide();
                    $noResultDOM.show();
                }

                if (filters.keyword) {
                    recommend.render(filters.keyword); // 根据 keyword 推荐相关搜索
                    $globalSearchKeyword.val(filters.keyword); // 填充全局搜索框
                }

                if (searchResult.pageNo > 1) { // 翻页后即非搜索页首页，筛选器自动收起
                    filter.unfoldFiltersBox();
                }

                if (cache.scrollTop === true) { // 底部翻页自动滚到顶部
                    $('html, body').animate({
                        scrollTop: 0
                    });
                    cache.scrollTop = false;
                }

                var search = this.url.split('?')[1]; // 更新导航栏 url 地址，兼容通用搜索框
                window.history.pushState({
                    type: '__plusFilterChange'
                }, initialState.lagoutitle, window.location.href.replace(/(\?.*|)$/, '?' + search));
                exposure();
            }
        });
    });

    /**
     * 处理浏览器 前进 / 后退 按钮
     */
    $(window).on('popstate', function (e) {
        if (document.location.href === document.referrer) { // 部分浏览器（360浏览器7.1、ie11）会重复触发，导致循环
            return;
        }

        document.location = document.location.href;
    });

    /**
     * 分页交互
     */
    $pagination.on('click', 'a', function (e) {
        cache.scrollTop = true;
        filter.page($(this).attr('data-page'));
    });

    /**
     * 初始化渲染分页
     */
    if (initialState.result) {
        var result = initialState.result;
        var pageNo = result.pageNo;
        var totalCount = Math.ceil(result.totalCount / result.pageSize);
        if (pageNo > 0 && totalCount >= pageNo) {
            pagination.render(pageNo, totalCount);
        }
    }

    /**
     * 翻页后即非搜索页首页，筛选器自动收起
     */
    if (initialState.params && initialState.params.pageNo && initialState.params.pageNo > 1) {
        filter.unfoldFiltersBox();
    }

    /**
     * 初始化根据 keyword 推荐相关搜索，填充全局搜索框
     */
    if (initialState.params && initialState.params.keyword) {
        recommend.render(initialState.params.keyword); // 初始化根据 keyword 推荐相关搜索
        $globalSearchKeyword.val(initialState.params.keyword); // 填充全局搜索框
    }
});