
function doUpvote(answer_id) {  
  var xhttp = new XMLHttpRequest();  
  var url = "/upvote/"+answer_id;
  xhttp.onreadystatechange = function() {
    if(xhttp.readyState == 4 && xhttp.status==200) {
      var resp = xhttp.responseText;
      if(resp=='unauthorized') {
        alert("You need to login to vote");
      } else if(resp=='false') {
        alert("you have already submitted your vote");
      } else {
        document.getElementById("nofupvotes"+answer_id).innerHTML = "+"+resp;
      }
    }
  }
  xhttp.open("POST", url, true);
  xhttp.send();
}


function doDownvote(answer_id) {  
  var xhttp = new XMLHttpRequest();  
  var url = "/downvote/"+answer_id;
  xhttp.onreadystatechange = function() {
    if(xhttp.readyState == 4 && xhttp.status==200) {      
      var resp = xhttp.responseText;
      if(resp=='unauthorized') {
        alert("You need to login to vote");
      } else if(resp=='false') {
        alert("you have already submitted your vote");
      } else {
        document.getElementById("nofdownvotes"+answer_id).innerHTML = "-"+resp;
      }
    }
  }
  xhttp.open("POST", url, true);
  xhttp.send();
}



//COMMENTS part
function submitCommentForQuestion(question_id) {
  var xhttp = new XMLHttpRequest();  
  var comment = document.getElementById('question_comment_'+question_id).value;  
  var url = "/comment_question/"+question_id;
  xhttp.onreadystatechange = function() {
    if(xhttp.readyState == 4 && xhttp.status==200) {
      var resp = xhttp.responseText;
      if(resp=='unauthorized') {
        alert("You need to login to comment");
      } else {        
        //refresh page
        location.reload();
      }
    }
  }
  xhttp.open("POST", url, true);
  xhttp.send("comment="+comment);
}

function submitCommentForAnswer(answer_id) {
  var xhttp = new XMLHttpRequest();  
  var url = "/comment_answer/"+answer_id;
  var comment = document.getElementById('answer_comment_'+answer_id).value;    
  xhttp.onreadystatechange = function() {
    if(xhttp.readyState == 4 && xhttp.status==200) {
      var resp = xhttp.responseText;
      if(resp=='unauthorized') {
        alert("You need to login to comment");
      } else {
        //refresh page
        location.reload();
      }
    }
  }
  xhttp.open("POST", url, true);
  xhttp.send("comment="+comment);
}
