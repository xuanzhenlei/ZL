/**
 * Created by zhengyang@starmerx.com on 17-1-5.
 */
var Operate = function () {
    var $table = $('#boot_table');

    var addFn = function () {
        //新增
        $(document).on('click', '#table_edit_new', function (e) {
            e.preventDefault();
            $('#modal_default .alert').hide();
            $('#form_default').clearForm();
            $('#form_default #key_id').data('index', '');
            $('#form_default #is_staff0').prop('checked', true);
            $('#modal_default').modal('show');
        });
    }, editFn = function (e, value, row, index) {
        //修改
        e.preventDefault();
        $('#modal_default .alert').hide();
        $('#form_default').clearForm();
        $('#form_default #key_id').val(row.id).data('index', index);
        $('#form_default #parent_tree_id').val(row.organize_id);
        $('#form_default #username').val(row.username);
        $('#form_default #email').val(row.email);
        $('#form_default #position').val(row.position);
        $('#form_default input[name="is_staff"][value='+row.is_staff+']').prop('checked', true);
        $('#modal_default').modal('show');
    };

    var operateEvents = {
        'click .edit': function (e, value, row, index) {
            return editFn(e, value,row,index);
        },
        'click .remove': function (e, value, row, index) {
            return delFn(e, value,row,index);
        }
    };

    var saveFn = function () {
        $('#form_default')
            .bootstrapValidator({
            feedbackIcons: {
                valid: 'glyphicon glyphicon-ok',
                invalid: 'glyphicon glyphicon-remove',
                validating: 'glyphicon glyphicon-refresh'
            },
        })
        .on('success.form.bv', function(e) {
            // Prevent form submission
            e.preventDefault();
            var $form = $(e.target);
            $form.ajaxSubmit({
                    "url": PUB_URL.saveUrl,
                    "type": 'POST',
                    "dataType": 'json',
                    "beforeSubmit": function () {
                    },
                    "success": function (data) {
                        var new_data = data.data;
                        if ($form.find('#key_id').val()){
                            var index = $form.find('#key_id').data('index');
                            p_bootstrap_table.updateRow(index, new_data);
                        }else{
                            p_bootstrap_table.addRow(new_data);
                        }
                        p_bootstrap_table.modalAlert('success', data.msg);
                        setTimeout(function () {$('#modal_default').modal('hide')}, 1000);
                    },
                    "error": function (xhr, status, error) {
                        p_bootstrap_table.modalAlert('danger');
                    },
                    "complete": function () {
                        $form.bootstrapValidator('disableSubmitButtons', false);    //提交按钮释放
                        $form.data("bootstrapValidator").resetForm();  //重置验证
                    }
                });
        });
    };

    //删除
    var delFn = function (e, value,row,index) {
        e.preventDefault();
        if (confirm("确认删除该条记录？") == false) {
            return false;
        }
        var params = {};
        params['key_id'] = value;
        $.ajax({
            "url": PUB_URL.delUrl,
            "data": params,
            "type": 'POST',
            "dataType": 'json',
            "beforeSubmit": function () {
            },
            "success": function (data) {
                p_bootstrap_table.modalOnlyAlert('success', '删除成功！');
                p_bootstrap_table.delRow(row);
            },
            "error": function (xhr, status, error) {
                p_bootstrap_table.modalOnlyAlert('danger', '删除失败，请联系研发！');
            }
        });
    };


    return {
        init: function () {
             addFn(); saveFn();
        },
        operateEvents: operateEvents
    }
}();
jQuery(document).ready(function () {
    Operate.init();
});