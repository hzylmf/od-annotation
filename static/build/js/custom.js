/**
 * 业务相关的JS处理代码
*/
ticketCount = 0;
ticketCurrentIndex = 1;
$(function(){
    $('#total').text(ticketCount);
    loadTicketPic(ticketCurrentIndex);
    $('#side_left').click(function(){
        $('#btn_save').click();
        ticketCurrentIndex -= 1;
        if(ticketCurrentIndex<=0){
            ticketCurrentIndex = ticketCount;
        }
        loadTicketPic(ticketCurrentIndex);
    });
    $('#side_right').click(function(){
        $('#btn_save').click();
        ticketCurrentIndex += 1;
        if(ticketCurrentIndex>ticketCount){
            ticketCurrentIndex = 1;
        }
        loadTicketPic(ticketCurrentIndex);
    });
    $(document).keyup(function(event){
      if (event.keyCode === 37){//left
        $('#side_left').click();
      }else if(event.keyCode === 39){//right
        $('#side_right').click();
      }
    });
    $('#jump_page').keypress(function(e){
        if(e.keyCode==13){
            var indexStr = $(this).val();
            index = parseInt(indexStr);
            if(index<=0 || indexStr==''){
                index = ticketCurrentIndex;
            }else if(index>ticketCount){
                index = ticketCount;
            }
            ticketCurrentIndex = index;
            loadTicketPic(index);
        }
    });
    $('#btn_save').click(function(){
        var picId = $('#cur_id').html();
        var regionLoc = $('#cur_loc').html();
        var regionClass = $('input[name="radio_region"]:checked').val();
        if(regionLoc=='') return;
        if(regionClass==null){
            layer.msg('请选择标注类别');
            return;
        }

        saveRegionInfo(picId,regionLoc,regionClass);
    });
    get_labels();
    $('#radio-type').click(function(){
        $(document).focus();
    });
});

function get_labels(){
    $.ajax({
		type : "GET",
		dataType : "json",
		url : "/api/annotation/labels?"+new Date(),
		beforeSend:function(){
		},
		success : function(result){
		    if(result.message=='success'){
		        var html = '标注类型：';
		        index = 0;
		        for (var i in result.data){
		            var id = 'region_'+result.data[i].name;
		            var value = result.data[i].name;
		            var text = result.data[i].desc;
		            html += '<label class="radio-inline"><input type="radio" name="radio_region" id="'+id+'" value="'+value+'">';
		            html += ' '+text+'</label>';
		            index++;
		        }
                $('#radio-type').html(html);
		    }
		},
		error: function(){
		}
	});
}

function loadTicketPic(index){
    picNumberStr = PrefixInteger(index,6);
    url = "/api/annotation/sample?index="+picNumberStr+'&time='+new Date();
    $('#ticket-img').css({"background":"url('"+url+"') no-repeat left top"});
    $('#cur_id').html(picNumberStr);
    $('.box').remove();
    $('#cur_loc').html('');
}

function saveRegionInfo(picId,regionLoc,regionClass){
    $.ajax({
		type : "POST",
		dataType : "json",
		url : "/api/annotation/save?"+new Date(),
		data : {"pic_id":picId, "region_loc":regionLoc,"region_class":regionClass},
		beforeSend:function(){
		},
		success : function(result){
		    layer.msg(result.message);
		    if(result.message=='success'){
		        var textarea = $('#annotation_status').append(picName+','+regionLoc+","+regionClass+" saved!\n");
		        textarea.scrollTop(textarea[0].scrollHeight - textarea.height());
		        $('#cur_loc').html('');
		    }
		},
		error: function(){
		}
	});
}

function isPassword(str) {
	var reg = /^(?![0-9]+$)(?![a-zA-Z]+$)[0-9A-Za-z]{6,15}/;
	return reg.test(str);
}

//时间戳转换成八位日期
function format2Date(uData){
	var myDate = new Date(uData);
	var year = myDate.getFullYear();
	var month = myDate.getMonth() + 1;
	var day = myDate.getDate();
	return year + '-' + month + '-' + day;
}

//时间戳转换成时间字符串
function format2Time(uData){
	var myDate = new Date(uData);
	var year = myDate.getFullYear();
	var month = myDate.getMonth() + 1;
	var day = myDate.getDate();
	var hour = myDate.getHours();
	var minute = myDate.getMinutes();
	var second = myDate.getSeconds();
	return year + '-' + month + '-' + day+' '+hour+':'+minute+':'+second;
}

function PrefixInteger(num, length) {
 return (Array(length).join('0') + num).slice(-length);
}