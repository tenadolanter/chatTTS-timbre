let fileUrl = "";
let timbreUrl = "";
$(document).ready(function () {
  // 文件上传事件
  $("#audio-file").on("change", function (e) {
    const file = e.target.files[0];
    if (!file) {
      return;
    }
    // 检查文件类型
    if (!file.type.startsWith("audio/")) {
      layer.msg("请上传音频文件", { icon: 2 });
      return;
    }
    // 上传文件
    const formData = new FormData();
    formData.append("audio_file", file);
    $("#loading-spinner").attr("style", "display: flex !important");
    $.ajax({
      url: "/upload",
      type: "POST",
      data: formData,
      processData: false,
      contentType: false,
      success: function (data) {
        // 处理上传成功的响应
        fileUrl = data;
        $("#loading-spinner").attr("style", "display: none !important");
        console.log(data);
      },
      error: function (xhr, status, error) {
        $("#loading-spinner").attr("style", "display: none !important");
        // 处理上传失败的情况
        layer.msg("上传失败: " + error, { icon: 2 });
      },
    });
  });
});

function uploadTimbre() {
  $("#audio-file").val("");
}

function downloadTimbre() {
  if (!timbreUrl) {
    layer.msg("没有可以下载的音色", { icon: 2 });
    return;
  }
  window.location.href = timbreUrl;
}

function generateTimbre() {
  const type = $('input[name="inlineRadioOptions"]:checked').val();
  console.log("type", type);
  if (!fileUrl) {
    layer.msg("请先上传音频文件", { icon: 2 });
    return;
  }
  $("#loading-spinner").attr("style", "display: flex !important");
  $.ajax({
    url: "/generate",
    type: "POST",
    data: {
      fileUrl: fileUrl,
      type: type,
    },
    success: function (data) {
      timbreUrl = data;
      $("#timbre-url").text(timbreUrl).css("display", "block");
      $("#loading-spinner").attr("style", "display: none !important");
    },
    error: function (xhr, status, error) {
      $("#loading-spinner").attr("style", "display: none !important");
      // 处理生成失败的情况
      layer.msg("生成失败: " + error, { icon: 2 });
    },
  });
}
