function addExpense(){

let name = document.getElementById("name").value
let amount = document.getElementById("amount").value
let category = document.getElementById("category").value

let list = document.getElementById("expenseList")

let item = document.createElement("li")

item.textContent = name + " - Rs" + amount + " (" + category + ")"

list.appendChild(item)

}