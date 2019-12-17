
function initSelect2() {
    $('.js-example-basic-multiple').select2({
        theme: "classic",
    });
};

$(document).ready(function () {
    initSelect2();
});

function httpreq(url, data, callback) {
    $.ajax({
        type: "POST",
        url: url,
        data: data,
        success: function (result) {
            callback(json_decode(result))
        }
    })
};

function json_decode(str) {
    var obj = JSON.parse(str)
    return obj
};

function json_encode(obj) {
    var str = JSON.stringify(obj);
    return str
};

function layer(msg) {
    alert(msg)
};


    var login_app = new Vue({
    el: '#login_app',
    methods: {
        click_login_btn: function () {
            httpreq(
                '/user/login_commit',
                $("#form_id").serialize(),
                function (resp) {
                    if (resp.errno === 0) {
                        //登录成功
                        window.location.href = '/';
                    } else {
                        //登录失败
                        layer(resp.errmsg)
                    }
                }
            );
        },
    },
});

var jmp_apply_app = new Vue({
    el: '#jmp_apply_app',
    methods: {
        //获取所有选中的资产信息（json）
        refresh_asset_list: function () {
            var asset_list = [];
            $("#assets option:selected").each(function () {
                var id = $(this).val();
                var hostname = $(this).attr('hostname');
                var ip = $(this).attr('ip');
                var text = $(this).attr('text');
                asset_list.push({
                    'id': id,
                    'hostname': hostname,
                    'ip': ip,
                    'text': text,
                });
            });
            var asset_list_str = json_encode(asset_list);
            $("#asset_list").val(asset_list_str);
        },
        refresh_sys_user_list: function () {
            var sys_user_list = [];
            $("#sys_users option:selected").each(function () {
                var id = $(this).val();
                var sys_user_name = $(this).attr('sys_user_name');
                sys_user_list.push({
                    'id': id,
                    'sys_user_name': sys_user_name,
                });
            });
            var sys_user_list_str = json_encode(sys_user_list);
            $("#sys_user_list").val(sys_user_list_str);
        },
        click_submit_btn: function () {

            this.refresh_asset_list();
            this.refresh_sys_user_list();

            httpreq(
                '/jmp_apply/submit',
                $("#form_id").serialize(),
                function (resp) {
                    if (resp.errno === 0) {
                        //提交成功
                        layer('提交成功');
                        window.location.href = '/jmp_apply/my_apply';
                    } else {
                        //提交失败
                        layer(resp.errmsg);
                    }
                }
            );

            return false;
        },
        click_reject_btn: function(order_id) {
            if (confirm('确认拒绝吗?')) {
                httpreq(
                    '/jmp_apply/reject',
                    {'order_id' : order_id},
                    function(resp) {
                        if (resp.errno === 0) {
                            layer('已拒绝');
                            window.location.href = '/jmp_apply/my_approval';
                        } else {
                            layer(resp.errmsg);
                            window.location.reload();
                        }
                    }
                );
            }
        },
        click_agree_btn: function(order_id) {
            if (confirm('点击同意后，会自动在jumpserver中创建授权规则，确认同意吗？')) {
                httpreq(
                    '/jmp_apply/agree',
                    {'order_id':order_id},
                    function(resp) {
                        if (resp.errno === 0) {
                            layer('已同意');
                            window.location.href = '/jmp_apply/my_approval';
                        } else {
                            layer('审批失败:' + resp.errmsg);
                            window.location.reload();
                        }
                    }
                );
            }
        },
    },
});

function click_order(order_id) {
    if (confirm('确认删除？')) {
                httpreq(
                     '/jmp_apply/delete',
                     {'order_id' : order_id},
                     function (resp) {
                         if (resp.errno === 0) {
                             //删除成功
                             layer('删除成功');
                         } else {
                             //删除失败
                             layer('删除失败:' + resp.errmsg);
                         }
                         window.location.reload();
                     }
                );
    }
    return false;
};

function mouseenter_on_td(tdId) {
    console.log('mouseenter_on_td');
    var full = $('#' + tdId).attr('full');
    $('#' + tdId).text(full);
};

function mouseleave_on_td(tdId) {
    console.log('mouseleave_on_td');
    var short = $('#' + tdId).attr('short');
    $("#" + tdId).text(short);
};
