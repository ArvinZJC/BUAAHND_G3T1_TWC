/*
 * JavaScript code that is related to "base2.html"
 * 
 * created on 28 October, 2018
 * 
 * author: Zhao Jichen and Ye Yifan
 */

//verify the submission from the dialog
function verifyDialogSubmit(array) {
	var i = 0, length = array.length, validata = true;
	for (i; i < length; i++) {
		var obj = array[i], _this = $(obj.id);
		validata = validate(obj, _this);
		if (!validata) {
			return validata;
		}
	}
	return validata;
} //end function verifyDialogSubmit

//do the validation task
function validate(obj, _this) {
	var tips = obj.tips, errorTips = obj.errorTips, regName = obj.regName, require = obj.require, repwd = obj.repwd, minlength = obj.minlength, strlength = obj.strlength, value = $
			.trim(_this.val());
	//validate NULL
	if (require && !value) {
		return Dml.fun.showValidateError(_this, tips);
	} else {
		if (regName && !Dml.regExp[regName].test(value)) {
			return Dml.fun.showValidateError(_this, errorTips);
		}

		//validate the minimum length
		if (minlength != undefined && value.length <= minlength) {
			return Dml.fun
					.showValidateError(_this, 'Need to be more than ' + minlength + ' characters!');
		}

		//validate the length
		if (strlength != undefined && value.length != strlength) {
			return Dml.fun
					.showValidateError(_this, 'Need to be' + strlength + ' characters!');
		}

		//validate the password entered again
		if (repwd != undefined && value != $(repwd).val()) {
			return Dml.fun.showValidateError(_this, Dml.Msg.erRePwd);
		}
	}
	_this.parent().removeClass('errorput');
	_this.parent().siblings('.error').hide();
	return true;
} //end function validate

$(function() {
	$('input[type=text]').focus(function() {
		$(this).parent().removeClass('errorput');
		$(this).parent().siblings('.error').hide();
	})
})