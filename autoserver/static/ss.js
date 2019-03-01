(function(jq){
        // console.log(jq);
    //为字符串创建format方法，用于字符串格式化
    String.prototype.format = function (args) {
        return this.replace(/\{(\w+)\}/g,function (s,i) {
            return args[i];
        })
    };
    function initial(url) {
        $.ajax({
            url:'/backend/curd_json.html',
            type:'GET',//获取数据
            dataType:'JSON',
            success:function (arg) {
                console.log(arg);
                /*
                {
                    'server_list':list(server_list),#所有的数据
                    'table_config':table_config，#所有的配置
                }

                */

                initTableHeader(arg.table_config);
                initTableBody(arg.server_list,arg.table_config);

            }
        })
    }
    function initTableHeader(tableConfig) {
        /*
        [
            {'q':'id','title':'ID'},
            {'q':'hostname','title':'主机名'},
        ]

        */

        $.each(tableConfig,function (k,v) {
            if (v.display){
                var tag = document.createElement('th');
                tag.innerHTML = v.title;
                $('#tbHead').find('tr').append(tag)
            }
        })
    }
    function initTableBody(serverList,tableConfig) {
        /*
         [
            {'id':1,'hostname':c2.com,create_at:'xxxx-xx-xx'},
            {'id':1,'hostname':c2.com,create_at:'xxxx-xx-xx'},
            {'id':1,'hostname':c2.com,create_at:'xxxx-xx-xx'},
         ]

        */

        $.each(serverList,function (k,row) {

            //row:{'id':1,'hostname':c2.com,create_at:'xxxx-xx-xx'},
            /*
            <tr>
                <td>1</td>
                <td>2</td>
                <td>3</td>
            </tr>
            */

            var tr = document.createElement('tr');
            $.each(tableConfig,function (kk,rrow) {

                //kk:1  rrow:{'q':'id','title':'ID'},//rrow.q = 'id'
                //kk: .  rrow:{'q':'hostname','title':'主机名'},//rrow.q = 'hostname'
                //kk: .  rrow:{'q':'create_at','title':'创建时间'},//rrow.q = 'create_at'

                if (rrow.display){
                    var td = document.createElement('td');
                    /*if(rrow['q']){
                        td.innerHTML = row[rrow.q];
                    }
                    else{
                        td.innerHTML = rrow.text;
                    }*/

                    //rrow.text.tpl = "abce{n1}sdf"
                    //rrow.text.kwargs = {'n1':'@id',n2':'123'}
                    var newKwars = {};//{'n1':1,n2':'123'}
                    $.each(rrow.text.kwargs,function (kkk,vvv) {
                        console.log(kkk,vvv)
                        var av = vvv;
                        if(vvv[0] == '@'){
                             av = row[vvv.substring(1,vvv.length)];//把@切除，即id的值,再通过serverList里的key获取

                        }
                        newKwars[kkk] = av;
                    });


                    var newText = rrow.text.tpl.format(newKwars);
                    td.innerHTML = newText;
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
    jq.extend({
        xx:function(arg){
            alert(arg)
        }
    });

})(jQuery);

