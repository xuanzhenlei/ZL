/**
 * Created by zhengyang@starmerx.com on 17-1-5.
 */
var Operate = function () {
    //Enable iCheck plugin for checkboxes
    //iCheck for checkbox and radio inputs
    var iCheckInit = function () {
        $('.mailbox-messages input[type="checkbox"]').iCheck({
            checkboxClass: 'icheckbox_flat-blue',
            radioClass: 'iradio_flat-blue'
        });
    };

    //Enable check and uncheck all functionality
    $(".checkbox-toggle").click(function () {
        var clicks = $(this).data('clicks');
        if (clicks) {
            //Uncheck all checkboxes
            $(".mailbox-messages input[type='checkbox']").iCheck("uncheck");
        } else {
            //Check all checkboxes
            $(".mailbox-messages input[type='checkbox']").iCheck("check");
        }
        $(this).data("clicks", !clicks);
    });

    var iCheckEvent = function () {
        $('section').on('ifClicked', '.mailbox-messages input[type="checkbox"]', function () {
            var j0 = $(this).data('j0'),
                    j1 = $(this).data('j1'),
                    v = $(this).val();
                var $box = $(this).parents('.mailbox-messages:first');
            if ($(this).prop('checked')){  // 从有到取消
                $box.find("input[type='checkbox'][data-j0="+v+"]").iCheck("uncheck");
                $box.find("input[type='checkbox'][data-j1="+v+"]").iCheck("uncheck");
            }else{ // 从没有到选中
                $box.find("input[type='checkbox'][value="+j0+"]").iCheck("check");
                $box.find("input[type='checkbox'][value="+j1+"]").iCheck("check");
                $box.find("input[type='checkbox'][data-j0="+v+"]").iCheck("check");
                $box.find("input[type='checkbox'][data-j1="+v+"]").iCheck("check");
            }
        })

    };

    var checkBoxVal = function () {
        // 获取被选中checkbox 的 value   value一般就是对应数据id的值。
        var boxs = $('.mailbox-messages input[type="checkbox"]');
        var idList = [];
        boxs.each(function () {
            if ($(this).prop('checked')) {
                var v = $(this).val();
                v && (v != 'on') && idList.push($(this).val());
            }
        });
        return idList;
    };

    var select2Init = function () {
        // select2 初始化
        $('.select2').select2();
    };

    var saveFn = function () {
        // 保存用户权限
        $('#form_default')
            .bootstrapValidator({
                feedbackIcons: {
                    valid: 'glyphicon glyphicon-ok',
                    invalid: 'glyphicon glyphicon-remove',
                    validating: 'glyphicon glyphicon-refresh'
                }
            })
            .on('success.form.bv', function (e) {
                // Prevent form submission
                e.preventDefault();
                var $form = $(e.target);
                var params = {};
                var jurisdiction = checkBoxVal();
                params['jurisdictions'] = jurisdiction.join(',');
                $form.ajaxSubmit({
                    "url": PUB_URL.saveUrl,
                    "type": 'POST',
                    "data": params,
                    "dataType": 'json',
                    "beforeSubmit": function () {
                    },
                    "success": function (data) {
                        $form.find('#user_id option:selected').data('jurisdiction', params['jurisdictions']);
                        p_bootstrap_table.modalOnlyAlert('success', data.msg);
                    },
                    "error": function (xhr, status, error) {
                        p_bootstrap_table.modalOnlyAlert('danger', '保存失败，请联系研发！');
                    },
                    "complete": function () {
                        $form.bootstrapValidator('disableSubmitButtons', false);    //提交按钮释放
                        $form.data("bootstrapValidator").resetForm();  //重置验证
                    }
                });
            });
    };

    var userCheckInit = function () {
        // 用户权限在面板的初始化。 已有的权限选中，没有权限不选中。
        $('section').on('change', '#user_id', function () {
            $(".mailbox-messages input[type='checkbox']").iCheck("uncheck");  // 取消所有checkbox
            var $option = $(this).find('option:selected');
            var jurisdiction = $option.data('jurisdiction').split(',');
            $.each(jurisdiction, function () {
                $(".mailbox-messages input[type='checkbox'][value="+this+"]").iCheck("check");
            });

            // 核实信息
            var email = $option.data('email'),
                organize = $option.data('organize');
            var html = '<p>部门： '+ organize +'</p>' +
                        '<p>邮箱： '+ email +'</p>';
            $('#hedui').html(html);
        });

    };

    return {
        init: function () {
            iCheckInit();
            iCheckEvent();
            select2Init();
            saveFn();
            userCheckInit();
        },
    }
}();
jQuery(document).ready(function () {
    Operate.init();
});