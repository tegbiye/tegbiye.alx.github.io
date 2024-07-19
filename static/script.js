$(window).on('load', function () {
  $(".trigger_popup_fricc").click(function(){
     $('.hover_bkgr_fricc').show();
  });
  $('.popupCloseButton').click(function(){
      $('.hover_bkgr_fricc').hide();
  });
});

function clientInfo(){
  document.getElementById("persnol-info-block").style.display="block";
  document.getElementById("request-block").style.display="none";
  document.getElementById("confirm-block").style.display="none";
    $.ajax({
      type: "GET",
      url: "getInfo",
      success: function (response) {
        document.getElementsByName("personName")[0].innerHTML="Name:    "+JSON.parse(response)[0].name;
        document.getElementsByName("mobile")[0].innerHTML="Mob#     "+JSON.parse(response)[0].mobile;
        document.getElementsByName("email")[0].innerHTML="Email:   "+JSON.parse(response)[0].email;
        document.getElementsByName("city")[0].innerHTML="City:    "+JSON.parse(response)[0].city;
        document.getElementsByName("pass")[0].innerHTML="Password:"+JSON.parse(response)[0].password;
      }
    });

  }
function loadmyJobs(){
$.ajax({
  type: "GET",
  url: "getMyJobs",
  success: function (response) {
    const requestBody=document.querySelector("#profile-table > tbody");
    console.log(requestBody);
    while(requestBody.firstChild){
      requestBody.removeChild(requestBody.firstChild);
    }
    var json=$.parseJSON(response)
    json.forEach(element => {
      const tr=document.createElement("tr");
      const td=document.createElement("td");
      const td1=document.createElement("td");
      const td2=document.createElement("td");
      const chawalBtn="<button class='red_btn' onclick='deleteAJob(this.parentNode.parentNode.id)'>Delete</button>";
      const td3=document.createElement("td");
      tr.id=element["job_id"];
     
      td.textContent=element['job_title'];
      tr.appendChild(td);
      td1.textContent=element['rate'];
      tr.appendChild(td1);
      td2.textContent=element['description'];
      tr.appendChild(td2);
      td3.insertAdjacentHTML("beforeend",chawalBtn);
      tr.appendChild(td3);
      requestBody.appendChild(tr);
    });
  }
});

}

function deleteAJob(jid){
  let deleteDataInfo={job_id:jid};
  $.ajax({
    type: "POST",
    url: "deleteMyJob",
    data: deleteDataInfo,
    
    success: function (response) {
      console.log(response);
      loadmyJobs();
    }
  });
}

function requestJobInfo(){
  document.getElementById("persnol-info-block").style.display="none";
  document.getElementById("confirm-block").style.display="none";
  document.getElementById("request-block").style.display="block";
}

function confirmJobInfo(){
  document.getElementById("persnol-info-block").style.display="none";
  document.getElementById("confirm-block").style.display="block";
  document.getElementById("request-block").style.display="none";
}

function loadConfirmTable() {
  $.ajax({
    type: "GET",
    url: "confirmData",
    success: function (response) {
      console.log(response);
      const requestBody=document.querySelector("#confirm-table > tbody");
      console.log(requestBody);
      while(requestBody.firstChild){
        requestBody.removeChild(requestBody.firstChild);
      }
      var json=$.parseJSON(response)
      json.forEach(element => {
        const tr=document.createElement("tr");
        const td=document.createElement("td");
        const td1=document.createElement("td");
        const td3=document.createElement("td");
        const td4=document.createElement("td");
        const slec=document.createElement("select");
        slec.id=element["job_id"]+","+element["worker_id"]+","+element["client_id"]+'1';
        const op=document.createElement("option");
        const op1=document.createElement("option");
        const op2=document.createElement("option");
        const op3=document.createElement("option");
        const op4=document.createElement("option");
        op.textContent="5";
        op1.textContent="4";
        op2.textContent="3";
        op3.textContent="2";
        op4.textContent="1";
        slec.appendChild(op);slec.appendChild(op1);slec.appendChild(op2);slec.appendChild(op3);slec.appendChild(op4);
        tr.id=element["job_id"]+","+element["worker_id"]+","+element["client_id"];
        const td2=document.createElement("td");
        td.textContent=element['job_title'];
        tr.appendChild(td);
        td1.textContent=element['name'];
        tr.appendChild(td1);
        td3.textContent=element['email'];
        tr.appendChild(td3);
       td4.appendChild(slec);
        tr.appendChild(td4);
        const chawalBtn="<button class='green_btn' onclick='complete(this.parentNode.parentNode.id)'>Complete</button>";
        td2.insertAdjacentHTML("beforeend",chawalBtn);
        tr.appendChild(td2);
        requestBody.appendChild(tr);
      });
    }
  });
}

