# -*- coding: utf-8 -*-

from django.db import connection, connections
from starpro.utils import json_encode, dictfetchall, listfetchall,\
     tuplefetchall

from .models import User, Organize, Jurisdiction, UserJurisdiction, DefaultJurisdiction

from .field_config import dataTableConfig

class MainIdSql():
    """bootstarp table 异步取数据,基本操作都差不多，封装起来,这里是为了生成原生sql，不是django queryset。
       这里是第一步，先按照主表的搜索条件来查出id"""
    def __init__(self, request, config, searchList = None):
        self.request = request
        self.searchList = searchList or []
        self.orderByStr = None
        self.table = config['db_table']
        self.config = config

    def getFieldDetail(self):
        fieldDetail = self.config
        self.fieldList = fieldDetail['fieldList']
        self.fieldInt = fieldDetail['fieldInt']
        if fieldDetail.get('charIndex'):
            self.charIndex = fieldDetail['charIndex']
        if fieldDetail.get('fieldRange'):
            self.fieldRange = fieldDetail['fieldRange']
        if fieldDetail.get('fieldTime'):
            self.fieldTime = fieldDetail['fieldTime']
        if fieldDetail.get('asFieldList'):
            self.asFieldList = fieldDetail['asFieldList']

    def bootTable(self):
        """bootstarp table 插件 页面参数"""
        self.tableOffset = int(self.request.POST.get('offset'))  # 起始数，0开始
        self.tableLimit = int(self.request.POST.get('limit'))  # 每页显示数

    def getOrderBy(self):
        """ 排序功能 """
        self.orderByStr = None
        sort = self.request.POST.get('sort')  # 排序字段名
        order = self.request.POST.get('order')  # 排序方式
        if sort:
            self.orderByStr = " ORDER BY %s "%sort
            if order == 'desc':
                self.orderByStr += ' DESC '
        return self.orderByStr

    def getParam(self, x):
        if hasattr(self, 'fieldRange') and (x in self.fieldRange):
            return [self.request.POST.get(x+'_gt'), self.request.POST.get(x+'_lt')]
        elif hasattr(self, 'fieldTime') and (x in self.fieldTime):
            return [self.request.POST.get(x+'_gt'), self.request.POST.get(x+'_lt')]
        else:
            return self.request.POST.get(x)

    def getParamList(self):
        """ 获取tables传回的参数 """
        self.paramList = map(self.getParam, self.fieldList)
        return self.paramList

    def getSearchList(self):
        """ 过滤空参数，并且将参数变为匹配字符串 """
        table = self.table
        for i, v in enumerate(self.paramList):
            if v:
                field = self.fieldList[i]
                if hasattr(self, 'asFieldList') and (field in self.asFieldList):
                    field = table + '.' + field
                if field in self.fieldInt:
                    self.searchList.append(field+" = %s"%int(v))
                elif hasattr(self, 'fieldRange') and (field in self.fieldRange):
                    if v[0]:
                        self.searchList.append(field+" >= %s"%v[0])
                    if v[1]:
                        self.searchList.append(field+" <= %s"%v[1])
                elif hasattr(self, 'fieldTime') and (field in self.fieldTime):
                    if v[0]:
                        time_begin = v[0] + ' 00:00:00'
                        self.searchList.append(field+" >= '%s'"%time_begin)
                    if v[1]:
                        time_end = v[1] + ' 23:59:59'
                        self.searchList.append(field+" <= '%s'"%time_end)
                elif hasattr(self, 'charIndex') and (field in self.charIndex):
                    self.searchList.append(field+" LIKE '%s%%'"%v)
                else:
                    self.searchList.append(field+" LIKE '%%%s%%'"%v)
        return self.searchList

    def getSearchStr(self):
        if self.searchList:
            self.searchStr=' WHERE '+' and '.join(self.searchList)
        else:
            self.searchStr=""
        return self.searchStr

    def getSqlStr(self, type='datatable'):
        """ 拼接查询语句 """
        table = self.table
        self.sqlstr='SELECT id FROM %s %s'%(table, self.searchStr)

        if self.orderByStr:
            self.sqlstr += self.orderByStr
        if type=='datatable':
            self.sqlstr +=' LIMIT %s,%s'%(self.tableOffset, self.tableLimit)

        return self.sqlstr

    def getCountStr(self):
        """ 总记录数sql """
        table = self.table
        self.countstr = 'SELECT count(id) FROM %s %s'%(table, self.searchStr)

        return self.countstr

    def run(self):
        self.getFieldDetail()
        self.bootTable()
        self.getOrderBy()
        self.getParamList()
        self.getSearchList()
        self.getSearchStr()
        self.getSqlStr()
        self.getCountStr()
        return self.sqlstr, self.countstr

