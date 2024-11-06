from datetime import datetime
import getpass
import pandas as pd

user_df = pd.DataFrame(columns=["Username", "Password","Reference"])

class User:


    
    def register_user(self, username ,password):
        self.username=username
        self.password=password

        global user_df
        

        print(self.username ," has been registered successfully")

        self.tracker=FinanceTracker()
          
        user_df.loc[len(user_df)] = {"Username": username, "Password": password, "Reference": self}

   
        self.tracker.showMenu(self.tracker)
    
    def user_login(self):
        print("\n\nLogin Successful !\n\n")
        self.tracker.showMenu(self.tracker)

    
class Transaction:
    def __init__(self, amount, description, category, date=None):
        self.amount = amount
        self.description = description
        self.category = category
        self.date = date if date else datetime.now()
        self.next = None  # Pointer to the next transaction
        self.prev=None

class Stack:
    def __init__(self):
        self.items = []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        if not self.is_empty():
            return self.items.pop()
        return None

    def is_empty(self):
        return len(self.items) == 0

class Queue:
    def __init__(self):
        self.items = []

    def is_empty(self):
        return len(self.items) == 0

    def enqueue(self, item):
        self.items.append(item)
    
    def dequeue(self):
        self.items.pop()

class LinkedList:
    def __init__(self):
        self.head = None

    def add_transaction(self, amount, description, category):
        new_transaction = Transaction(amount, description, category)
        if not self.head:
            self.head = new_transaction
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_transaction
            new_transaction.prev=current

    def display_transactions(self):
        if not self.head:
            print("No transactions recorded.")
            return
        
        print("\nTransaction History:")
        current = self.head
        while current and current.next:
            current=current.next
        while current:
            print(f"₹{abs(current.amount)} - {current.description} in {current.category} on {current.date.strftime('%Y-%m-%d')}")
            current=current.prev
        print()
        
            

