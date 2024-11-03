import matplotlib.pyplot as plt

from datetime import datetime

class Transaction:
    def __init__(self, amount, description, category, date=None):
        self.amount = amount
        self.description = description
        self.category = category
        self.date = date if date else datetime.now()
        self.next = None  # Pointer to the next transaction

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
        if(self.is_empty()):
            print("no elements to dequeue")
        else:
            self.items.pop()
            

class LinkedList:
    def __init__(self):
        self.head = None

    def add_transaction(self, new_transaction ):
        
        if not self.head:
            self.head = new_transaction
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_transaction

    def display_transactions(self):
        if not self.head:
            print("No transactions recorded.")
            return
        
        print("\nTransaction History:")
        current = self.head
        while current:
            print(f"₹{abs(current.amount)} - {current.description} in {current.category} on {current.date.strftime('%Y-%m-%d')}")
            current = current.next

class FinanceTracker:
    def __init__(self):
        self.expenses = LinkedList()  # Linked list for expenses
        self.income = LinkedList()  # Linked list for income
        self.history = Stack()  # Stack for transaction history
        self.redo_stack = Stack()  # Stack for redo functionality
        self.category_queues = {
            "Food": Queue(),
            "Travel": Queue(),
            "Clothing": Queue(),
        }  # Queues for categorized expenses
        self.budget_limits = {}  # Dictionary for category budget limits

    def add_expense(self, amount, description, category):
        if category not in self.category_queues:
            print("Invalid category. Please choose from Food, Travel, or Clothing.")
            return
        
        new_expense = Transaction(-amount, description, category)

        # Add to linked list of expenses
        self.expenses.add_transaction(new_expense)

        # Add to the respective category queue
        self.category_queues[category].enqueue(new_expense)

        self.history.push(("Expense", new_expense))
        self.redo_stack = Stack()  # Clear the redo stack when a new transaction is added
        print(f"Expense added: ₹{amount} for {description} in {category}")

    def add_income(self, amount, description):
        new_income = Transaction(amount, description, "Income")
        self.income.add_transaction(new_income)
        self.history.push(("Income", new_income))
        self.redo_stack = Stack()  # Clear the redo stack when a new transaction is added
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

    def view_history(self):
        if self.history.is_empty():
            print("No transaction history")
        else:
            print("Transaction History (Most recent first):")
            for transaction_type, transaction in reversed(self.history.items):
                print(f"{transaction_type}: ₹{abs(transaction.amount)} - {transaction.description} on {transaction.date.strftime('%Y-%m-%d')}")

    def undo_last_transaction(self):
        if not self.history.is_empty():
            last_transaction = self.history.pop()
            self.redo_stack.push(last_transaction)
            if last_transaction[0] == "Expense":
                """ self.remove_expense(last_transaction[1]) """

                curr=self.expenses.head

                if curr is None:
                    print("no transactions to undo")
                elif curr.next is None:
                    self.expenses.head=None
                    category=last_transaction[1].category
                    self.category_queues[category].dequeue()
                else:
                    while curr.next.next is not None :
                        curr=curr.next
                    curr.next=None
                    category=last_transaction[1].category
                    self.category_queues[category].dequeue()
            
            elif last_transaction[0] == "Income":
                curr=self.income.head
                if curr is None:
                    print("no transactions to undo")
                elif curr.next is None:
                    self.income.head=None
                else:
                    while curr.next.next is not None :
                        curr=curr.next
                    curr.next=None
                """ self.remove_income(last_transaction[1]) """

            print(f"Undid {last_transaction[0]}: ₹{abs(last_transaction[1].amount)} - {last_transaction[1].description}")
        else:
            print("No transactions to undo.")

    def redo_last_transaction(self):
        if not self.redo_stack.is_empty():
            redo_transaction = self.redo_stack.pop()
            self.history.push(redo_transaction)
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
    
    def calculate_total_expenditures(self):
        """Calculate total expenditure for each category and overall."""
        category_totals = {category: 0 for category in self.category_queues}
        total_expenditure = 0
        
        for category, q in self.category_queues.items():
            category_total = sum(abs(expense.amount) for expense in q.items)
            category_totals[category] = category_total
            total_expenditure += category_total

        return category_totals, total_expenditure

    def plot_categorized_spending_pie_chart(self):
        """Generate a pie chart for categorized spending."""
        category_totals, _ = self.calculate_total_expenditures()
        
        # Filter out categories with zero spending
        non_zero_categories = {k: v for k, v in category_totals.items() if v > 0}
        
        if non_zero_categories:
            plt.figure(figsize=(8, 8))
            plt.pie(non_zero_categories.values(), labels=non_zero_categories.keys(), autopct='%1.1f%%')
            plt.title("Categorized Spending")
            plt.show()
        else:
            print("No expenditures to display.")

    def plot_income_vs_expenditure(self):
        """Generate a bar chart comparing total income and expenditure."""
        _, total_expenditure = self.calculate_total_expenditures()
        total_income = sum(transaction.amount for transaction in self.collect_transactions(self.income))

        plt.figure(figsize=(6, 6))
        plt.bar(['Income', 'Expenditure'], [total_income, total_expenditure], color=['green', 'red'])
        plt.title("Total Income vs. Expenditure")
        plt.ylabel("Amount (₹)")
        plt.show()

    def plot_budget_limits(self):
        """Generate a bar chart comparing category spending against budget limits."""
        category_totals, _ = self.calculate_total_expenditures()
        
        categories = []
        spent_amounts = []
        limits = []

        for category, limit in self.budget_limits.items():
            categories.append(category)
            spent_amounts.append(category_totals.get(category, 0))
            limits.append(limit)

        if categories:
            plt.figure(figsize=(8, 6))
            bar_width = 0.35
            index = range(len(categories))

            plt.bar(index, spent_amounts, bar_width, label="Spent", color="orange")
            plt.bar([i + bar_width for i in index], limits, bar_width, label="Limit", color="blue")

            plt.xlabel("Categories")
            plt.ylabel("Amount (₹)")
            plt.title("Category Spending vs. Budget Limits")
            plt.xticks([i + bar_width / 2 for i in index], categories)
            plt.legend()
            plt.show()
        else:
            print("No budget limits set to display.")
            
    def plot_category_spending_bar_chart(self):
        """Generate a bar chart showing spending in each subcategory."""
        category_totals, _ = self.calculate_total_expenditures()
        
        categories = list(category_totals.keys())
        spent_amounts = list(category_totals.values())

        plt.figure(figsize=(8, 6))
        bars = plt.bar(categories, spent_amounts, color="purple")

        plt.xlabel("Categories")
        plt.ylabel("Amount Spent (₹)")
        plt.title("Spending in Each Category")

        # Add amount spent on top of each bar
        for bar in bars:
            yval = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2, yval, f"₹{yval}", ha='center', va='bottom')

        plt.show()


