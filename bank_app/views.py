from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Customer,Account,Transaction
from .serializers import CustomerSerializer,AccountSerializer,TransactionSerializer
from django.views.decorators.csrf import csrf_exempt, csrf_protect
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

    @csrf_exempt
    def post(self, request):
        serializer = TransactionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "Transaction created successfully.",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response({
            "message": "Failed to create transaction.",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class TransactionDetailApi(APIView):
    
    def get_object(self,request,pk):
        try:
            return Transaction.objects.get(pk=pk)
        except Transaction.DoesNotExist:
            raise None

    def handle_object_not_found(self):
        return Response({
            "message": "Transaction not found.",
            "error_code": "TRANSACTION_NOT_FOUND"
        }, status=status.HTTP_404_NOT_FOUND)

    def get(self,request,pk):
        transaction=self.get_object(pk)
        if transaction is None:
            return self.handle_object_not_found()
        serializer = TransactionSerializer(transaction)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    @csrf_exempt
    def put(self,request,pk):
        transaction = self.get_object(pk)
        if transaction is None:
            return self.handle_object_not_found()
        serializer = TransactionSerializer(transaction,data=request.data)
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
    
    def delete(self,request,pk):
        transaction = self.get_object(pk)
        if transaction is None:
            return self.handle_object_not_found()
        transaction.delete()
        return Response({
            "message": "Transaction deleted successfully."
        }, status=status.HTTP_204_NO_CONTENT)

