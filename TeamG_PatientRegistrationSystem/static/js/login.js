/*
 * JavaScript code that is related to "base2.html";
 * author: Zhao Jichen and Ye Yifan
 */

var zyemail = "", zyUname = "", zy_c_num = 60, zy_str = "";
var hash = {
	'qq.com' : 'http://mail.qq.com',
	'gmail.com' : 'http://mail.google.com',
	'sina.com' : 'http://mail.sina.com.cn',
	'163.com' : 'http://mail.163.com',
	'126.com' : 'http://mail.126.com',
	'yeah.net' : 'http://www.yeah.net/',
	'sohu.com' : 'http://mail.sohu.com/',
	'tom.com' : 'http://mail.tom.com/',
	'sogou.com' : 'http://mail.sogou.com/',
	'139.com' : 'http://mail.10086.cn/',
	'outlook.com' : 'http://www.hotmail.com',
	'live.com' : 'http://login.live.com/',
	'live.cn' : 'http://login.live.cn/',
	'live.com.cn' : 'http://login.live.com.cn',
	'189.com' : 'http://webmail16.189.cn/webmail/',
	'yahoo.com.cn' : 'http://mail.cn.yahoo.com/',
	'yahoo.cn' : 'http://mail.cn.yahoo.com/',
	'eyou.com' : 'http://www.eyou.com/',
	'21cn.com' : 'http://mail.21cn.com/',
	'188.com' : 'http://www.188.com/',
	'foxmail.com' : 'http://www.foxmail.com'
}; // email templates

// verify the email to activate the account
function zy_Countdown() {
	zy_c_num--;
	$(".sendE2 span").html(zy_c_num + "s");
	$(".zy_success span").html(zy_str);
	(zy_c_num < 58) && $(".zy_success").addClass("upmove");
	if (zy_c_num <= 0) {
		zy_c_num = 60;
		$(".sendE2").hide();
		$(".sendE").show()
		return false;
	}
	setTimeout("zy_Countdown()", 1000);
} // end function zy_Countdown

// refresh the verification code
function refresh_captcha(event) {
	$.get("/captcha/refresh/?" + Math.random(),
			function(result) {
				$('#' + event.data.form_id + ' .captcha').attr("src",
						result.image_url);
				$('#id_captcha_0').attr("value", result.key);
			});
	return false;
} // end function refresh_captcha

// submit the login form
function login_form_submit() {
	var $jsLoginBtn = $('#jsLoginBtn'), $jsLoginTips = $('#jsLoginTips'), $accountl = $("#account_l"), args = window.location.search
			.substr(1, window.location.search.length).split('&'), arg = [], verify = verifyDialogSubmit([
			{
				id : '#account_l',
				tips : Dml.Msg.epUserName,
				errorTips : Dml.Msg.erUserName,
				regName : 'username',
				require : true
			},{
				id : '#password_l',
				tips : Dml.Msg.epPwd,
				errorTips : Dml.Msg.erPwd,
				regName : 'pwd',
				require : true
			} ]);
	if (!verify) {
		return;
	}
	var autoLogin = false;
	if ($('#jsAutoLogin').is(':checked')) {
		autoLogin = true;
	}
	$.each(args, function(key, value) {
		arg = value.split('=');
		if (arg[0] == 'name') {
			return false;
		}
	});
	$
			.ajax({
				cache : false,
				type : 'post',
				dataType : 'json',
				url:"/user/login/",
				data : $('#jsLoginForm').serialize() + '&autologin='
						+ autoLogin + '&' + arg[0] + '=' + arg[1],
				async : true,
				beforeSend : function(XMLHttpRequest) {
					$jsLoginBtn.val("Logging in...");
					$jsLoginBtn.attr("disabled", "disabled");
				},
				success : function(data) {
					if (data.account_l) {
						Dml.fun.showValidateError($accountl, data.account_l);
					} else if (data.password_l) {
						Dml.fun.showValidateError($("#password_l"),
								data.password_l);
					} else {
						if (data.status == "success") {
							$('#jsLoginForm')[0].reset();
							window.location.href = data.url;
						} else if (data.status == "failure") {
							// execute if the account is not activated
							if (data.msg == 'no_active') {
								zyemail = $accountl.val();
								zyUname = zyemail;
								$('#jsEmailToActive').html(zyemail);
								var url = zyemail.split('@')[1], $jsGoToEmail = $('#jsGoToEmail');
								$jsGoToEmail.attr("href", hash[url]);
								if (undefined == hash[url] || hash[url] == null) {
									$jsGoToEmail.parent().hide();
								}
								Dml.fun.showDialog('#jsUnactiveForm');
							} else {
								$jsLoginTips.html("Incorrect username or password! Please re-enter!").show();
							}
						}
					}
				},
				complete : function(XMLHttpRequest) {
					$jsLoginBtn.val("Log In");
					$jsLoginBtn.removeAttr("disabled");
				}
			});
} // end function login_form_submit