class FinanceTracker:
    
    def __init__(self):
        self.history_ll=LinkedList()
        # self.expenses = LinkedList()  # Linked list for expenses
       # self.income = LinkedList()  # Linked list for income
        self.history = Stack()  # Stack for transaction history
        self.redo_stack = Stack()  # Stack for redo functionality
        self.category_queues = {
            "Food": Queue(),
            "Travel": Queue(),
            "Clothing": Queue(),
        }  # Queues for categorized expenses
        self.budget_limits = {}  # Dictionary for category budget limits
        self.prev_transaction = Stack()
    
    def add_new_category(self,category):
        flag = False
        for i in self.category_queues:
            if i == category:
                flag = True
                break
        
        if flag:
            print("\nCategory already exists\n")
        else:
            self.category_queues[category]=Queue() #creating new key value pair    

    def add_expense(self, amount, description, category):
        if category not in self.category_queues:
            print("Invalid category. Please choose from Food, Travel, or Clothing.")
            return
        
        new_expense = Transaction(-amount, description, category)

        #history linked list 
        self.history_ll.add_transaction(-amount,description,category)

        # Add to linked list of expenses
        #self.expenses.add_transaction(-amount, description, category)

        # Add to the respective category queue
        self.category_queues[category].enqueue(new_expense)

        self.history.push(("Expense", new_expense))
        self.redo_stack = Stack()  # Clear the redo stack when a new transaction is added

        self.prev_transaction = Stack()
        self.prev_transaction.push(("Expense",new_expense))
        print(f"Expense added: ₹{amount} for {description} in {category}")

    def add_income(self, amount, description):
        new_income = Transaction(amount, description, "Income")
        self.history_ll.add_transaction(amount, description , "Income")
        #self.income.add_transaction(amount, description, "Income")
        self.history.push(("Income", new_income))
        self.redo_stack = Stack()  # Clear the redo stack when a new transaction is added

        self.prev_transaction = Stack()
        self.prev_transaction.push(("Income",new_income))
        print(f"Income added: ₹{amount} from {description}")

    def view_categorized_expenses(self):
        for category, q in self.category_queues.items():
            print(f"\nExpenses in {category}:")
            if q.is_empty():
                print("  No expenses recorded")
            else:
                for expense in q.items:
                    print(f"  ₹{abs(expense.amount)} - {expense.description} on {expense.date.strftime('%Y-%m-%d')}")

    def calculate_balance(self):
        total_income = sum(transaction.amount for transaction in self.collect_transactions(self.income))
        total_expenses = sum(abs(transaction.amount) for transaction in self.collect_transactions(self.expenses))
        return total_income - total_expenses

    def collect_transactions(self, linked_list):
        transactions = []
        current = linked_list.head
        while current:
            transactions.append(current)
            current = current.next
        return transactions

    """def view_history(self):
        This code has been dicarded cuz it directly accesses the stack which should not be done
        if self.history.is_empty():
            print("No transaction history")
        else:
            print("Transaction History (Most recent first):")
            for transaction_type, transaction in reversed(self.history.items):
                print(f"{transaction_type}: ₹{abs(transaction.amount)} - {transaction.description} on {transaction.date.strftime('%Y-%m-%d')}")"""
    
    def view_transaction_by_date(self , year =None , month = None , day = None):
        if not self.head:
            print("No transactions recorded.")
            return
        
        print("\nTransaction History:")
        current = self.head
        while current and current.next:
            current=current.next
        
        while current:
            transaction_date = current.date

            if ((year is None or transaction_date.year == year) and (month is None or transaction_date.month == month) and (day is None or transaction_date.day == day)):
                print(f"₹{abs(current.amount)} - {current.description} in {current.category} on {transaction_date.strftime('%Y-%m-%d')}")

        current = current.prev

        




    def undo_last_transaction(self):
        if not self.history.is_empty():
            last_transaction = self.history.pop()  
            self.redo_stack.push(last_transaction)
            #print(last_transaction)
            self.prev_transaction = Stack()
            if last_transaction[0] == "Expense":
                self.remove_expense(last_transaction[1])
                self.category_queues[last_transaction[1].category].dequeue()
            elif last_transaction[0] == "Income":
                self.remove_income(last_transaction[1])
            print(f"Undid {last_transaction[0]}: ₹{abs(last_transaction[1].amount)} - {last_transaction[1].description}")
        else:
            print("No transactions to undo.")

    def redo_last_transaction(self):
        if not self.prev_transaction.is_empty():
            last_transaction = self.prev_transaction.pop()
            #self.history.push(last_transaction)
            if last_transaction[0] == "Expense":
                self.add_expense(abs(last_transaction[1].amount) , last_transaction[1].description,last_transaction[1].category)
            elif last_transaction[0] =="Income":
                self.add_income(last_transaction[1].amount,last_transaction[1].description)
            print(f"Redid {last_transaction[0]}: ₹{abs(last_transaction[1].amount)} - {last_transaction[1].description}")
        else:
            print("no transactions to undo")

    def redo_last_undid_transaction(self):
        if not self.redo_stack.is_empty():
            redo_transaction = self.redo_stack.pop()
            #self.history.push(redo_transaction)
            if redo_transaction[0] == "Expense":
                self.add_expense(abs(redo_transaction[1].amount), redo_transaction[1].description, redo_transaction[1].category)
            elif redo_transaction[0] == "Income":
                self.add_income(redo_transaction[1].amount, redo_transaction[1].description)
            print(f"Redid {redo_transaction[0]}: ₹{abs(redo_transaction[1].amount)} - {redo_transaction[1].description}")
        else:
            print("No transactions to redo.")

    def set_budget_alert(self, category, limit):
        if category in self.category_queues:
            self.budget_limits[category] = limit
            print(f"Budget alert set for {category}: ₹{limit}")
        else:
            print("Invalid category. Please choose from Food, Travel, or Clothing.")

    def view_budget_alerts(self):
        for category, limit in self.budget_limits.items():
            total_spent = sum(abs(expense.amount) for expense in self.category_queues[category].items)
            if total_spent > limit:
                print(f"Exceeded budget for {category} by ₹{total_spent - limit:.2f}")
            else:
                print(f"Remaining budget for {category}: ₹{limit - total_spent:.2f}")

    """ def remove_expense(self, expense):
        if not self.history_ll.head:
            return
        
        current = self.history_ll.head
        
        # If the head is the expense to be removed
        if current == expense:
            self.history_ll.head = current.next
            if current.next:
                current.next.prev = None  # Update the previous pointer of the new head
            return
        
        # Traverse the list to find the expense
        while current.next:
            if current.next == expense:
                current.next = current.next.next  # Bypass the expense node
                if current.next:  # If there is a next node, update its prev pointer
                    current.next.prev = current
                return
            current = current.next """
    
    def remove_expense(self,expense):
        if not self.history_ll.head:
            return
    
        # If there's only one node, remove it
        if not self.history_ll.head.next:
            self.history_ll.head = None
            return
        
        # Traverse to the end of the list
        current = self.history_ll.head
        while current.next:
            current = current.next
        
        # Update the second-last node's next pointer to None
        if current.prev:
            current.prev.next = None


    def remove_income(self, income):
        if not self.history_ll.head:
            return
    
        # If there's only one node, remove it
        if not self.history_ll.head.next:
            self.history_ll.head = None
            return
        
        # Traverse to the end of the list
        current = self.history_ll.head
        while current.next:
            current = current.next
        
        # Update the second-last node's next pointer to None
        if current.prev:
            current.prev.next = None


    """ def remove_income(self, income):
        if not self.history_ll.head:
            return
        
        current = self.history_ll.head """

    def showMenu(self ,user_tracker):
        tracker = user_tracker

        print("FINANCE TRACKER APPLICATION")
        while True:
            print("\n1. Add Income")
            print("2. Expense Options")
            print("3. View Categorized Expenses")
            print("4. Set custom category")
            print("5. Set Budget Alert")
            print("6. View Budget Alerts")
            print("7. View Transaction History")
            print("8. View Transactions by date")
            print("9. Quit")
            choice = input("Choose an option: ")
            
            if choice == "1":
                amount = float(input("Enter income amount: "))
                description = input("Enter income description: ")
                tracker.add_income(amount, description)
            elif choice == "2":
                while True:
                    print("\n Expense Menu \n")
                    print("\n1. Add New Expense")
                    print("2. Undo Last Expense")
                    print("3. Redo Last Undid Expense")
                    print("4. Redo last transaction")
                    print("5. Quit")
                    sub_choice = input("Choose an option: ")
                    
                    if sub_choice == "1":
                        amount = float(input("Enter expense amount: "))
                        description = input("Enter expense description: ")
                        category = input("Enter expense category (Food, Travel, Clothing): ")
                        tracker.add_expense(amount, description, category)
                    elif sub_choice == "2":
                        tracker.undo_last_transaction()
                    elif sub_choice == "3":
                        tracker.redo_last_undid_transaction()
                    elif sub_choice == "4":
                        tracker.redo_last_transaction()
                    elif sub_choice == "5":
                        break
                    else:
                        print("Invalid option")
            elif choice == "3":
                tracker.view_categorized_expenses()
            elif choice == "4":
                category = input("Enter category name: ")
                tracker.add_new_category(category)
            elif choice == "5":
                category = input("Enter category for budget alert: ")
                limit = float(input("Enter budget limit: "))
                tracker.set_budget_alert(category, limit)
            elif choice == "6":
                tracker.view_budget_alerts()
            elif choice == "7":
                tracker.history_ll.display_transactions()
            elif choice == "8":
                print("quit the application successfully")
                homepage()
            else:
                print("Invalid option")


def register():
    username=input("Enter username: ")
    password=getpass.getpass("enter password: ")
    u=User()
    u.register_user(username,password)

def login():
    username=input("Enter username")
    password=getpass.getpass("enter password")
    user_exists = not user_df[(user_df["Username"] == username) & (user_df["Password"] == password)].empty

    if user_exists:
        user_row = user_df[(user_df["Username"] == username) & (user_df["Password"] == password)]
        user_ref = user_row["Reference"].values[0]
        user_ref.user_login()
    else:
        print("Invalid login credintials")


def homepage():
    print("HOMEPAGE")

    print("Enter 1 to register")
    print("Enter 2 to login")
    
    choice =input("enter choice: ")

    if choice=="1":
        register()
    
    elif choice=="2":
        login()
    
    else:
        print("Invalid choice")
        print("Redirecting to homepage......")
        homepage()
    
    

homepage()