class MultiTableById():
    '''根据主表的id来联表查询所需数据'''

    def __init__(self, tables, id_tuple_str):
        # tables 格式为 [{'table_name':table_name,'table_field':[name1,name2],'table_key':关联的主键},{}……]
        # 采用leftjoin方式， 关联方式，后面所有的表与第一个表关联
        self.tables = tables
        self.id_tuple_str = id_tuple_str

    def selectField(self, table_name, table_field):
        l = [table_name+'.'+x for x in table_field]
        return ','.join(l)

    def loopTables(self):
        tables = self.tables
        id_tuple_str = self.id_tuple_str
        selectField = self.selectField

        table_main = tables[0]
        table_vice = tables[1:]

        main_name = table_main['table_name']
        main_field = table_main['table_field']
        main_key = table_main['table_key']

        select_str = 'SELECT ' + selectField(main_name, main_field)
        from_str = ' FROM %s '%main_name
        left_str = ''
        where_str = ' WHERE %s.id in %s ORDER BY FIELD(%s.id, %s'%(main_name, id_tuple_str, main_name, id_tuple_str[1:])


        for table in table_vice:
            table_name = table['table_name']
            table_field = table['table_field']
            table_key = table['table_key']

            select_str += ','+selectField(table_name, table_field)
            left_str += ' LEFT JOIN %s ON %s.%s=%s.%s'%(table_name, main_name, main_key, table_name, table_key)

        final_sql = select_str + from_str + left_str + where_str
        return final_sql

    def run(self):
        return self.loopTables()


class QuaryTableBySql():
    """这里的查询封装，只限于，搜索排序字段都在主表里面，附表只用来左联接。"""
    def __init__(self, request, config_key, searchList = None, db_name='default'):
        self.request = request
        self.config = dataTableConfig(config_key)
        self.searchList = searchList
        self.db_name = db_name
        self.tables = self.config['tables']

    def getCursor(self):
        db_name = self.db_name
        if db_name == 'default':
            self.cursor = connection.cursor()
        else:
            self.cursor = connections[db_name].cursor()


    def getTableData(self):
        request = self.request
        searchList = self.searchList
        cursor = self.cursor
        tables = self.tables
        config = self.config

        count = 0
        tableData = []

        try:
            mainIdSql = MainIdSql(request, config, searchList)
            data_sql, count_sql = mainIdSql.run()
            cursor.execute(count_sql)
            count = cursor.fetchone()[0]
            print data_sql
            cursor.execute(data_sql)
            id_tuple = tuplefetchall(cursor)

            if id_tuple:
                id_tuple_str = str(id_tuple).replace(',)', ')')
                multiTableById = MultiTableById(tables, id_tuple_str)
                final_sql = multiTableById.run()
                print '-------'
                print final_sql
                cursor.execute(final_sql)
                tableData = dictfetchall(cursor)

        finally:
            cursor.close()

        return count, tableData

    def run(self):
        self.getCursor()
        return self.getTableData()