"""     def remove_expense(self, expense):
        if not self.expenses.head:
            return
        current = self.expenses.head
        if current == expense:
            self.expenses.head = current.next
            return
        while current.next:
            if current.next == expense:
                current.next = current.next.next
                return
            current = current.next

    def remove_income(self, income):
        if not self.income.head:
            return
        current = self.income.head
        if current == income:
            self.income.head = current.next
            return
        while current.next:
            if current.next == income:
                current.next = current.next.next
                return
            current = current.next """



def main():
    tracker = FinanceTracker()
    
    # Existing main function code for menu-based options ...

    while True:
        print("\n1. Add Income")
        print("2. Add Expenses")
        print("3. View Categorized Expenses")
        print("4. Set Budget Alert")
        print("5. View Budget Alerts")
        print("6. View Transaction History")
        print("7. Generate Spending Charts")
        print("8. Quit")
        choice = input("Choose an option: ")
        
        if choice == "1":
            amount = float(input("Enter income amount: "))
            description = input("Enter income description: ")
            tracker.add_income(amount, description)
        elif choice == "2":
            amount = float(input("Enter expense amount: "))
            description = input("Enter expense description: ")
            category = input("Enter expense category (Food, Travel, Clothing): ")
            tracker.add_expense(amount, description, category)
        elif choice == "3":
            tracker.view_categorized_expenses()
        elif choice == "4":
            category = input("Enter category for budget alert: ")
            limit = float(input("Enter budget limit: "))
            tracker.set_budget_alert(category, limit)
        elif choice == "5":
            tracker.view_budget_alerts()
        elif choice == "6":
            tracker.view_history()
        elif choice == "7":
            print("\n1. View Pie Chart")
            print("2. View Income vs Expenditure")
            print("3. View Budget Limits")
            print("4. View Spending in Each Category (Bar Chart)")
            chart_choice = input("Choose a chart option: ")
            if chart_choice == "1":
                tracker.plot_categorized_spending_pie_chart()
            elif chart_choice == "2":
                tracker.plot_income_vs_expenditure()
            elif chart_choice == "3":
                tracker.plot_budget_limits()
            elif chart_choice == "4":
                tracker.plot_category_spending_bar_chart()
            else:
                print("Invalid chart option.")
        elif choice == "8":
            break
        else:
            print("Invalid option.")

if __name__ == "__main__":
    main()