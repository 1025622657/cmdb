
//自执行函数，相当于封装了作用域，只有内部能调用，外部没有，防止重名
(function(jq){
    var CREATE_SEARCH_CONDITION = true;
    var GLOBAL_DICT = {};


    // console.log(jq);
    //为字符串创建format方法，用于字符串格式化
    String.prototype.format = function (args) {
        return this.replace(/\{(\w+)\}/g,function (s,i) {
            return args[i];
        })
    };

    //搜索条件
    function getSearchCondition(){
        var condition = {};
        //查找input标签或select标签的name,value
        $('.search-list').find('input[type="text"],select').each(function(){
            /*获取所有的搜索条件 */
            var name = $(this).attr('name');
            var value = $(this).val();
            if(condition[name]){
                //.push为添加
                condition[name].push(value);
            }else{
                condition[name] = [value,];
            }
            // console.log('==',condition)

                })
        return condition;
    }

    function initial(url) {
        //执行一个函数，获取当前搜索条件
        //注：搜索或刷新均会执行initial函数，查询条件为输入框的条件，直接访问url也会执行initial函数，但查询条件为空
        var searchCondition = getSearchCondition();
        console.log('----?',searchCondition);
        $.ajax({
            url:url,
            type:'GET',//获取数据
            data:{'condition':JSON.stringify(searchCondition)},//把搜索条件发到后台
            dataType:'JSON',
            success:function (arg) {
                //把枚举类型的数据，或数据库里查询到的类型，返回并存下便于后继使用
                $.each(arg.global_dict,function(k,v){
                    //因经常用到，所以处理成变量存放
                    GLOBAL_DICT[k] = v
                });

                /*
                {
                    'server_list':list(server_list),#所有的数据
                    'table_config':table_config，#所有的配置
                }
                #无组json序列化后会变成列表
                'global_dict':{
                     'device_type_choices':(
                             (1, '服务器'),
                            (2, '交换机'),
                            (3, '防火墙'),
                     ),
                      'device_status_choices': (
                           (1, '上架'),
                           (2, '在线'),
                          (3, '离线'),
                         (4, '下架'),
                      ),
                }

                */

                initTableHeader(arg.table_config);
                initTableBody(arg.server_list,arg.table_config);
                initSearch(arg.search_config);

            }
        })
    }
    /*
    初始化搜索条件
    */
    function initSearch(searchConfig){
        //只生成一次搜索条件
        if(searchConfig && CREATE_SEARCH_CONDITION){
            console.log(searchConfig)
            CREATE_SEARCH_CONDITION = false;
            //找到searchArea ul,初始化搜索的下拉选项
            $.each(searchConfig,function(k,v){
                /*if(k==0){
                    $('#searchDefault').text(v.text);
                }*/
                var li = document.createElement('li');
                $(li).attr('search_type',v.search_type);
                $(li).attr('name',v.name);

                //select标签时，设置多一个global_name属性
                if(v.search_type == 'select'){
                    $(li).attr('global_name',v.global_name);
                }

                var a = document.createElement('a');
                a.innerHTML = v.text;
                $(li).append(a);
                //初始化时，只有一个searchArea ul,所以用class定位无素也可以，
                //类定义会定义到，所有这个类的元素
                $(".searchArea ul").append(li)
            });

            //初始化默认搜索条件
            //searchConfig[0],进行初始化
            //初始化默认选中值
            $('.search-item .searchDefault').text(searchConfig[0].text);

            //初始化默认查询标签
            if(searchConfig[0].search_type == 'select'){
                //select标签
                var sel = document.createElement('select');
                 $(sel).attr('class','form-control');
                $.each(GLOBAL_DICT[searchConfig[0].global_name],function(k,v){
                    var op = document.createElement('option');
                    $(op).text(v[1]);
                    $(op).val(v[0]);
                    $(sel).append(op);
                });
                $('.input-group').append(sel);

            }else{
                //input标签
                //<input type="text" class="form-control" aria-label="...">
                var inp = document.createElement('input');
                $(inp).attr('name',searchConfig[0].name);
                $(inp).attr('type','text');
                $(inp).attr('class','form-control');
                $('.input-group').append(inp);

            }
        }

    }

    //列表头的设置
    function initTableHeader(tableConfig) {
        /*
        [
            {'q':'id','title':'ID'},
            {'q':'hostname','title':'主机名'},
        ]

        */
        console.log("===",tableConfig)
        var tr = document.createElement('tr');
        $.each(tableConfig,function (k,v) {


            //列表表头的设置，循环配置文件，
            //display为True设置前台可见，tableConfig为列表嵌套字典
            //字典里的值，js可通过v.titile或v['title']获取

            $('#tbHead').empty();//刷新的时候需要清空，因为是再次发起请求
            if (v.display){
                var tag = document.createElement('th');
                // tag.innerHTML = v.title;
                $(tag).html(v.title) ;
                $(tr).append(tag);//<tr>下添加<th>子类

            }
        });
        $('#tbHead').append(tr);//<thead>下添加<tr>
    }
    //列表内容的设置
    function initTableBody(serverList,tableConfig) {

        /*
         [
            {'id':1,'hostname':c2.com,create_at:'xxxx-xx-xx'},
            {'id':1,'hostname':c2.com,create_at:'xxxx-xx-xx'},
            {'id':1,'hostname':c2.com,create_at:'xxxx-xx-xx'},
         ]
        */
        $('#tbBody').empty();//刷新时需清空内容
        $.each(serverList,function (k,row) {

            //row:{'id':1,'hostname':c2.com,create_at:'xxxx-xx-xx'},
            /*
            <tr>
                <td>1</td>
                <td>2</td>
                <td>3</td>
            </tr>
            */
            //设置行<tr>
            var tr = document.createElement('tr');
            // tr.setAttribute('nid',row.id);
            $(tr).attr('nid',row.id);
            $.each(tableConfig,function (kk,rrow) {

                //kk:1  rrow:{'q':'id','title':'ID'},//rrow.q = 'id'
                //kk: .  rrow:{'q':'hostname','title':'主机名'},//rrow.q = 'hostname'
                //kk: .  rrow:{'q':'create_at','title':'创建时间'},//rrow.q = 'create_at'

                //设置列<td>
                if (rrow.display){
                    var td = document.createElement('td');
                    /*if(rrow['q']){
                        td.innerHTML = row[rrow.q];
                    }
                    else{
                        td.innerHTML = rrow.text;
                    }*/

                    //rrow.text.tpl = "abce{n1}sdf"
                    //rrow.text.kwargs = {'n1':'@id',n2':'@@123'}


                    /*在td标签中添加内容*/
                    var newKwars = {};//{'n1':1,n2':'123'}
                    $.each(rrow.text.kwargs,function (kkk,vvv) {
                        var av = vvv;
                        //两个'@@'符号表示models下的枚举类型显示内容
                        if(vvv.substring(0,2) == '@@'){
                            var global_dict_key = vvv.substring(2,vvv.length);
                            var nid = row[rrow.q];
                            $.each(GLOBAL_DICT[global_dict_key],function(gk,gv){

                                if(gv[0] == nid){
                                    av = gv[1];
                                }
                            })
                        }
                        //一个'@'表示models下.values值的获取，即serverList里的内容
                        else if(vvv[0] == '@'){
                             av = row[vvv.substring(1,vvv.length)];//把@切除，即id的值,再通过serverList里的key获取

                        }
                        newKwars[kkk] = av;

                    });


                    var newText = rrow.text.tpl.format(newKwars);

                    //设置td标签文本
                    td.innerHTML = newText;


                    /* 在td标签中添加属性*/
                    $.each(rrow.attrs,function(atkey,atval){
                        if(atval[0] == '@'){
                            td.setAttribute(atkey,row[atval.substring(1,atval.length)]);
                        }else{
                             td.setAttribute(atkey,atval);
                        }

                    });

                    $(tr).append(td);
                }
            });



            /*$.each(row,function (kk,rrow) {
                //kk:'id'  rrow:1
                var td = document.createElement('td');
                td.innerHTML = rrow;
                $(tr).append(td);

            })*/
            $('#tbBody').append(tr);
        })
    }
    //进入编辑模式
    function trIntoEdit($tr){
        $tr.find('td[edit-enable="true"]').each(function(){
            //$(this)每一个td
            var editType = $(this).attr('edit-type');
            if(editType == 'select'){
                //生成下拉框,找到数据源
                //$(this).arrt('global_key');//device_type_choices
                var deviceTypeChoices = GLOBAL_DICT[$(this).attr('global_key')];
                // console.log('><',deviceTypeChoices)

                //生成select标签
                var selectTag = document.createElement('select');
                var origin = $(this).attr('origin');//默认选中的option

                $.each(deviceTypeChoices,function(k,v){
                    var option = document.createElement('option');
                    $(option).text(v[1]);
                    $(option).val(v[0]);
                    if(v[0] == origin){
                        //默认选中原来的值
                        $(option).prop('selected',true);
                    }
                    $(selectTag).append(option);
                });

                $(this).html(selectTag);
                //显示默认值

            }else{
                //获取原来td中的文本内容
                var v1 = $(this).text();
                //创建input标签，并且内部设置值
                var inp = document.createElement('input');
                $(inp).val(v1);//input框的value设置成v1
                //添加到td中
                $(this).html(inp);


            }
        })

    }
    //退出编辑模式
    function trOutEdit($tr){

        //console.log($tr[0])转成DOM对象看$tr内容，$tr为jQuery对象
        $tr.find('td[edit-enable="true"]').each(function(){
            //查找到可编辑属性为真的td标签
            // $(this)每一个td
            var editType = $(this).attr('edit-type');
            //如果td标签有edit-type这个属性则为【select】标签，没有则默认生成【input】标签
            if(editType == 'select'){
                /*
                v = $('#i1')[0]  变DOC对象
                op = v.selectedOptions ===>  [<option value='2'>上海 </option>]
                v.selectedIndex ===>2
                $(op).text()
                $(op).val()
                */
                var option = $(this).find('select')[0].selectedOptions;
                //设置修改的select状态，key:new-origin
                $(this).attr('new-origin',$(option).val());
                $(this).html($(option).text());

            }else{
               var inputVal = $(this).find('input').val();
               // console.log('--',inputVal);
                $(this).html(inputVal);
            }


        });
    }

    jq.extend({
        xx:function(url){

            initial(url);


            //以委托的形式加载数据，后面才加载的数据，用这种形式
            //所有checkbox绑定事件

            //选中则进入/退出编辑模式
            $('#tbBody').on('click',':checkbox',function(){
                //$(this)为[type=checkbox]标签,即选择列表下的input标签;
                //1.检测是否已经补选中
                // alert('123');
                // alert($(this).prop('checked'));
                if($('#inOutEditMode').hasClass('btn-warning')) {
                    //若【进入编辑模式】为选中状态则进入编辑模式
                    var $tr = $(this).parent().parent();

                    if ($(this).prop('checked')) {
                        //若选择列表为【选中】状态则进入编辑模式
                        trIntoEdit($tr);
                    } else {
                        //退出编辑模式
                        trOutEdit($tr)
                    }
                }
            });


            //全选按钮绑定事件，批量操作
            $('#checkAll').click(function(){
                /*
                $('#tbBody').find(':checkbox').prop('checked',true);
                //选中每一个，进入编辑模式
                $('#tbBody').find('tr').each(function(){
                    trIntoEdit($(this));
                })
                */
                if($('#inOutEditMode').hasClass('btn-warning')){
                    $('#tbBody').find(':checkbox').each(function(){
                    //没有选中的通过全选进入编辑模式，
                    //因原来点击已经进入了编辑模式，所以只把没选中的进入编辑模式
                    if(!$(this).prop('checked')){
                        var $tr = $(this).parent().parent();
                        trIntoEdit($tr);
                        //设置选中
                        $(this).prop('checked',true);
                    };
                })//没有进入编辑模式的全选
                }else{
                    $('#tbBody').find(':checkbox').prop('checked',true);
                }
            });
            //反选按钮
            $('#checkReverse').click(function(){
                 if($('#inOutEditMode').hasClass('btn-warning')) {
                     $('#tbBody').find(':checkbox').each(function () {
                         var $tr = $(this).parent().parent();
                         if ($(this).prop('checked')) {
                             // $(this).prop('checked',false)
                             trOutEdit($tr);
                             $(this).prop('checked', false);
                         } else {
                             // $(this).prop('checked',true)
                             trIntoEdit($tr);
                             $(this).prop('checked', true);
                         }
                     })
                 }else{
                      $('#tbBody').find(':checkbox').each(function () {
                         var $tr = $(this).parent().parent();
                         if ($(this).prop('checked')) {
                             // $(this).prop('checked',false)
                             $(this).prop('checked', false);
                         } else {
                             // $(this).prop('checked',true)
                             $(this).prop('checked', true);
                         }
                     })
                 }
            });
            //取消按钮
            $('#checkCancel').click(function(){
                if($('#inOutEditMode').hasClass('btn-warning')) {
                    // $('#tbBody').find(':checkbox').prop('checked',false);
                    $('#tbBody').find(':checkbox').each(function () {
                        if ($(this).prop('checked')) {
                            var $tr = $(this).parent().parent();
                            trOutEdit($tr);
                            $(this).prop('checked', false);

                        };
                    })
                }else{
                    $('#tbBody').find(':checkbox').prop('checked',false);
                }
            });
            //进出编辑模式
            $('#inOutEditMode').click(function(){
                if($(this).hasClass('btn-warning')){
                    //退出编辑模式
                    $(this).removeClass('btn-warning');
                    $(this).text('进入编辑模式');
                    $('#tbBody').find(':checkbox').each(function () {
                        if ($(this).prop('checked')) {
                            var $tr = $(this).parent().parent();
                            trOutEdit($tr);
                        };
                    })
                }else{
                    //进入编辑模式
                    $(this).addClass('btn-warning');
                    $(this).text('退出编辑模式');

                     $('#tbBody').find(':checkbox').each(function () {
                        if ($(this).prop('checked')) {
                            var $tr = $(this).parent().parent();
                            trIntoEdit($tr);
                        };
                    })

                }
            });
            //批量删除
            $('#multiDel').click(function(){
                var idList = [];
                //$('#tbBody').find(':checkbox')表示找到所有的checkbox
                //$('#tbBody').find(':checked')表示找到checkbox下选中的input框

                $('#tbBody').find(':checked').each(function(){
                    var v = $(this).val();
                    idList.push(v);
                });
                console.log(idList);

                $.ajax({
                    url:url,
                    type:'delete',//大小写均可
                    // data:JSON.stringify(idList),
                    traditional:true,
                    data:idList,
                    success:function(arg){
                        console.log(arg);
                    }
                })
            });
            //刷新按钮
            $('#refresh').click(function(){
                initial(url);
            });
            //保存按钮
            $('#save').click(function(){
                //先退出编辑模式
                if($('#inOutEditMode').hasClass('btn-warning')){
                    $('#tbBody').find(':checkbox').each(function(){
                        if($(this).prop('checked')){
                            var $tr = $(this).parent().parent();
                            trOutEdit($tr);
                            $('#inOutEditMode').removeClass('btn-warning');
                        }
                    });
                };

                var all_list = [];
                //获取用户修改过的数据
                $('#tbBody').children().each(function() {
                    //$(this) = tr
                    var $tr = $(this);
                    var nid = $tr.attr('nid');
                    var row_dict = {};
                    var flag = false;

                    $tr.children().each(function () {
                        if ($(this).attr('edit-enable')) {
                            if($(this).attr('edit-type') == 'select'){
                                //select标签，如果newData与oldData不一致则表示修改过
                                var newData = $(this).attr('new-origin');
                                var oldData = $(this).attr('origin');

                                if(newData){
                                    if (newData != oldData) {
                                        var name = $(this).attr('name');
                                        console.log('==>>',$(this)[0]);
                                        row_dict[name] = newData;
                                        console.log('--',row_dict)
                                        flag = true;
                                    }
                                }
                                // console.log('>',newData,'<',oldData);


                            }else{
                                // console.log('==>>',$(this)[0]);

                                var newData = $(this).text();
                                var oldData = $(this).attr('origin');
                                console.log('p',$(this)[0])
                                // console.log('>?',newData,'<',oldData);

                                if (newData != oldData) {
                                    var name = $(this).attr('name');
                                    row_dict[name] = newData;
                                    flag = true;
                                    console.log('-->><<',row_dict)
                                }
                            }
                        }

                    });

                    if (flag) {
                        row_dict['id'] = nid;
                        all_list.push(row_dict);
                    }



                });

                //通过Ajax提交后台
                $.ajax({
                    url:url,
                    type:'PUT',
                    data:JSON.stringify(all_list),
                    success:function(arg){
                        console.log(arg);
                    }
                });
                console.log('>>',all_list);

            });

            //多条件查询搜索框，通过委托方式绑定事件，因是后来添加的li标签
            $('.search-list').on('click','li',function(){
                //点击li执行函数,$(this)为li标签
                var wenben = $(this).text();
                var searchType = $(this).attr('search_type');
                var name = $(this).attr('name');
                //只有select标签才有global_name属性,
                //没有而获取则为undefined即为空
                var globalName = $(this).attr('global_name');


                //默认搜索框的显示文本替换，从父级的上一个兄弟查找
                $(this).parent().prev().find('.searchDefault').text(wenben);
                //默认搜索框的标签替换
                if(searchType == 'select'){
                    var sel = document.createElement('select');
                    //设置样式
                    $(sel).attr('class','form-control');

                    //设置name便于数据提交后台时查询，name的key需与数据库一致
                    $(sel).attr('name',name);
                    //设置select下的option选项
                    $.each(GLOBAL_DICT[globalName],function(k,v){
                        var op = document.createElement('option');
                        $(op).text(v[1]);
                        $(op).val(v[0]);
                        $(sel).append(op);
                    });
                    //父级的父级的下一个移除，即移除原来的
                    $(this).parent().parent().next().remove();
                    //父级的父级的.after，即添加同级标签
                    $(this).parent().parent().after(sel);

                }else{
                    //input框设置
                    var inp = document.createElement('input');
                    $(inp).attr('class','form-control');
                    $(inp).attr('type','text');
                    $(inp).attr('name',name);
                    $(this).parent().parent().next().remove();
                    $(this).parent().parent().after(inp);

                }
            });
            //点击+号时会复制一份搜索框，通过委托事件实现绑定
            $('.search-list').on('click','.add-search-condition',function(){
                //拷贝新的搜索项
                var newSearchItem = $(this).parent().parent().clone();
                //添加新的搜索项的+号变成-号，即通过类实现
                $(newSearchItem).find('.add-search-condition span').removeClass('glyphicon-plus').addClass('glyphicon-minus');
                //添加新的搜索项的class由add-search-condition变成del-search-condition
                $(newSearchItem).find('.add-search-condition').addClass('del-search-condition').removeClass('add-search-condition');

                $('.search-list').append(newSearchItem)
            });
            //点击-号时会删除一份搜索框，通过委托事件实现绑定
            $('.search-list').on('click','.del-search-condition',function(){
                //删除新的搜索项
                $(this).parent().parent().remove();
            });

            //点击搜索按钮
            $('#doSearch').click(function(){
                /*
                var condition = {};
                $('.search-list').find('input[type="text"],select').each(function(){
                    // 获取所有的搜索条件
                    var name = $(this).attr('name');
                    var value = $(this).val();
                    if(condition[name]){
                        condition[name].push(value);
                    }else{
                        condition[name] = [value,];
                    }
                    // console.log('==',condition)

                });
                */

                initial(url);


            })

        }
    })
})(jQuery);