class UnionDataTableSql():
    """union多表联合查询,这里是为了生成原生sql，不是django queryset。"""
    def __init__(self, request, config_key, searchList = None, db_name='default'):
        self.request = request
        self.searchList = searchList or []
        self.orderByStr = None
        self.config = dataTableConfig(config_key)
        self.db_name = db_name
        self.tables = self.config['tables']

    def getTablePostfix(self):
        request = self.request
        category_id_path = request.POST.get('category_id_path')
        catlist = []
        if category_id_path:
            cat_id = category_id_path.split('>')[0]
            catlist = Category.objects.filter(id=cat_id)
        else:
            handle_id = request.session.get('user')
            handle = SysUser.objects.get(id=handle_id)
            cat_ids = handle.edit_cat_ids #编辑做过哪些分类
            if cat_ids:
                cat_id_li = [int(x) for x in cat_ids.split(',') if x]
            else:
                cat_id_li = []
            catlist = Category.objects.filter(id__in=cat_id_li)
        self.table_postfix = ['_'+x.table_name for x in catlist]
        return self.table_postfix


    def getFieldDetail(self):
        fieldDetail = self.config
        self.fieldList = fieldDetail['fieldList']
        self.fieldInt = fieldDetail['fieldInt']
        if fieldDetail.get('charIndex'):
            self.charIndex = fieldDetail['charIndex']
        if fieldDetail.get('fieldRange'):
            self.fieldRange = fieldDetail['fieldRange']
        if fieldDetail.get('fieldTime'):
            self.fieldTime = fieldDetail['fieldTime']
        if fieldDetail.get('asFieldList'):
            self.asFieldList = fieldDetail['asFieldList']
            self.asTableList = fieldDetail['asTableList']


    def datatable(self):
        """datatable 插件 页面参数"""
        self.iDisplayStart = int(self.request.POST['iDisplayStart'])    #起始页
        self.iDisplayLength = int(self.request.POST['iDisplayLength'])   #该页显示数据量


    def getOrderBy(self):
        """ 排序功能 """
        self.orderByStr = None
        iSortCol_0 = self.request.POST['iSortCol_0']  #排序参数：列的索引号
        sSortDir_0 = self.request.POST['sSortDir_0']  #排序参数：顺逆规则
        if iSortCol_0:
            if sSortDir_0=='asc':
                self.orderByStr = " ORDER BY %s"%self.theadList[int(iSortCol_0)]
            else:
                self.orderByStr = " ORDER BY %s DESC"%self.theadList[int(iSortCol_0)]
        return self.orderByStr

    def getParam(self, x):
        if hasattr(self, 'fieldRange') and (x in self.fieldRange):
            return [self.request.POST.get(x+'_gt'), self.request.POST.get(x+'_lt')]
        elif hasattr(self, 'fieldTime') and (x in self.fieldTime):
            return [self.request.POST.get(x+'_gt'), self.request.POST.get(x+'_lt')]
        else:
            return self.request.POST.get(x)


    def getParamList(self):
        """ 获取datatables传回的参数 """
        self.paramList = map(self.getParam, self.fieldList)
        return self.paramList

    def getSearchList(self):
        """ 过滤空参数，并且将参数变为匹配字符串 """
        for i, v in enumerate(self.paramList):
            if v:
                field = self.fieldList[i]
                if hasattr(self, 'asFieldList') and (field in self.asFieldList):
                    table_name = self.asTableList[self.asFieldList.index(field)] + '_postfix'
                    if field in self.fieldInt:
                        self.searchList.append(table_name+'.'+field+" = %s"%int(v))
                    elif hasattr(self, 'fieldRange') and (field in self.fieldRange):
                        if v[0]:
                            self.searchList.append(table_name+'.'+field+" >= %s"%v[0])
                        if v[1]:
                            self.searchList.append(table_name+'.'+field+" <= %s"%v[1])
                    elif hasattr(self, 'fieldTime') and (field in self.fieldTime):
                        if v[0]:
                            time_begin = v[0] + ' 00:00:00'
                            self.searchList.append(table_name+'.'+field+" >= '%s'"%time_begin)
                        if v[1]:
                            time_end = v[1] + ' 23:59:59'
                            self.searchList.append(table_name+'.'+field+" <= '%s'"%time_end)
                    else:
                        self.searchList.append(table_name+'.'+field+" LIKE '%%%s%%'"%v)
                else:
                    if field in self.fieldInt:
                        self.searchList.append(field+" = %s"%int(v))
                    elif hasattr(self, 'fieldRange') and (field in self.fieldRange):
                        if v[0]:
                            self.searchList.append(field+" >= %s"%v[0])
                        if v[1]:
                            self.searchList.append(field+" <= %s"%v[1])
                    elif hasattr(self, 'fieldTime') and (field in self.fieldTime):
                        if v[0]:
                            time_begin = v[0] + ' 00:00:00'
                            self.searchList.append(field+" >= '%s'"%time_begin)
                        if v[1]:
                            time_end = v[1] + ' 23:59:59'
                            self.searchList.append(field+" <= '%s'"%time_end)
                    else:
                        self.searchList.append(field+" LIKE '%%%s%%'"%v)
        return self.searchList

    def getSearchStr(self):
        if self.searchList:
            self.searchStr=' WHERE '+' and '.join(self.searchList)
        else:
            self.searchStr=""
        return self.searchStr



    def selectField(self, table_name, table_field):
        l = [table_name+'.'+x for x in table_field]
        return ','.join(l)

    def searchAsStr(self,searchStr, postfix):
        if hasattr(self, 'asFieldList'):
            asFieldList = self.asFieldList
            for i, field in enumerate(asFieldList):
                table_name = self.asTableList[i] + '_postfix'
                new_name = self.asTableList[i] + postfix
                searchStr = searchStr.replace(table_name,new_name)
            return searchStr
        else:
            return searchStr

    def getOneSql(self, postfix, searchStr):
        '''获取联合查询中 单个查询的sql'''
        selectField = self.selectField
        tables = self.tables

        table_main = tables[0]
        main_name = table_main['table_name'] + postfix
        main_field = table_main['table_field']
        main_key = table_main['table_key']
        select_str = 'SELECT ' + selectField(main_name, main_field)
        select_cont_str = 'SELECT count(%s.id) as cnt '%main_name
        from_str = ' FROM %s '%main_name
        left_str = ''
        where_str = self.searchAsStr(searchStr, postfix)

        table_vice = tables[1:]
        for table in table_vice:
            table_name = table['table_name'] + postfix
            table_field = table['table_field']
            table_key = table['table_key']

            select_str += ','+selectField(table_name, table_field)
            left_str += ' LEFT JOIN %s ON %s.%s=%s.%s'%(table_name, main_name, main_key, table_name, table_key)


        final_sql = select_str + from_str + left_str + where_str
        final_count_sql = select_cont_str + from_str + left_str + where_str
        return final_sql, final_count_sql


    def getSqlStr(self, type='datatable'):
        """ 拼接查询语句 """
        table_postfix = self.table_postfix
        getOneSql = self.getOneSql
        searchStr = self.searchStr

        # def _getOneSql(x):
        #     return getOneSql(x, searchStr)
        # count_list = map(_getOneSql, table_postfix)
        count_list = []
        data_list = []
        for postfix in table_postfix:
            data_sql, count_sql = getOneSql(postfix, searchStr)
            data_list.append(data_sql)
            count_list.append(count_sql)

        sqlstr = ' union all '.join(data_list)
        if self.orderByStr:
            sqlstr += self.orderByStr
        if type=='datatable':
            sqlstr +=' LIMIT %s,%s'%(self.iDisplayStart, self.iDisplayLength)

        self.sqlstr = sqlstr

        countsql = ' union all '.join(count_list)
        self.countsql = countsql
        return sqlstr, countsql

    def getCountStr(self):
        """ 总记录数sql """
        sql_str = self.countsql
        if sql_str:
            self.countstr = 'select sum(cnt) from (' + sql_str + ') t'
        else:
            self.countstr = ''
        return self.countstr

    def run(self):
        self.getTablePostfix()
        if not self.getTablePostfix():
            return '', ''
        self.getFieldDetail()
        self.datatable()
        self.getOrderBy()
        self.getParamList()
        self.getSearchList()
        self.getSearchStr()
        self.getSqlStr()
        self.getCountStr()
        return self.sqlstr, self.countstr


