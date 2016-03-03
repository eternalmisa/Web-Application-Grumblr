$(document).ready(function(){
	setInterval(
		function(){
			if ($("#stream").text() == "follower"||$("#stream").text() == "global"||$("#stream").text() == "profile"){
				$.get("/grumblr/update_stream", {'time':$("#update_time").text()}, function(data){
					$("#update_time").text(data['update_time']);
					var messages = data['messages'];
					for (num in messages){
						var message = messages[num];
						if ($("#stream").text() == "follower" && message.isFollow == "False") { break; }
						var html = '<div class="grumblr-box">\
										<div class="grumblr" id="grumblr{{ message.id }}">\
											<img src="/grumblr/media/avatar/'+ message.user_id +'" class="img-circle user-picture" alt="photo">\
											<a href="/grumblr/profile/'+ message.user_id +'">'+ message.user_name +'</a>\
										</div>\
										<div class="post-time text-right">\
											<h6><span class="glyphicon glyphicon-time"></span> '+ message.timestamp +'</h6>\
										</div>\
										<p class="post-text">'+ message.text +'</p>';
										if (message.img != ""){
											html += '<img src="/grumblr/media/picture/' + message.mid +'" class="img-thumbnail post-picture center-block" alt="photo">';
										}
										html += '<div class="btn-group btn-group-justified" role="group" aria-label="...">\
                									<div class="btn-group" role="group">\
                    									<button type="button" class="btn btn-default commentBtn" data="' + message.mid +'">\
                        									<small><span class="glyphicon glyphicon-pencil" id="bar'+ message.mid +'"> Comment</span></small>\
                    									</button>\
                									</div>\
												</div>';
									// comment-box
									var csrftoken = getCookie('csrftoken');
									var html2 = '<div class="comment-box" style="display:none;" id="commentBox'+ message.mid +'">\
													<div align="center" id="errors'+ message.mid +'"></div>\
													<form class="comment-form" id="form'+ message.mid +'" action="/grumblr/comment/'+ message.mid +'" method="post">\
														<input type="hidden" name="id" value="'+ message.mid +'">\
														<input type="text" id="text'+ message.mid +'" class="form-control" placeholder="Type Your comment" name="text">\
														<input type="hidden" name="csrfmiddlewaretoken" value="'+ csrftoken +'">\
														<button type="submit" class="btn btn-info pull-right submitBtn btn-xs" value="'+ message.mid +'">Comment</button>\
													</form>\
													<div class="comment"><ol class="list-unstyled" id="comment'+ message.mid +'"></ol></div><br>\
												</div>';

						html += html2;
						html +='</div>';
						$("#stream-list").prepend(html);
						bindClickBtnListener(".commentBtn[data="+ message.mid +"]");
						bindCommentBtnListener(".submitBtn[value="+ message.mid +"]");
					}
				});
			}
		},
		5000);
	bindNavListListener();
	bindClickBtnListener(".commentBtn");
	bindCommentBtnListener(".submitBtn");
});

function bindNavListListener(){
	$("#drop").hover(function(){
		$("#nav-list").slideDown(200);
	}, 						function(){
		$("#nav-list").slideUp(200);
	});
}

function bindClickBtnListener(selector){
	$(selector).click(function() {
		var messageId=$(this).attr("data");
		$.get("/grumblr/get-comments/"+messageId, function(data){
			$("#text"+messageId).empty();
			$("#comment"+messageId).empty();
			$("#errors"+messageId).empty();
			var comments = data['comments'];
			for (cid in comments){
				var comment = comments[cid];
				var html = "<li><div class='small-line'></div><h6>"+ comment.time+"</h6>" +
					"<img class='img-circle small-picture'  src='/grumblr/media/avatar/"+ comment.uid +"' alt='photo'>" +
					"&nbsp;&nbsp;<a href='/grumblr/profile/"+ comment.uid +"'>"+ comment.username +"</a>&nbsp;said:&nbsp;"+ comment.text+"</li>";
				$("#comment"+messageId).append(html);
			}
		});
		//prompt(messageId);
		var commentBox = $('#commentBox'+messageId);
		if (commentBox.css("display") == "none") {
			commentBox.show();
		} else {
			commentBox.hide();
		}

	});
}

function bindCommentBtnListener(selector){
	$(selector).click(function() {
		var messageId=$(this).attr("value");
		var frm = $('#form'+messageId);
		var error = document.getElementById("errors"+messageId);
		$.ajax({
			type: frm.attr('method'),
			url:frm.attr('action'),
			async:true,
			data:frm.serialize(),
			success: function( context ) {
				if (context["error"]=="false") {
					$("#form" + messageId)[0].reset();
					var number = context["number"];
					var list = document.getElementById("comment"+messageId);
					var newItem = document.createElement("li");
					newItem.innerHTML = '<div class="small-line"></div>' +
					'<h6>'+ context["time"] +'</h6>' +
					'<img class="img-circle small-picture"  src="/grumblr/media/avatar/'+ context["writer_id"] +'" alt="photo">' +
					'&nbsp;&nbsp;<a href="/grumblr/profile/'+ context["writer_id"] +'">'+ context["writer_name"] +'</a>' +
					'&nbsp;said:&nbsp;'+ context["comment"] +'';
					list.appendChild(newItem);
					$("#error").empty();
				} else {
					var newError = document.createElement("li");
					newError.innerHTML = "<h5 class='error'>Your comment is invalid!</h5>";
                    error.appendChild(newError);
				}
			},
			error: function( context ) {
				alert( "Sorry, This message has been deleted by poster! Please refresh the page." );
			}
		});
		return false;
	});
}

function getCookie(cname) {
    var name = cname + "=";
    var ca = document.cookie.split(';');
    for(var i=0; i<ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0)==' ') c = c.substring(1);
        if (c.indexOf(name) == 0) return c.substring(name.length,c.length);
    }
    return "";
}
