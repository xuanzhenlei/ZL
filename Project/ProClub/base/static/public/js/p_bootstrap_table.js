/**
 * Created by zhengyang@starmerx.com on 17-1-8.
 */
var p_bootstrap_table = function () {
    var $table = $('#boot_table'); // 默认的数据表格
    
    // 工具栏搜索参数
    var submitFilter = function () {
        var aoDataParam = {};
        var toolbar = $('#toolbar');
        // get all typeable inputs
        $('textarea.toolbar-filter, select.toolbar-filter, input.toolbar-filter:not([type="radio"],[type="checkbox"])', toolbar).each(function () {
            ($(this).val()) && (aoDataParam[$(this).attr("name")] = $(this).val());
        });
        // get all radio buttons
        $('input.toolbar-filter[type="radio"]:checked', toolbar).each(function () {
            ($(this).val()) && (aoDataParam[$(this).attr("name")] = $(this).val());
        });
        return aoDataParam;
    };
    // 表单提交 结果提示， alert在表的modal中。
    var modalAlert = function (type, title, contxt) {
        title = title || '';
        // contxt = contxt || '';
        var type_class = '.alert-' + type;
        if (title) {
            $('#modal_default ' + type_class).find('span.message').html(title);
        }
        $('#modal_default ' + type_class).show();
    };
    // ajax执行结果提示， alert在单独的modal中
    var modalOnlyAlert = function (type, title, contxt) {
        $('#modal_alert .alert').hide();   //先隐藏所有alert

        title = title || '';    // title 默认为空
        var type_class = '.alert-' + type;
        if (title) {   // 如果title为空， 就使用html中的默认提示。
            $('#modal_alert ' + type_class).find('span.message').html(title);
        }
        $('#modal_alert ' + type_class).show();  // 显示选的类型的alert
        $('#modal_alert').modal('show');    // 显示模态框
        setTimeout(function () {
            $('#modal_alert').modal('hide');
        }, 2000)
    };
    
    // 表格插入数据
    var addRow = function (row) {
            $table.bootstrapTable('prepend', row);
            $table.bootstrapTable('scrollTo', 'top');    //  滚动条回到表格头部， 新增数据的时候使用，可以不用。
    };
    // 更新行
    var updateRow = function (index, row) {
        $table.bootstrapTable('updateRow', {        
                'index': index,
                'row': row
            });
    };
    // 删除行
    var delRow = function (row) {
        $table.bootstrapTable('remove', {
                field: 'id',
                values: [row.id]
            });
    };

    return {
        init: function () {
        },
        submitFilter: submitFilter,     // 自动加载工具栏里的搜索参数
        modalAlert: modalAlert,         // 表单modal里控制信息提示
        modalOnlyAlert: modalOnlyAlert, // 单独modal里的信息提示
        addRow: addRow,                 // 表格前端进行增加行的处理
        updateRow: updateRow,           // 表格更新行的处理
        delRow: delRow                  // 表格删除行的处理
    }
}();
jQuery(document).ready(function () {
    p_bootstrap_table.init()
});
