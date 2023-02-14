function BindEmailCaptchaClick(){
    $("#captcha-btn").click(function (event){
        let $this = $(this) //当前按钮的jQuery对象
        // 阻止默认的事件
        event.preventDefault();

        let email = $("input[name = 'email']").val();

        $.ajax({
            url: "/auth/captcha/email?email="+email,
            method: "GET",
            success: function(result){
                if(result.code==200){
//                    alert("邮箱验证码发送成功")

                    $this.off("click");//取消按钮的点击事件

                    let countdown = 5;//显示倒计时
                    let time = setInterval(function(){
                        $this.text(countdown);
                        countdown -= 1;
                        if(countdown < 0){
                            //清掉定时器
                            clearInterval(time);
                            $this.text("获取验证码")
                            //重新绑定点击事件
                            BindEmailCaptchaClick()
                        }
                    },1000)
                }else{
                    alert(result.message)
                }
            },
            fail:function(error){
            }

        })
    })
}
$(  function(){ //等待所有标签全部载入后执行
    BindEmailCaptchaClick()
})