class MyEditTaskDataTableSql(UnionDataTableSql):
    def getOneSql(self, postfix, searchStr):
        '''获取联合查询中 单个查询的sql'''
        selectField = self.selectField
        tables = self.tables

        table_main = tables[0]
        main_name = table_main['table_name'] + postfix
        main_field = table_main['table_field']
        main_key = table_main['table_key']
        select_str = 'SELECT ' + selectField(main_name, main_field)
        select_cont_str = 'SELECT count(%s.id) as cnt '%main_name
        from_str = ' FROM %s '%main_name
        left_str = ''
        where_str = self.searchAsStr(searchStr, postfix)

        table_vice = tables[1:]
        for table in table_vice:
            table_name = table['table_name'] + postfix
            table_field = table['table_field']
            table_key = table['table_key']

            select_str += ','+selectField(table_name, table_field)
            left_str += ' LEFT JOIN %s ON %s.%s=%s.%s'%(table_name, main_name, main_key, table_name, table_key)

        select_str += ", '%s' as table_name"%main_name

        final_sql = select_str + from_str + left_str + where_str
        final_count_sql = select_cont_str + from_str + left_str + where_str
        return final_sql, final_count_sql

class MyEditTaskCountSql(MyEditTaskDataTableSql):
    def datatable(self):
        self.iDisplayStart = 0
        self.iDisplayLength = 0
    def getOrderBy(self):
        self.orderByStr = ''
        return ''

