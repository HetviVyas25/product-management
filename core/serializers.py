
from rest_framework import serializers
from core import models as core_models


def validate_customer_id(self,value):
    customer_instance = core_models.Customer.objects.filter(
        customer_id=value).last()
    if not customer_instance:
        raise serializers.ValidationError("Invalid Customer ID")

    return value

class CustomerSerializer(serializers.Serializer):
    name=serializers.CharField(max_length=100)
    email=serializers.EmailField()
    mobile=serializers.CharField(max_length=100)


class UpdateCustomerViewSet(serializers.Serializer):
    name=serializers.CharField(max_length=100)
    email=serializers.EmailField()
    mobile=serializers.CharField(max_length=100)

    def validate_customer_id(self,value):
        return validate_customer_id(self,value)
        

def validate_category_id(self,value):
    category_instance=core_models.Category.objects.filter(
        category_id=value).last()
    if not category_instance:
        raise serializers.ValidationError("Invalid Category ID")


class CategorySerializer(serializers.Serializer):
    name=serializers.CharField(max_length=100)
    des=serializers.CharField(max_length=100,required=False,allow_null=True,allow_blank=True)


    def validate_name(self,value):
        is_category_name=core_models.Category.objects.filter(
            name=value).exists()

        if is_category_name:
            raise serializers.ValidationError("Category Already exists")

        return value

class UpdateCategorySerializer(serializers.Serializer):
    name=serializers.CharField(max_length=100)
    des=serializers.CharField(max_length=100,required=False,allow_null=True,allow_blank=True)

    def validate_category_id(self,value):
        return validate_category_id(self,value)

class AddressSerializer(serializers.Serializer):
    addr1=serializers.CharField(max_length=300)
    addr2=serializers.CharField(max_length=300,required=False,allow_null=True,allow_blank=True)
    pincode=serializers.CharField(max_length=100)
    is_default=serializers.BooleanField(default=False)

def validate_address_id(self,value):
    address_instance = core_models.Address.objects.filter(
        address_id=value).last()
    if not address_instance:
        raise serializers.ValidationError("Invalid Address ID")

    return value


class UpdateAddressSerializer(serializers.Serializer):
    addr1=serializers.CharField(max_length=300)
    addr2=serializers.CharField(max_length=300,required=False,allow_null=True,allow_blank=True)
    pincode=serializers.CharField(max_length=100)
    is_default=serializers.BooleanField(default=False)

    def validate_address_id(self,value):
        return validate_address_id(self,value)

def validate_subcategory_id(self,value):
    subcategory_instance=core_models.SubCategory.objects.filter(
        subcategory_id=value).last()
    if not subcategory_instance:
        raise serializers.ValidationError("Invalid SubCategory ID")


class SubCategorySerializer(serializers.Serializer):
    name=serializers.CharField(max_length=100)

    def validate_name(self,value):
        is_subcategory_name=core_models.SubCategory.objects.filter(
            name=value).exists()

        if is_subcategory_name:
            raise serializers.ValidationError("Sub Category Already exists")

        return value


class UpdateSubCategorySerializer(serializers.Serializer):
    name=serializers.CharField(max_length=100)

    def validate_subcategory_id(self,value):
        return validate_subcategory_id(self,value)


def validate_product_id(self,value):
    product_instance=core_models.Product.objects.filter(
        product_id=value).last()
    if not product_instance:
        raise serializers.ValidationError("Invalid Product ID")

    return value

class ProductSerializer(serializers.Serializer):
    name=serializers.CharField(max_length=100)
    ram=serializers.CharField(max_length=100)
    num_of_products=serializers.IntegerField(default=0)
    price=serializers.CharField(max_length=100)

    def validate_name(self,value):
        is_product_name=core_models.Product.objects.filter(
            name=value).exists()

        if is_product_name:
            raise serializers.ValidationError("Product Already exists")

        return value


class UpdateProductSerializer(serializers.Serializer):
    name=serializers.CharField(max_length=100)
    ram=serializers.CharField(max_length=100)
    num_of_products=serializers.IntegerField(default=0)
    price=serializers.CharField(max_length=100)

    def validate_product_id(self,value):
        return validate_product_id(self,value)
        

class AddToCartSerializer(serializers.Serializer):
    product_id=serializers.UUIDField()
    is_plus=serializers.BooleanField(default=False)

    def validate_category_id(self,value):
        return validate_category_id(self,value)

    def validate_product_id(self,value):
        return validate_product_id(self,value)
