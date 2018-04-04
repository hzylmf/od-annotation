/**
 * 业务相关的JS处理代码
*/
sampleCount = 0;
sampleCurrentIndex = 1;
boxId = 1;
boxListOfSample = {}; //一张样本图片的标注集合(box_id为key)
$(function(){
    $('#total').text(sampleCount);
    loadSamplePic(sampleCurrentIndex);
    $('#side_left').click(function(){
        $('#btn_save').click();
        sampleCurrentIndex -= 1;
        if(sampleCurrentIndex<=0){
            sampleCurrentIndex = sampleCount;
        }
        loadSamplePic(sampleCurrentIndex);
    });
    $('#side_right').click(function(){
        $('#btn_save').click();
        sampleCurrentIndex += 1;
        if(sampleCurrentIndex>sampleCount){
            sampleCurrentIndex = 1;
        }
        loadSamplePic(sampleCurrentIndex);
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
                index = sampleCurrentIndex;
            }else if(index>sampleCount){
                index = sampleCount;
            }
            sampleCurrentIndex = index;
            loadSamplePic(index);
        }
    });
    $('#btn_save').click(function(){
        if (JSON.stringify(boxListOfSample) == '{}'){
            layer.msg('请先进行标注');
            return;
        }
        tagStrTotal = '';
        for(key in boxListOfSample){
            tagStrTotal+=boxListOfSample[key]+'\n';
        }
        saveRegionInfo(tagStrTotal);
        $('#cur_loc').html('');
        updateTotalTagStatus();
        boxId = 1;
        boxListOfSample = {};
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
		            if(index==0){
		                html += '<label class="radio-inline"><input type="radio" name="radio_region" checked="checked" id="'+id+'" value="'+value+'">';
		            }else{
		                html += '<label class="radio-inline"><input type="radio" name="radio_region" id="'+id+'" value="'+value+'">';
		            }
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

function loadSamplePic(index){
    picNumberStr = PrefixInteger(index,6);
    url = "/api/annotation/sample?index="+picNumberStr+'&time='+new Date();
    $('#img').css({"background":"url('"+url+"') no-repeat left top"});
    $('#cur_id').html(picNumberStr);
    $('.box').remove();
    $('#cur_loc').html('');
}

function saveRegionInfo(tagResult){
    $.ajax({
		type : "POST",
		dataType : "json",
		url : "/api/annotation/save?"+new Date(),
		data : {'tags':tagResult},
		beforeSend:function(){
		},
		success : function(result){
		    layer.msg(result.message);
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