const form = document.getElementById("expenseForm");

form.addEventListener("submit", async function(e){

e.preventDefault();

const category = document.getElementById("category").value;
const amount = document.getElementById("amount").value;
const date = document.getElementById("date").value;

await fetch("http://127.0.0.1:5000/add-expense", {

method: "POST",

headers: {
"Content-Type": "application/json"
},

body: JSON.stringify({
category: category,
amount: amount,
date: date
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

li.innerText =
exp[1] + " | " + exp[2] + " | Rs " + exp[3];

list.appendChild(li);

});

}