// submit the form for getting back a password
function find_password_form_submit() {
	var $findPwdBtn = $("#jsFindPwdBtn"), $idAccount = $("#account");
	verify = verifyDialogSubmit([ {
		id : '#account',
		tips : Dml.Msg.epUserName,
		errorTips : Dml.Msg.erUserName,
		regName : 'phMail',
		require : true
	}, {
		id : '#find-password-captcha_1',
		tips : Dml.Msg.epVerifyCode,
		errorTips : Dml.Msg.erVerifyCode,
		regName : 'verifyCode',
		require : true
	} ]);
	if (!verify) {
		return;
	}

	$.ajax({
		cache : false,
		type : 'post',
		dataType : 'json',
		url : "/forget/",
		data : $('#jsFindPwdForm').serialize(),
		async : true,
		beforeSend : function(XMLHttpRequest) {
			$findPwdBtn.val("Submitting...")
			$findPwdBtn.attr("disabled", "disabled")
		},
		success : function(data) {
			refresh_captcha({
				"data" : {
					"form_id" : "jsFindPwdForm"
				}
			});
			if (data.account) {
				Dml.fun.showValidateError($idAccount, data.account);
			} else if (data.captcha_f) {
				Dml.fun.showValidateError($('#find-password-captcha_1'),
						data.captcha_f);
			} else {
				if ($idAccount.val().indexOf("@") > 0) {
					Dml.fun.showTipsDialog({
						title : 'Submission Succeeded',
						h2 : 'A verification link has been sent to the email address you provided (' + $idAccount.val()
								+ '). Please check your email now and click on the link to reset your password.'
					});
					$('#jsFindPwdForm')[0].reset();
					setTimeout(function() {
						window.location.href = window.location.href;
					}, 1500);
				} else {
					if (data.status == 'success') {
						$('#jsForgetTips').html("A verification code has been sent to your mobile. Please check your mobile.").show();
						$('#jsInpResetMobil').val($idAccount.val());
						setTimeout(function() {
							Dml.fun.showDialog('#jsSetNewPwd')
						}, 1500);
					} else if (data.status == 'failure') {
						$('#jsForgetTips').html("Failed to send a verification code to your mobile!").show();
					}
				}
			}
		},
		complete : function(XMLHttpRequest) {
			$findPwdBtn.val("Submit");
			$findPwdBtn.removeAttr("disabled");
		}
	});
} // end function find_password_form_submit

$('#jsSetNewPwdBtn').on('click', function() {
	var _self = $(this), $idAccount = $("#account");
	verify = verifyDialogSubmit([ {
		id : '#jsResetPwd',
		tips : Dml.Msg.epResetPwd,
		errorTips : Dml.Msg.erResetPwd,
		regName : 'pwd',
		require : true
	}, {
		id : '#jsResetPwd2',
		tips : Dml.Msg.epRePwd,
		repwd : '#jsResetPwd',
		require : true
	}, {
		id : '#jsResetCode',
		tips : Dml.Msg.epPhCode,
		errorTips : Dml.Msg.erPhCode,
		regName : 'phoneCode',
		require : true
	} ]);
	if (!verify) {
		return;
	}

	$.ajax({
		cache : false,
		type : 'post',
		dataType : 'json',
		url : "/mobile/resetpassword/",
		data : $('#jsSetNewPwdForm').serialize(),
		async : true,
		beforeSend : function(XMLHttpRequest) {
			_self.val("Submitting...")
			_self.attr("disabled", "disabled")
		},
		success : function(data) {
			if (data.status == 'success') {
				Dml.fun.showTipsDialog({
					title : 'Reset Succeeded',
					h2 : 'Succeeded to reset the password!'
				});
				$('#jsSetNewPwdForm')[0].reset();
				Dml.fun.winReload();
			} else if (data.status == 'faliuer') {
				Dml.fun.showTipsDialog({
					title : 'Reset Failed',
					h2 : data.msg,
					type : 'failbox'
				})
			} else if (data.code) {
				Dml.fun.showValidateError($('#jsResetCode'), data.code);
			}
		},
		complete : function(XMLHttpRequest) {
			_self.val("Submit");
			_self.removeAttr("disabled");
		}
	});
})

