# coding: utf-8
from .models import User, Organize, Jurisdiction, UserJurisdiction, DefaultJurisdiction

BaseTableMondel = {
    'user': {
        'fieldList': [f.name for f in User._meta.get_fields()],
        'fieldInt': ['id', 'create_user_id', 'update_user_id', 'organize_id'],
        # 'fieldRange': [],
        'fieldTime': ['date_joined', 'update_time', 'quit_time', 'last_login'],
        'charIndex': ['organize_tree_id'],
        'db_table': User._meta.db_table
    }
}


# 其中tables需要说明一下
# [{'table_name':table_name,'table_field':[name1,name2],'table_key':关联的主键},{'table_name':table_name,'table_field':[name1,name2],'table_key':关联的主键}……]
# 第一个是主表，后面的都为副表，后面的表关联主键全部和第一个表的关联主键关联，然后联表查这几个多表。
# 如果多个表有相同字段，用 ' as 别名'
def dataTableConfig(config_key):
    global BaseTableMondel
    if config_key == 'sysUser':
        fieldDict = {
            'fieldList': [  # user
                'id','last_login','username','email','is_staff','is_active',
                'date_joined','default_Ups','default_Usps','default_Fedex',
                'erp_id', 'organize_tree_id', 'user_code', 'position',
                'create_user_id', 'create_user_name', 'update_time', 'update_user_id',
                'update_user_name', 'quit_time', 'organize_id',
                # organzie
                'organize_name', 'level', 'url', 'parent_tree_name'
            ],
            # 'theadList': ["category_id_path", "supplier_id", "title", "developer_id", "ps_state",
            #               "priority", "create_time", "deadline", "id"],
            # 'asFieldList': ["edit_state", "ps_state"],
            # 'asTableList': ["task_main", "task_main"],
            # 'fieldThead': ["类别", "供应商", "title", "开发人", "美工",
            #                "优先级", "创建时间", "时限", "操作"],
            'tables': [{'table_name': 'user',
                        'table_field': ['id','last_login','username','email','is_staff','is_active',
                                        'date_joined','default_Ups','default_Usps','default_Fedex',
                                        'erp_id', 'organize_tree_id', 'user_code', 'position',
                                        'create_user_id', 'create_user_name', 'update_time', 'update_user_id',
                                        'update_user_name', 'quit_time', 'organize_id'],
                        'table_key': 'organize_id'},
                       {'table_name': 'organize',
                        'table_field': ['organize_name', 'level', 'url', 'parent_tree_name'],
                        'table_key': 'id'}]
        }
        fieldDict.update(BaseTableMondel['user'])
        return fieldDict

    if config_key == 'myEditTask':  # 个人任务管理
        fieldDict = {
            # fieldList是用来找查询字段的，遍历fieldList,获取请求，多表如果冲突，这里应该是as 后的别名
            'fieldList': [#taskmain
                          'category_id_path', 'category_name_path', 'create_time', 'deadline', 'edit_difficulty',
                          'edit_end_time', 'edit_handle_id', 'edit_handle_name', 'edit_reward', 'edit_score',
                          'edit_state', 'edit_type', 'id', 'priority', 'product_id', 'ps_difficulty', 'ps_end_time',
                          'ps_handle_id', 'ps_handle_name', 'ps_reward', 'ps_score', 'ps_state', 'ps_type',
                          'supplier_id', 'title',
                          #product
                          'new_category_id_path', 'new_category_name_path', 'supplier_name'],
            'fieldInt': ['id', 'product_id', 'supplier_id', 'ps_state', 'ps_difficulty',
                         'ps_handle_id', 'ps_score', 'edit_state', 'edit_difficulty',
                         'edit_handle_id', 'edit_score', 'priority',
                         'edit_type', 'ps_type'],
            # 'fieldRange': [],
            'fieldTime': ['create_time', 'deadline', 'ps_end_time', 'edit_end_time'],
            'charIndex': ['category_id_path'],

            'theadList': ["category_id_path", "supplier_id", "title", "developer_id", "ps_state",
                          "priority", "create_time", "deadline", "edit_difficulty",
                          "edit_handle_name", "edit_end_time", "edit_score", "edit_state"],
            #where子句中的冲突，如果两个表都含有该字段，那么查询就需要加表名去查询。
            'asFieldList': ["edit_state", "ps_state"],
            'asTableList': ["task_main", "task_main"],

            #这里面的字段是用来sql查询的，冲突的字段应该是 原字段as别名
            'tables': [{'table_name': 'task_main',
                        'table_field': ['category_id_path', 'create_time', 'deadline', 'edit_difficulty',
                                        'edit_end_time', 'edit_handle_id', 'edit_handle_name', 'edit_reward',
                                        'edit_score', 'edit_state', 'edit_type', 'id', 'priority', 'product_id',
                                        'ps_difficulty', 'ps_end_time', 'ps_handle_id', 'ps_handle_name', 'ps_reward',
                                        'ps_score', 'ps_state', 'ps_type', 'supplier_id', 'title'],
                        'table_key': 'product_id'},
                       {'table_name': 'product_main',
                        'table_field': ['new_category_id_path', 'new_category_name_path', 'supplier_name', 'developer_id', 'developer_name',
                                        'ps_state as product_ps_state'],
                        'table_key': 'id'}]
        }
        return fieldDict

    if config_key == 'editTaskCount':
        fieldDict = {
            'theadList': [],
            'fieldList': [],
            'fieldInt': [],
            'tables': [{'table_name': 'task_main',
                        'table_field': [],
                        'table_key': 'product_id'},
                       ]
        }
        fieldDict.update(BaseTableMondel['taskMain'])
        return fieldDict
