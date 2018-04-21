$(function(e){
  e = e || window.event;
  // startX, startY 为鼠标点击时初始坐标
  // diffX, diffY 为鼠标初始坐标与 box 左上角坐标之差，用于拖动
  var startX, startY, diffX, diffY;
  // 是否拖动，初始为 false
  var dragging = false;
  var draw_obj = $('#img');
  // 鼠标按下
  document.onmousedown = function(e) {
      startX = e.pageX;
      startY = e.pageY;

      // 如果鼠标在 box 上被按下
      if(e.target.className.match(/box/)) {
          // 允许拖动
          dragging = true;

          // 设置当前 box 的 id 为 moving_box
          if(document.getElementById("moving_box") !== null) {
              document.getElementById("moving_box").removeAttribute("id");
          }
          e.target.id = "moving_box";

          // 计算坐标差值
          diffX = startX - e.target.offsetLeft;
          diffY = startY - e.target.offsetTop;
      }
      else if(e.target.className.indexOf("img-main")!=-1){// 如果鼠标在 样本区域 被按下
          // 在页面创建 box
          var active_box = document.createElement("div");
          active_box.id = "active_box";
          active_box.setAttribute("box_id",'box_'+boxId); // 设置
          boxId++;
          active_box.className = "box";
          active_box.style.position = 'absolute';
          active_box.style.top = startY + 'px';
          active_box.style.left = startX + 'px';
          document.body.appendChild(active_box);
          active_box = null;
      }
  };

  //右键移除该矩形框
  document.oncontextmenu = function(e){
    // 如果鼠标在 box 上按下右键
    if(e.target.className.match(/box/)) {
      document.body.removeChild(e.target);
      delete boxListOfSample[$(e.target).attr('box_id')];
      updateCurTagStatus();
      $('#cur_loc').html('');
      //不继续传递右键事件，即不弹出菜单
      return false;
    }
    return true;
  };

  // 鼠标移动
  document.onmousemove = function(e) {
      // 更新 box 尺寸
      if(document.getElementById("active_box") !== null) {
          var ab = document.getElementById("active_box");
          ab.style.width = e.pageX - startX + 'px';
          ab.style.height = e.pageY - startY + 'px';
      }

      // 移动，更新 box 坐标
      if(document.getElementById("moving_box") !== null && dragging) {
          var mb = document.getElementById("moving_box");
          mb.style.top = e.pageY - diffY + 'px';
          mb.style.left = e.pageX - diffX + 'px';
      }
  };

  // 鼠标抬起
  document.onmouseup = function(e) {
      // 禁止拖动
      dragging = false;
      if(document.getElementById("active_box") !== null) {
          var ab = document.getElementById("active_box");
          ab.removeAttribute("id");
          // 如果长宽均小于 3px，移除 box
          if(ab.offsetWidth < 3 || ab.offsetHeight < 3) {
              document.body.removeChild(ab);
          }else{
              updateLoc(ab);
              $(ab).html('<div class="box_label">'+$('input[name="radio_region"]:checked').parent().text()+"</div>");
          }
      }else if(document.getElementById("moving_box") !== null) {
        var ab = document.getElementById("moving_box");
        updateLoc(ab);
      }
  };

  function updateLoc(obj){
    img = document.getElementById("img");
    x_left = obj.offsetLeft - img.offsetLeft;
    y_left = obj.offsetTop - img.offsetTop;
    x_right = x_left + $(obj).width();
    y_right = y_left + $(obj).height();
    var regionLoc = x_left+','+y_left+','+x_right+','+y_right;
    $('#cur_loc').html(regionLoc);
    var picId = $('#cur_id').html();
    var regionClass = $('input[name="radio_region"]:checked').val();
    tagStr = picId+','+regionLoc+","+regionClass;
    box_id = $(obj).attr('box_id');
    boxListOfSample[box_id] = tagStr;
    updateCurTagStatus();
  }
});

function updateCurTagStatus(){
    tagStrTotal = '';
    for(key in boxListOfSample){
        tagStrTotal+=boxListOfSample[key]+'\n';
    }
    var textarea = $('#annotation_cur_status').val(tagStrTotal);
    textarea.scrollTop(textarea[0].scrollHeight - textarea.height());
}

function updateTotalTagStatus(){
    tagStrTotal = '';
    for(key in boxListOfSample){
        tagStrTotal+=boxListOfSample[key]+'\n';
    }
    var textarea = $('#annotation_total_status').append(tagStrTotal);
    textarea.scrollTop(textarea[0].scrollHeight - textarea.height());
}