$(function() {
	// for IE 9
	function isPlaceholder() {
		var input = document.createElement('input');
		return 'placeholder' in input;
	} // end function isPlaceholder
	if (!isPlaceholder()) {
		$("input").not("input[type='password']").each(function() {
			if ($(this).val() == "" && $(this).attr("placeholder") != "") {
				$(this).val($(this).attr("placeholder"));
				$(this).focus(function() {
					if ($(this).val() == $(this).attr("placeholder"))
						$(this).val("");
				});
				$(this).blur(function() {
					if ($(this).val() == "")
						$(this).val($(this).attr("placeholder"));
				});
			}
		});
		$("textarea").each(function() {
			if ($(this).val() == "" && $(this).attr("placeholder") != "") {
				$(this).val($(this).attr("placeholder"));
				$(this).focus(function() {
					if ($(this).val() == $(this).attr("placeholder"))
						$(this).val("");
				});
				$(this).blur(function() {
					if ($(this).val() == "")
						$(this).val($(this).attr("placeholder"));
				});
			}
		});
		var pwdField = $("input[type=password]");
		var pwdVal = pwdField.attr('placeholder');
		pwdField.after('<input id="pwdPlaceholder" type="text" value=' + pwdVal
				+ ' autocomplete="off" />');
		var pwdPlaceholder = $('#pwdPlaceholder');
		pwdPlaceholder.show();
		pwdField.hide();

		pwdPlaceholder.focus(function() {
			pwdPlaceholder.hide();
			pwdField.show();
			pwdField.focus();
		});

		pwdField.blur(function() {
			if (pwdField.val() == '') {
				pwdPlaceholder.show();
				pwdField.hide();
			}
		});
	}

	$('.imgslide').unslider({
		speed : 500,
		delay : 3000,
		complete : function() {
		},
		keys : true,
		dots : true,
		fluid : false
	});
	var unslider = $('.imgslide').unslider();
	$('.unslider-arrow').click(function() {
		var fn = this.className.split(' ')[1];
		unslider.data('unslider')[fn]();
	});

	$('.tab > h2').click(
			function() {
				var _self = $(this), index = _self.index();
				_self.addClass('active').siblings().removeClass('active');
				$('.tab-form').eq(index).removeClass('hide').siblings(
						'.tab-form').addClass('hide');
			});

	$('input[type=text]').focus(function() {
		$(this).parent().removeClass('blur').addClass('focus');
	});
	$('input[type=text]').blur(function() {
		$(this).parent().removeClass('focus').addClass('blur');
	});
	$('input[type=password]').focus(function() {
		$(this).parent().removeClass('blur').addClass('focus');
	});
	$('input[type=password]').blur(function() {
		$(this).parent().removeClass('focus').addClass('blur');
	});

	// a button to close the dialog box
	$('.jsCloseDialog').on('click', function() {
		$(this).parents('.dialogbox').hide();
		$('#dialogBg').hide();
		if ($(this).siblings('form')[0]) {
			$(this).siblings('form')[0].reset();
		}
	});

	// refresh the verification code
	$('#email_register_form .captcha-refresh').click({
		'form_id' : 'email_register_form'
	}, refresh_captcha);
	$('#email_register_form .captcha').click({
		'form_id' : 'email_register_form'
	}, refresh_captcha);
	$('#mobile_register_form .captcha').click({
		'form_id' : 'jsRefreshCode'
	}, refresh_captcha);
	$('#changeCode').click({
		'form_id' : 'jsRefreshCode'
	}, refresh_captcha);
	$('#jsFindPwdForm .captcha-refresh').click({
		'form_id' : 'jsFindPwdForm'
	}, refresh_captcha);
	$('#jsFindPwdForm .captcha').click({
		'form_id' : 'jsFindPwdForm'
	}, refresh_captcha);
	$('#jsChangePhoneForm .captcha').click({
		'form_id' : 'jsChangePhoneForm'
	}, refresh_captcha);

	// log in
	$('#jsLoginBtn').on('click', function() {
		login_form_submit();
	})
	
	// the keyboard event for the login form
	$("#jsLoginForm").keydown(function(event) {
		if (event.keyCode == 13) {
			$('#jsLoginBtn').trigger('click');
		}
	});

	// sign up with an email
	$('#jsEmailRegBtn').on('click', function() {
		register_form_submit(this, 'emailReg');
	});
	$("#email_register_form").keydown(function(event) {
		if (event.keyCode == 13) {
			$('#jsEmailRegBtn').trigger('click');
		}
	});

	// the keyboard event for the password finding form
	$('#jsFindPwdBtn').on('click', function() {
		find_password_form_submit();
	});
	$("#jsFindPwdForm").keydown(function(event) {
		if (event.keyCode == 13) {
			$('#jsFindPwdBtn').trigger('click');
		}
	});

	// send a verification link to the user's email again
	$('#jsSenEmailAgin').on('click', function(e) {
		e.preventDefault();
		$(".zy_success").removeClass("upmove");
		$(this).parent().hide();
		$(".sendE2").show().find("span").html("60s");
		$.ajax({
			cache : false,
			type : 'get',
			dataType : 'json',
			url : "/send_again_email/",
			data : {
				username : zyUname
			},
			success : function(data) {
				zy_str = "Succeeded to send a verification link to your email again!";
				if (data)
					zy_Countdown();
			},
			error : function() {
				zy_str = "Failed to send a verification link to your email again!";
			}
		});
	});
});