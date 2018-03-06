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
        var picName = $('#cur_id').html();
        var regionLoc = $('#cur_loc').html();
        var regionClass = $('input[name="radio_region"]:checked').val();
        if(regionLoc=='') return;
        saveRegionInfo(picName,regionLoc,regionClass);
    });
});

function loadTicketPic(index){
    picNumberStr = PrefixInteger(index,6);
    url = "/static/dataset/"+picNumberStr+".jpg?"+new Date();
    console.log(url);
    $('#ticket-img').css({"background":"url('"+url+"') no-repeat left top"});
    $('#cur_id').html(picNumberStr+'.jpg');
    $('.box').remove();
    $('#cur_loc').html('');
}

function saveRegionInfo(picName,regionLoc,regionClass){
    $.ajax({
		type : "POST",
		dataType : "json",
		url : "/api/annotation/save?"+new Date(),
		data : {"pic_name":picName, "region_loc":regionLoc,"region_class":regionClass},
		beforeSend:function(){
		},
		success : function(result){
		    layer.msg(result.message);
		    if(result.message=='success'){
		        var textarea = $('#annotation_status').append(picName+','+regionLoc+","+regionClass+" saved!\n");
		        textarea.scrollTop(textarea[0].scrollHeight - textarea.height());
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