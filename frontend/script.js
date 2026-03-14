let expenses = JSON.parse(localStorage.getItem("expenses")) || []

function addExpense(){

let name = document.getElementById("name").value
let amount = document.getElementById("amount").value
let category = document.getElementById("category").value

let expense = {
name:name,
amount:amount,
category:category
}

expenses.push(expense)

localStorage.setItem("expenses", JSON.stringify(expenses))

displayExpenses()

}

function displayExpenses(){

let list = document.getElementById("expenseList")

list.innerHTML = ""

expenses.forEach(function(exp){

let item = document.createElement("li")

item.textContent = exp.name + " - Rs" + exp.amount + " (" + exp.category + ")"

list.appendChild(item)

})

}

displayExpenses()