const form = document.getElementById("expenseForm");

form.addEventListener("submit", async function(e){

e.preventDefault();

const category = document.getElementById("category").value;
const amount = document.getElementById("amount").value;
const date = document.getElementById("date").value;
const payment_mode = document.getElementById("payment_mode").value;

await fetch("http://127.0.0.1:5000/add-expense", {

method: "POST",

headers: {
"Content-Type": "application/json"
},

body: JSON.stringify({
category: category,
amount: amount,
date: date,
payment_mode: payment_mode
})

});

alert("Expense Added!");

});


async function loadExpenses(){

const response = await fetch("http://127.0.0.1:5000/expenses");

const data = await response.json();

const list = document.getElementById("expenseList");

list.innerHTML = "";

data.forEach(exp => {

const li = document.createElement("li");

li.className = "list-group-item";

li.innerText =
exp.date + " | " + exp.category + " | Rs " + exp.amount + " | " + exp.payment_mode;

list.appendChild(li);

});

}

function openDashboard(){
    alert("Open your Power BI dashboard file and click Refresh to see the latest data.");
}