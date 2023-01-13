// location route check and navbar changes
var loc = window.location.href
var nav_delete_all = document.getElementById("deleteAll")
var nav_delete_todos_all = document.getElementById("deleteAllToDos")
if (loc.includes("notes")){
    nav_delete_all.style.display = "block"
} else {
    nav_delete_all.style.display = "none"
}
if (loc.includes("to-dos")){
    nav_delete_todos_all.style.display = "block"
}else{
    nav_delete_todos_all.style.display = "none"
}


// auto delete the todo if time's up
function deleteToDo(ToDoId){
    fetch('/account/auto-delete',{
        method : 'POST' , 
        body   :  JSON.stringify({ToDoId : ToDoId})
    });
}

// search_bar and live time counter 

let tests_search = document.getElementsByClassName("tm_search")
var test_search = Array.from(tests_search)
var box = document.getElementById("alert-box")
var search = document.getElementById("search-todos")
let dis_search = document.getElementById("display-search")
let dis_add = document.getElementById("display-addition")
let no_todo = document.getElementById("no-todo")
let search_results = document.getElementById("child-of-display-search")

if (no_todo != null){
    if (no_todo.innerText.startsWith("No")){
        search.disabled = true;
    }
}


search.addEventListener("input",async function(){
    let val = document.getElementById("search-todos").value
    val = val.toLowerCase()
    if (val == ""){
        dis_add.style.display = "block";
        dis_search.style.display = "none"
    }else{
        dis_add.style.display = "none";
        dis_search.style.display = "block";
        let response = await fetch("/account/search?q="+val)
        let todos = await response.json()
        let html = ""
        if (Object.keys(todos).length == 0){
            html += `<div class="col">
            <div class="card">
                <div class="card-body">
                    <h5>No <strong class="text-success">Todo</strong> results with : <strong class="text-primary">${val}</strong></h5>
                </div>
            </div>
        </div>`
        }else{
        for (let id in todos){
            let data = todos[id]
            // let todo = data[0].title.replace('<','&lt;').replace('&','&amp;')
            let todo = data[0]
            const firstLetter = todo.charAt(0)
            const firstLetterCap = firstLetter.toUpperCase()
            const remainingLetters = todo.slice(1)
            todo = firstLetterCap + remainingLetters
            console.log(data)
            console.log(id)
            html += `<div class="col">
                    <div class="card">
                        <div class="card-body">
                            <input value="key" type="hidden">
                            <nav class="navbar">
                                <h5 class="tmHead text-break" id="${id}">Only <span class="tim">${data[1]}</span> left</h5>
                                <h3 class="card-title mb-2 text-warning text-break">To ${todo}</h3>
                            </nav>
                        <form action="/remove" method="post">
                            <input type="hidden" value ="${id}" name="de">
                            <input type="submit" class="btn btn-primary" value="Finish!">
                        </form>
                        </div>
                    </div>
                </div>`
            }
            
        }
        search_results.innerHTML = html
        countdown();
    }
    
})


// live time counter for display to-dos screen
let tests = document.getElementsByClassName("tm")
var test = Array.from(tests)

for (var i = 0;i < test.length ; i ++){
(function(i) {
    var start = new Date;
    if (dis_search.style.display == "none"){
        wanted_time = test[i].innerText;
    }
    let timee = wanted_time.split(":")
    start.setHours(timee[0], timee[1], 0);
    start.setDate(timee[2])
    function pad(num) {
        return ("0" + parseInt(num)).substr(-2);
    }
    function tick() {
        var now = new Date;
        // start - now => the differences of milliseconds 
        // to get the actual second diffenerce , divide with 1000
        var remain = ((start - now) / 1000);
        var dd = pad((remain / 60 / 60  / 24) % 24);    
        var hh = pad((remain / 60  / 60) % 24);
        var mm = pad((remain / 60) % 60);
        var ss = pad(remain % 60);
        if (dd == 0){
            result = hh + ":" + mm + ":" + ss;
        }else{
            var day = parseInt(dd)
            result = `${hh} : ${mm} : ${ss} and ${day} Day(s)`
        }
        let time_diff = start-now
        if (time_diff < 0 || dd < 0 || hh < 0 || mm < 0 || ss < 0){
            result = "00" + ":" + "00" + ":" + "00"
        }
        test[i].innerHTML = result;
        let interval_id;
        interval_id = setTimeout(tick, 1000);
        if (test[i].innerHTML == "00" + ":" + "00" + ":" + "00"){
            clearTimeout(interval_id)
            let t = test[i].parentElement.getAttribute("id")
            test[i].parentElement.innerHTML = `<h4 style="color:red" id="">Sorry! Time's up</h4>`
            deleteToDo(t)
            console.log(t)
        }
    }

    document.addEventListener('DOMContentLoaded', tick);
})(i);
}

// live time countdown function

function countdown(){
    let search_times = document.getElementsByClassName("tim")
    var search_time = Array.from(search_times)
    for (var i = 0;i < search_time.length ; i ++){
        (function(i) {
            var start = new Date;
            wanted_time = search_time[i].innerText;
            let timee = wanted_time.split(":")
            start.setHours(timee[0], timee[1], 0);
            start.setDate(timee[2])
            function pad(num) {
                return ("0" + parseInt(num)).substr(-2);
            }
            function tick() {
                var now = new Date;
                // start - now => the differences of milliseconds 
                // to get the actual second diffenerce , divide with 1000
                var remain = ((start - now) / 1000);
                var dd = pad((remain / 60 / 60  / 24) % 24);    
                var hh = pad((remain / 60  / 60) % 24);
                var mm = pad((remain / 60) % 60);
                var ss = pad(remain % 60);
                if (dd == 0){
                    result = hh + ":" + mm + ":" + ss;
                }else{
                    var day = parseInt(dd)
                    result = `${hh} : ${mm} : ${ss} and ${day} Day(s)`
                }
                let time_diff = start-now
                console.log(dd,hh,mm,ss)
                if (time_diff < 0 || dd < 0 || hh < 0 || mm < 0 || ss < 0){
                    result = "00" + ":" + "00" + ":" + "00"
                }
                search_time[i].innerHTML = result;
                let interval_id;
                interval_id = setTimeout(tick, 1000);
                if (search_time[i].innerHTML == "00" + ":" + "00" + ":" + "00"){
                    clearTimeout(interval_id)
                    let t = search_time[i].parentElement.getAttribute("id")
                    search_time[i].parentElement.innerHTML = `<h4 style="color:red" id="">Sorry! Time's up</h4>`
                    deleteToDo(t)
                }
            }
    
            tick()
        })(i);
    }
    }