class EditTaskCountSql(UnionDataTableSql):
    def getTablePostfix(self):
        catlist = Category.objects.filter(category_id_path='0')
        self.table_postfix = ['_'+x.table_name for x in catlist]
        self.table_id = [x.id for x in catlist]
        self.table_name = [x.category_name for x in catlist]
        return self.table_postfix

    def getOneSql(self, postfix, searchStr):
        '''各分类不同状态数据统计，方便主管去浏览操作。'''
        tables = self.tables

        table_main = tables[0]
        main_name = table_main['table_name'] + postfix
        # main_key = table_main['table_key']
        select_cont_str = 'SELECT count(%s.id) as cnt '%main_name
        from_str = ' FROM %s '%main_name
        left_str = ''
        where_str = self.searchAsStr(searchStr, postfix)

        # 这里应该支持，多表的条件查询，目前还没用的先不出理了
        # table_vice = tables[1:]
        # for table in table_vice:
        #     table_name = table['table_name'] + postfix
        #     table_key = table['table_key']
        #
        #     left_str += ' LEFT JOIN %s ON %s.%s=%s.%s'%(table_name, main_name, main_key, table_name, table_key)
        i = self.table_postfix.index(postfix)
        id = self.table_id[i]
        category_name = self.table_name[i]
        select_cont_str += ", '%s' as id, '%s' as category_name"%(id, category_name)

        final_count_sql = select_cont_str + from_str + left_str + where_str
        return '', final_count_sql

    def getSqlStr(self, type='datatable'):
        """ 拼接查询语句 """
        table_postfix = self.table_postfix
        getOneSql = self.getOneSql
        searchStr = self.searchStr

        count_list = []
        data_list = []
        for postfix in table_postfix:
            data_sql, count_sql = getOneSql(postfix, searchStr)
            data_list.append(data_sql)
            count_list.append(count_sql)


        countsql = ' union all '.join(count_list)
        self.countsql = countsql
        return '', countsql


    def run(self):
        ret = self.getTablePostfix()
        if not ret:
            return '', ''
        self.getFieldDetail()
        self.getParamList()
        self.getSearchList()
        self.getSearchStr()
        self.getSqlStr()
        return '', self.countsql

class EditTaskCountSqlCategory(EditTaskCountSql):
    def getTablePostfix(self, cat_id):
        catlist = Category.objects.filter(id=cat_id)
        self.table_postfix = ['_'+x.table_name for x in catlist]
        self.table_id = [x.id for x in catlist]
        self.table_name = [x.category_name for x in catlist]
        return self.table_postfix

    def run(self, cat_id):
        ret = self.getTablePostfix(cat_id)
        if not ret:
            return '', ''
        self.getFieldDetail()
        self.getParamList()
        self.getSearchList()
        self.getSearchStr()
        self.getSqlStr()
        return '', self.countsql

class RunSql():
    ''' 执行sql '''
    def __init__(self, db_name='default'):
        self.db_name = db_name

    def getCursor(self):
        db_name = self.db_name
        if db_name == 'default':
            self.cursor = connection.cursor()
        else:
            self.cursor = connections[db_name].cursor()


    def runDictData(self,sqlstr):
        cursor = self.cursor
        data = []
        try:
            cursor.execute(sqlstr)
            data = dictfetchall(cursor)

        except:
            pass

        return data

    def runOneData(self,sqlstr):
        cursor = self.cursor
        data = None
        try:
            cursor.execute(sqlstr)
            data = cursor.fetchone()
        except:
            pass

        return data

    def closeCursor(self):
        self.cursor.close()