function loadRequestTable(){
  $.ajax({
    type: "GET",
    url: "requestData",
    success: function (response) {
      console.log(response);
      const requestBody=document.querySelector("#request-table > tbody");
      console.log(requestBody);
      while(requestBody.firstChild){
        requestBody.removeChild(requestBody.firstChild);
      }
      var json=$.parseJSON(response)
      json.forEach(element => {
        const tr=document.createElement("tr");
        const td=document.createElement("td");
        const td1=document.createElement("td");
        const td2=document.createElement("td");
        const td3=document.createElement("td");
        const td4=document.createElement("td");
        const chawalBtn="<button class='red_btn' onclick='cancelit(this.parentNode.parentNode.id)'>Cancel</button>";
        tr.id=element["job_id"]+","+element["worker_id"]+","+element["client_id"];
        
        td.textContent=element['job_title'];
        tr.appendChild(td);
        td1.textContent=element['name'];
        tr.appendChild(td1);
        td3.textContent=element['email']
        tr.appendChild(td3);
        td4.textContent=element['city'];
        tr.appendChild(td4);
        td2.insertAdjacentHTML("beforeend",chawalBtn);
        tr.appendChild(td2);
        requestBody.appendChild(tr);
      });
    }
  });
}

function complete(ids) {
  var str=ids+"1";
  var e = document.getElementById(str);
  var rateing = e.options[e.selectedIndex].text;
  console.log(rateing);
  let singleId=String(ids).split(",");
  let completeJobInfo={job_id:singleId[0],worker_id:singleId[1],client_id:singleId[2],star:rateing};
  $.ajax({
    type: "POST",
    url: "closeTheJob",
    data: completeJobInfo,
    success: function (response) {
      console.log(response);
      loadConfirmTable();
      
    }
  });
}

function cancelit(idsCollection){

let ids=String(idsCollection).split(",");
let deleteDataInfo={job_id:ids[0],worker_id:ids[1],client_id:ids[2]};
$.ajax({
  type: "POST",
  url: "cancelRequest",
  data: deleteDataInfo,
  
  success: function (response) {
    console.log(response);
    loadRequestTable();
  }
});
}

function deleteit(idsCollection){

  let ids=String(idsCollection).split(",");
  console.log(ids);
  let deleteDataInfo={job_id:ids[0],worker_id:ids[1],client_id:ids[2]};
  $.ajax({
    type: "POST",
    url: "cancelRequest",
    data: deleteDataInfo,
    
    success: function (response) {
      console.log(response);
      loadWorkerRequestTable();
    }
  });
  }

