from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Customer,Account,Transaction
from .serializers import CustomerSerializer,AccountSerializer,TransactionSerializer
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.http import Http404
# Create your views here.

# customer API
class CustomerListCreateApi(APIView):
    def get(self, request):
        customer = Customer.objects.all()
        serializer = CustomerSerializer(customer, many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    @csrf_exempt
    def post(self, request):
        serializer = CustomerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.data,status=status.HTTP_400_BAD_REQUEST)

# List,Update,Delete
class CustomerDetailsApi(APIView):
    def get_object(self,pk):
        try:
            return Customer.objects.get(pk=pk)
        except Customer.DoesNotExist:
            return None
     
    def get(self,request,pk):
        # customer = Customer.objects.get(pk=pk) OR
        customer=self.get_object(pk)
        if customer is None:
            return Response({"error": "Customer not found"},status=status.HTTP_404_NOT_FOUND)
        serializer = CustomerSerializer(customer)
        return Response(serializer.data,status=status.HTTP_200_OK)

    @csrf_exempt
    def put(self,request,pk):
        # customer = Customer.objects.get(pk=pk) OR
        customer=self.get_object(pk)
        if customer is None:
            return Response({"error": "Customer not found"},status=status.HTTP_404_NOT_FOUND)
        serializer = CustomerSerializer(customer,data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @csrf_exempt
    def delete(self,request,pk):
        customer = self.get_object(pk)
        if customer is None():
            return Response({"error": "Customer not found"},status=status.HTTP_404_NOT_FOUND)
        customer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# account api
class AccountListCreateApi(APIView):

    def get(self,request):
        account=Account.objects.all()
        serializer = AccountSerializer(account,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

    @csrf_exempt
    def post(self,request):
        serializer = AccountSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AccountDetailsApi(APIView):

    def get_object(self,pk):
        try:
            Account.objects.get(pk=pk)
        except Account.DoesNotExist:
            return None
    
    def get(self,request):
        account=self.get_object(pk)
        if account is None:
            return Response({"error": "Account not found"},status=status.HTTP_404_NOT_FOUND)
        serializer = AccountSerializer(account)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    @csrf_exempt
    def put(self,request,pk):
        account=self.get_object(pk)
        if account is None:
            return Response({"error": "account not found"},status=status.HTTP_404_NOT_FOUND)
        serializer = AccountSerializer(account, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @csrf_exempt
    def delete(self,request,pk):
        account = self.get_object(pk)
        if account is None():
            return Response({"error": "account not found"},status=status.HTTP_404_NOT_FOUND)
        account.delete()
        Response({
            "message": "Account deleted successfully."
        }, status=status.HTTP_204_NO_CONTENT)


class TransactionListCreateAPI(APIView):
    
    def get(self, request):
        transactions = Transaction.objects.all()
        serializer = TransactionSerializer(transactions, many=True)
        return Response({
            "message": "Transactions retrieved successfully.",
            "data": serializer.data
        }, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = TransactionSerializer(data=request.data)
        if serializer.is_valid():
            transaction_type=serializer.validated_data['transaction_type']
            amount=serializer.validated_data['amount']
            account=serializer.validated_data['account']

            if transaction_type == 'DEPOSIT':
                account.balance += amount
            elif transaction_type == 'WITHDRAW':
                if account.balance >= amount:
                    account.balance -= amount
                else:
                    return Response({
                        "message": "Insufficient balance.",
                        "errors": {"balance": "You cannot withdraw more than the available balance."}
                    }, status=status.HTTP_400_BAD_REQUEST)

            # Save the account balance update
            account.save(update_fields=['balance'])

            # Now save the transaction
            transaction = serializer.save()

            return Response({
                "message": "Transaction created successfully.",
                "data": TransactionSerializer(transaction).data
            }, status=status.HTTP_201_CREATED)

        return Response({
            "message": "Failed to create transaction.",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class TransactionDetailApi(APIView):
    
    def get_object(self, pk):
        try:
            return Transaction.objects.get(pk=pk)
        except Transaction.DoesNotExist:
            raise Http404  # Use Http404 for not found

    def handle_object_not_found(self):
        return Response({
            "message": "Transaction not found.",
            "error_code": "TRANSACTION_NOT_FOUND"
        }, status=status.HTTP_404_NOT_FOUND)

    def get(self, request, pk):
        try:
            transaction = self.get_object(pk)
            serializer = TransactionSerializer(transaction)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Http404:
            return self.handle_object_not_found()
    
    @csrf_exempt  # If needed; otherwise, consider removing this decorator
    def put(self, request, pk):
        try:
            transaction = self.get_object(pk)
            serializer = TransactionSerializer(transaction, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    "message": "Transaction updated successfully.",
                    "data": serializer.data
                }, status=status.HTTP_200_OK)
            return Response({
                "message": "Failed to update transaction.",
                "errors": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        except Http404:
            return self.handle_object_not_found()
    
    def delete(self, request, pk):
        try:
            transaction = self.get_object(pk)
            transaction.delete()
            return Response({
                "message": "Transaction deleted successfully."
            }, status=status.HTTP_204_NO_CONTENT)
        except Http404:
            return self.handle_object_not_found()

