import uuid

from django.db import models
# Create your models here.


class BaseModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False, db_index=True)

    def delete(self):
        self.is_deleted = True
        self.save(update_fields=["is_deleted"])

    def restore(self):
        self.is_deleted = False
        self.save(update_fields=["is_deleted"])

    class Meta:
        abstract = True

class Customer(BaseModel):
    customer_id = models.UUIDField(max_length=100,default=uuid.uuid4 , db_index=True)
    name = models.CharField(max_length=100)
    email=models.EmailField()
    mobile=models.CharField(max_length=100)

    def __str__(self):
        return self.name

    def get_data(self):
        return{
            
            "customer_id":self.customer_id,
            "name":self.name,
            "email":self.email,
            "mobile":self.mobile,
        }


class Address(BaseModel):
    address_id=models.UUIDField(max_length=100,default=uuid.uuid4,db_index=True)
    addr1=models.CharField(max_length=300,null=True,blank=True)
    addr2=models.CharField(max_length=300,null=True,blank=True)
    pincode=models.CharField(max_length=100)
    is_default=models.BooleanField(default=False)
    customer=models.ForeignKey("core.Customer",on_delete=models.PROTECT)

    def __str__(self):
        return self.pincode

    def get_data(self):
        return{

            "address_id":self.address_id,
            "addr1":self.addr1,
            "addr2":self.addr2,
            "pincode":self.pincode,
            "is_default":self.is_default,
            "customer":self.customer.get_data()
        }

class Category(BaseModel):
    category_id=models.UUIDField(max_length=100,default=uuid.uuid4,db_index=True)
    name=models.CharField(max_length=100)
    des=models.CharField(max_length=200,null=True,blank=True)

    def __str__(self):
        return self.name

    def get_data(self):
        return{

            "category_id":self.category_id,
            "name":self.name,
            "des":self.des
        }

class SubCategory(BaseModel):
    subcategory_id=models.UUIDField(max_length=100,default=uuid.uuid4,db_index=True)
    name=models.CharField(max_length=100)
    category=models.ForeignKey("core.Category", on_delete=models.PROTECT)

    def __str__(self):
        return self.name

    def get_data(self):
        return{

            "subcategory_id":self.subcategory_id,
            "name":self.name,
            "category":self.category.get_data()
        }

class Product(BaseModel):
    product_id=models.UUIDField(max_length=100,default=uuid.uuid4,db_index=True)
    name=models.CharField(max_length=100)
    ram=models.CharField(max_length=100)
    num_of_products=models.IntegerField(default=0)
    price=models.CharField(max_length=100)
    category=models.ForeignKey("core.Category", on_delete=models.PROTECT,null=True)
    sub_category=models.ForeignKey("core.SubCategory", on_delete=models.PROTECT,null=True)

    def __str__(self):
        return self.name

    def get_data(self):
        return{
            
            "product_id":self.product_id,
            "name":self.name,
            "ram":self.ram,
            "num_of_products":self.num_of_products,
            "price":self.price,
            "category":self.category.get_data(),
            "subcategory":self.sub_category.get_data(),
        }


class AddToCart(BaseModel):
    cart_id=models.UUIDField(max_length=100,default=uuid.uuid4,db_index=True)
    num_of_products=models.IntegerField(default=0)
    customer=models.ForeignKey("core.Customer",related_name="cart_customer", on_delete=models.PROTECT)
    product=models.ForeignKey("core.Product",related_name="product_cartdata",on_delete=models.PROTECT)

    def __str__(self):
        return self.customer.email

    def get_data(self):
        return{

            "num_of_products":self.num_of_products,
            "customer":self.customer.get_data(),
            "product":self.product.get_data(),
        }