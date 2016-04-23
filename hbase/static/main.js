
window.onload = function() {
	var a = document.getElementById("conn");
	a.value = "default_conn";
	var b = document.getElementById("l_table");
	b.value = "default_tbl";
	var c = document.getElementById("l_rklist");
	c.value = "default_rk"
	document.getElementById("t_table").value = "default_tbl";
	document.getElementById("appkey").value = "default_rk";
	document.getElementById("dt").value = "2016-04-15";
}

$.myFunc = {
	appuserstat : function() {
		var dt = arguments[0][1].trim(), appkey = arguments[0][2].trim(), chan = arguments[0][3]
				.trim(), ver = arguments[0][4].trim();
		var a = dt + '_' + appkey;

		if (arguments[0].length == 5) {
			if (chan != '' && ver != '') {
				a = a + '&&' + chan + '\x1F##' + ver;
			} else if (chan != '') {
				a = a + '&&' + chan;
			} else if (ver != '') {
				a = a + '##' + ver;
			}
		}
		return $.md5(a).slice(0, 4) + '_' + a;
	},

	getRowkey : function() {
		var tbl = arguments[0];
		var fn = eval('$.myFunc.' + tbl)
		if ($.isFunction(fn)) {
			this.func = function() {
			};
			this.func = fn;
			var rs = this.func(arguments) + "";
			return rs;
		}
	}
}

$(document).ready(
		function() {

			$("#btn-get").click(function() {
				var input = {
					conn : $("#conn").val().trim(),
					tbl : $("#l_table").val().trim(),
					rk : $("#l_rklist").val().trim(),
					cols : $("#l_cols").val().trim()
				};
				if (input.tbl == '' || input.rk == '' || input.conn == '') {
					console.log("Empty tbl or rk or conn");
					return false;
				}
				$.ajax({
					type : 'POST',
					url : '/hbase/ajax_getData/',
					data : input,
					dataType : 'json',
					cache : 'false',
					success : function(data) {
						$('#ltext')[0].value = JSON.stringify(data, null, 4);
					}
				})
			});

			$("#btn-top")
					.click(
							function() {
								var tbl = $("#t_table").val().trim(), dt = $(
										"#dt").val().trim(), appkey = $(
										"#appkey").val().trim(), chan = $(
										"#chan").val().trim(), ver = $("#ver")
										.val().trim();
								$("#rowkey")[0].value = $.myFunc.getRowkey(tbl,
										dt, appkey, chan, ver)
										+ "";
							});

			$("#btn-add").click(function() {
				var rowkey = $("#rowkey").val();
				if ($("#l_rklist")[0].value.trim() == '') {
					$("#l_rklist")[0].value = rowkey;
				} else {
					$("#l_rklist")[0].value += (',' + rowkey);
				}

			});

			$("#btn-copy").click(function() {
				$("#r_table")[0].value = $("#l_table")[0].value.trim();
				$("#r_cols")[0].value = $("#l_cols")[0].value.trim();
				$("#r_rklist")[0].value = $("#l_rklist")[0].value.trim();
				$("#rtext")[0].value = $("#ltext")[0].value.trim().replace(/\\u00(\w{2})/g,"\\x$1");
			});

			$("#btn-fire").click(
					function() {
						var input = {
							conn : $("#conn").val().trim(),
							tbl : $("#r_table").val().trim(),
							rk : $("#r_rklist").val().trim()
						};
						var method = $('input:radio[name=type]:checked').val();
						var urlstr = '';
						if (method == 'PUT') {
							urlstr = '/hbase/ajax_put/';
							if ($("#rtext").val().trim() == '') {
								console.log("Empty rtext");
								return false;
							}
//							try {
//								$.parseJSON($("#rtext").val());
//							} catch (e) {
//								alert("Incorrect JSON format.");
//								return false;
//							}
							input.input = $("#rtext").val();
						} else if (method == 'DEL') {
							urlstr = '/hbase/ajax_del/';
							input.cols = $("#r_cols").val().trim();
						} else {
							console.log("Incorrect method:" + method);
							return false;
						}
						if (input.tbl.trim() == '' || input.rk.trim() == '') {
							console.log("Empty tbl or rk");
							return false;
						}
						
						$("#log")[0].innerHTML = "progress..." + "\t"
						+ new Date().toLocaleTimeString();
						
						$.ajax({
							type : 'POST',
							url : urlstr,
							data : input,
							dataType : 'json',
							cache : 'false',
							success : function(data) {
								$("#log")[0].innerHTML = JSON.stringify(data)
										+ "\t"
										+ new Date().toLocaleTimeString();
							},
							error : function(data) {
								$("#log")[0].innerHTML = "unexpected error"
								+ "\t"
								+ new Date().toLocaleTimeString();
					        }
						})

					});

		})

function plainSwitch() {
	var b = document.getElementById("plain").checked;
	try {
		var obj1 = jQuery.parseJSON($("#ltext").val());
	} catch (e) {
		alert("Incorrect JSON format.");
		return false;
	}
	if (b) {
		$("#ltext")[0].value = JSON.stringify(obj1);
	} else {
		$("#ltext")[0].value = JSON.stringify(obj1, null, 4);
	}
}

function wrapSwitch() {
	var b = document.getElementById("wrap").checked;
	if (b) {
		document.getElementById("ltext").wrap = "virtual";
	} else {
		document.getElementById("ltext").wrap = "off";
	}
}
