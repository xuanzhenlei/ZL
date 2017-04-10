/**
 * Created by zhengyang@starmerx.com on 17-1-5.
 */
var Operate = function () {
    var $table = $('#boot_table');

    // 表格插入数据
    var addRow = function (row) {
            $table.bootstrapTable('prepend', {     // 在数据头部加行
                'organize_name': row.organize_name,
                'level': row.level,
                'parent_tree_name': row.parent_tree_name,
                'id': row.id
            });
            $table.bootstrapTable('scrollTo', 'top');    //  滚动条回到表格头部， 新增数据的时候使用，可以不用。
    };


    var operateEvents = {
        'click .edit': function (e, value, row, index) {
            $table.bootstrapTable('updateRow', {        // 更新行
                'index': index,
                'row': {     // 在数据头部加行
                    'organize_name': '研发部',
                    'level': '3',
                    'parent_tree_name': '总监室',
                    'id': '108'
                }
            });
        },
        'click .remove': function (e, value, row, index) {
            $table.bootstrapTable('remove', {
                field: 'id',
                values: [row.id]
            });
        }
    };

    var saveOrganize = function () {
        $('#form_default')
            .bootstrapValidator({
            message: 'This value is not valid',
            feedbackIcons: {
                valid: 'glyphicon glyphicon-ok',
                invalid: 'glyphicon glyphicon-remove',
                validating: 'glyphicon glyphicon-refresh'
            },
            // fields: {
            //     username: {
            //         validators: {
            //             notEmpty: {
            //                 message: 'The username is required'
            //             }
            //         }
            //     },
            // },
        })
        .on('success.form.bv', function(e) {
            // Prevent form submission
            e.preventDefault();
            var $form = $(e.target);
            $form.ajaxSubmit({
                    "url": PUB_URL.saveOrganize,
                    "type": 'POST',
                    "dataType": 'json',
                    "beforeSubmit": function () {
                    },
                    "success": function (data) {
                        alert('保存成功！');
                        var new_data = data.data;
                        addRow(new_data);
                        $('#myModal').modal('hide');
                    },
                    "error": function (xhr, status, error) {
                        $form.bootstrapValidator('disableSubmitButtons', false);
                    }
                });
        });
    };


    return {
        init: function () {
             saveOrganize();
        },
        operateEvents: operateEvents
    }
}();
jQuery(document).ready(function () {
    Operate.init()
});