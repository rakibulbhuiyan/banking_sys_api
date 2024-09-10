from django.db import models
from django.db.models import F

# Create your models here.
class Customer(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15)
    address = models.TextField()
    date_of_birth = models.DateField()

    def __str__(self):
        return self.name

class Account(models.Model):
    customer=models.ForeignKey(Customer,on_delete=models.CASCADE,related_name='account')
    account_number=models.CharField(max_length=20,unique=True)
    account_type=models.CharField(max_length=20,choices=[('SAVINGS','Savings'),('CURRENT','Current')])
    balance = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.account_number


class Transaction(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='transactions')
    transaction_type = models.CharField(max_length=10, choices=[('DEPOSIT', 'Deposit'), ('WITHDRAW', 'Withdraw')])
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_date = models.DateTimeField(auto_now_add=True)

    # def save(self, *args, **kwargs):
    #     if self.transaction_type == 'DEPOSIT':
    #         self.account.balance += self.amount
    #     elif self.transaction_type == 'WITHDRAW':
    #         if self.account.balance >= self.amount:
    #             self.account.balance -= self.amount
    #         else:
    #             raise ValueError("Insufficient balance.")  # Add custom error handling if needed
    #     self.account.save(update_fields=['balance'])
    #     super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.transaction_type} - {self.amount}"