function loadWorkerRequestTable(){
  console.log("kya masla ho gya")
  $.ajax({
    type: "GET",
    url: "requestDataForWorker",
    success: function (response) {
      const requestBody=document.querySelector("#request-table > tbody");
      console.log(requestBody);
      while(requestBody.firstChild){
        requestBody.removeChild(requestBody.firstChild);
      }
      var json=$.parseJSON(response)
      json.forEach(element => {
        const tr=document.createElement("tr");
        const td=document.createElement("td");
        const td1=document.createElement("td");
        const td4=document.createElement("td");
        const td2=document.createElement("td");
        const td3=document.createElement("td");
        const chawalBtn="<button class='red_btn' onclick='deleteit(this.parentNode.parentNode.id)'>Delete</button><button class='green_btn' onclick='acceptJob(this.parentNode.parentNode.id)'>Accept</button>";
        // const acceptBtn="<button onclick='cancelit(this.parentNode.parentNode.id)'>Accept</button>"
        tr.id=element["job_id"]+","+element["worker_id"]+","+element["user_id"];
       
        td.textContent=element['job_title'];
        tr.appendChild(td);
        td1.textContent=element['name'];
        tr.appendChild(td1);
        td3.textContent=element['email'];
        tr.appendChild(td3);
        td4.textContent=element['city'];
        tr.appendChild(td4);
        td2.insertAdjacentHTML("beforeend",chawalBtn);
        tr.appendChild(td2);
        // td3.insertAdjacentHTML("beforeend",acceptBtn);
        // tr.appendChild(td3);
        requestBody.appendChild(tr);
      });
    }
  });
}

function loadWorkerConfirmTable(){
  $.ajax({
    type: "GET",
    url: "confirmDataForWorker",
    success: function (response) {
      const requestBody=document.querySelector("#confirm-table > tbody");
      console.log(requestBody);
      while(requestBody.firstChild){
        requestBody.removeChild(requestBody.firstChild);
      }
      var json=$.parseJSON(response)
      json.forEach(element => {
        const tr=document.createElement("tr");
        const td=document.createElement("td");
        const td1=document.createElement("td");
        const td2=document.createElement("td");
        const td3=document.createElement("td");
        tr.id=element["job_id"]+","+element["worker_id"]+","+element["user_id"];
       
        td.textContent=element['job_title'];
        tr.appendChild(td);
        td1.textContent=element['name'];
        tr.appendChild(td1);
        td2.textContent=element['email'];
        tr.appendChild(td2);
        td3.textContent=element['city'];
        tr.appendChild(td3);
        requestBody.appendChild(tr);
      });
    }
  });
}

function acceptJob(idsCollection){
  let ids=String(idsCollection).split(",");
  console.log(ids);
  let DataInfo={job_id:ids[0],worker_id:ids[1],client_id:ids[2]};
  $.ajax({
    type: "POST",
    url: "acceptRequest",
    data: DataInfo,
    
    success: function (response) {
      console.log(response);
      deleteit(idsCollection);
    }
  });
}

function detailsShow(jid) {
  var jdata={id:jid}
  $.ajax({
    type: "GET",
    url: "jobDetails",
    data: jdata,
    success: function (response) {
      var details1=document.getElementsByClassName('details')[0];
      details1.classList.toggle('hide');
      document.getElementsByName("title")[0].innerHTML=JSON.parse(response)[0].job_title;
      document.getElementsByName("personName")[0].innerHTML="Name: "+JSON.parse(response)[0].name;
      document.getElementsByName("rating")[0].innerHTML="Rating &#9734;"+JSON.parse(response)[0].rating;
      document.getElementsByName("email")[0].innerHTML="Email: "+JSON.parse(response)[0].email;
      document.getElementsByName("mob")[0].innerHTML="Mob# "+JSON.parse(response)[0].mobile;
      document.getElementsByName("cty")[0].innerHTML="City: "+JSON.parse(response)[0].city;
      document.getElementsByName("rate")[0].innerHTML="Price: "+JSON.parse(response)[0].rate+"/hour";
      document.getElementsByName("desc")[0].innerHTML="Description: "+JSON.parse(response)[0].description;
      document.getElementsByName("jid")[0].setAttribute('value',JSON.parse(response)[0].job_id);
      document.getElementsByName("wid")[0].setAttribute('value', JSON.parse(response)[0].worker_id);
    }
  });
  
}
