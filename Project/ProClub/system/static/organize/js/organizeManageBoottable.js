/**
 * Created by zhengyang@starmerx on 17-1-5.
 */
var BootstrapTables = function () {
    var e = function () {
        var e = $("#boot_table");
        e.bootstrapTable({
            striped: true,   //隔行变色
            // sortname: // 排序名
            // sortOrder: asc //排序方式
            pagination: true, //底部分页条
            pageList: [20, 50, 100, 200, 500], //页面条数
            height: 500, //表格高度
            undefinedText: '', //当数据为 '', undefined 时显示的字符
            sidePagination: 'server',
            // ajaxOptions: {}, //额外参数应该不需要，默认json格式
            url: PUB_URL.organizeManage,
            method: 'post',
            contentType: 'application/x-www-form-urlencoded',  //默认是 json 也可以，不过后台需要单独处理获取
            queryParams: function (params) {
                // params.   //自定义参数
                var toolbar_params = p_bootstrap_table.submitFilter();
                $.extend(params, toolbar_params);
                return params;
            },
            columns: [
                {
                    field: 'state',
                    checkbox: true,

                }, {
                    field: 'organize_name',   //这里是一个标记， 应该可以直接返回对象的id属性值，同时是一个标记，许多选择的东西通过这个。
                    title: '名称',  //这个就是界面显示的th
                    sortable: true,     // 排序
                }, {
                    field: 'level',
                    title: '级别',
                    sortable: true,
                }, {
                    field: 'parent_tree_name',
                    title: '父级'
                }, {
                    field: 'id',
                    title: '操作',
                    events: Operate.operateEvents,
                    formatter: operateFormatter,
                    titleTooltip: 'what',    // 鼠标在该字段不动的时候，显示说明
                    clickToSelect: false,   //与外面的clicktoselect结合使用
                }
            ],
            detailView: true,       // 详情功能
            detailFormatter: function (index, row) {     //详情格式化
                return index;
            },
            showColumns: true,      // 列影藏
            showRefresh: true,      // 刷新按钮
            // showToggle: true,       // 视图切换
            // showPaginationSwitch: true      // 显示影藏分页
            toolbar: "#toolbar", // 工具行
            clickToSelect: true,     // 点击行，就选择到checkbox

        });
        function operateFormatter(value, row, index) {
            return [
                '<a class="edit text-primary" href="javascript:void(0)" title="编辑">',
                '<i class="glyphicon glyphicon-pencil"></i>',
                '</a>',
                '&nbsp;',
                '<a class="remove text-red" href="javascript:void(0)" title="删除">',
                '<i class="glyphicon glyphicon-remove"></i>',
                '</a>'
            ].join('');
        }
    };
    return {
        init: function () {
            e();
        }
    }
}();
jQuery(document).ready(function () {
    BootstrapTables.init();
    var $table = $("#boot_table");
    $table.on('load-success.bs.table', function () {
        $table.bootstrapTable('expandAllRows');

    });

    // $table.bootstrapTable('remove', {field: 'id', values: ids});  //删除行，这里 id 是字段
    // $table.bootstrapTable('updateRow', {index: 1, row: row});     // 更新行，index就是table自己的一个索引序列。 row是一个对象。
    // $table.bootstrapTable('insertRow', {index: 1, row: row});     // 插入页
    // $table.bootstrapTable('selectPage', page);          // 跳页
    // $table.bootstrapTable('getSelections');      // 获取选择到的行
    // $table.bootstrapTable('refresh');        // 刷新， 原有的排序 工具里的参数， 分页都会在， 不过滚动条会回到头。 多条更新的时候看情况。

});