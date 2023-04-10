from django.shortcuts import render

# Create your views here.
from django.http import Http404
from django.db.models import Sum

from rest_framework.views import APIView

from core import models as core_models
from core import serializers as core_serializers
from core import utils as core_utils


class CustomerViewset(APIView):
    def post(self,request):
        req_data=request.data
        serializer_instance = core_serializers.CustomerSerializer(data=req_data)
        if not serializer_instance.is_valid():
            return core_utils.create_response(serializer_instance.errors, 400)


        customer_instance=core_models.Customer.objects.create(
            name=serializer_instance.validated_data.get("name"),
            email=serializer_instance.validated_data.get("email"),
            mobile=serializer_instance.validated_data.get("mobile")

        )
        return core_utils.create_response(customer_instance.get_data(), 200)

    def get(self,request,customer_id=None):
        customer_instance = core_models.Customer.objects.filter(
            customer_id=customer_id
        ).last()

        return core_utils.create_response(customer_instance.get_data(), 200)

    def put(self,request,customer_id=None):
        req_data=request.data

        serializer_instance = core_serializers.UpdateCustomerViewSet(data=req_data)
        if not serializer_instance.is_valid():
            return core_utils.create_response(serializer_instance.errors, 400)

        customer_instance=core_models.Customer.objects.filter(
            customer_id=customer_id
        ).last()

        customer_instance.name=serializer_instance.validated_data.get("name")
        customer_instance.email=serializer_instance.validated_data.get("email")
        customer_instance.mobile=serializer_instance.validated_data.get("mobile")

        customer_instance.save(update_fields=["name","email","mobile"])

        return core_utils.create_response(customer_instance.get_data(), 200)

    def delete(self,request,customer_id=None):
        customer_instance=core_models.Customer.objects.filter(
            customer_id=customer_id
        ).last()
        if not customer_instance:
            raise Http404

        customer_instance.delete()

        return core_utils.create_response({"message":"Customer details are Deleted"}, 200)

class CategoryCreateViewset(APIView):
    def post(self,request):
        req_data=request.data

        serializer_instance=core_serializers.CategorySerializer(data=req_data)
        if not serializer_instance.is_valid():
            return core_utils.create_response(serializer_instance.errors, 400)

        category_instance=core_models.Category.objects.create(
            name=serializer_instance.validated_data.get("name"),
            des=serializer_instance.validated_data.get("des")
        )

        return core_utils.create_response(category_instance.get_data(), 200)

    def get(self,request,category_id=None):
        category_instance=core_models.Category.objects.filter(
            category_id=category_id
        ).last()
        if not category_instance:
            raise Http404

        return core_utils.create_response(category_instance.get_data(), 200)

    def put(self,request,category_id=None):
        req_data=request.data
        
        serializer_instance=core_serializers.UpdateCategorySerializer(data=req_data)
        if not serializer_instance.is_valid():
            return core_utils.create_response(serializer_instance.errors, 400)

        category_instance=core_models.Category.objects.filter(
            category_id=category_id
        ).last()
        if not category_instance:
            return core_utils.create_response({"message":"Category details NOT FOUND.. !"}, 400)

        category_instance.name=serializer_instance.validated_data.get("name")
        category_instance.des=serializer_instance.validated_data.get("des")

        category_instance.save(update_fields=["name","des"])

        return core_utils.create_response(category_instance.get_data(), 200)

    def delete(self,request,category_id=None):
        category_instance=core_models.Category.objects.filter(
            category_id=category_id
        ).last()
        if not category_instance:
            raise Http404

        category_instance.delete()
        return core_utils.create_response({"message":"Category data Deleted"}, 200)

class SubCategoryCreateViewset(APIView):
    def post(self,request,category_id):
        req_data=request.data

        serializer_instance=core_serializers.SubCategorySerializer(data=req_data)
        if not serializer_instance.is_valid():
            return core_utils.create_response(serializer_instance.errors, 400)

        category_instance=core_models.Category.objects.filter(
            category_id=category_id
        ).last()
        if not category_instance:
            raise Http404

        subcategory_instance=core_models.SubCategory.objects.create(
            name=serializer_instance.validated_data.get("name"),
            category=category_instance
        )

        return core_utils.create_response(subcategory_instance.get_data(), 200)

    def get(self,request,category_id=None):
        subcategory_instances=core_models.SubCategory.objects.filter(
            category__category_id=category_id
        ).last()
        if not subcategory_instances:
            raise Http404

        data = [obj_data.get_data() for obj_data in subcategory_instances]
        
        return core_utils.create_response(data, 200)

    def put(self,request,subcategory_id=None):
        req_data=request.data

        serializer_instance=core_serializers.UpdateSubCategorySerializer(data=req_data)
        if not serializer_instance.is_valid():
            return core_utils.create_response(serializer_instance.errors, 400)

        subcategory_instance=core_models.SubCategory.objects.filter(
            subcategory_id=subcategory_id
        ).last()

        subcategory_instance.name=serializer_instance.validated_data.get("name")

        subcategory_instance.save(update_fields=["name"])

        return core_utils.create_response(subcategory_instance.get_data(), 200)

    def delete(self,request,subcategory_id=None):
        subcategory_instance=core_models.SubCategory.objects.filter(
            subcategory_id=subcategory_id
        ).last()
        if not subcategory_instance:
            raise Http404

        subcategory_instance.delete()
        return core_utils.create_response({"message":"SubCategory data Deleted"}, 200)


class ProductCreateViewset(APIView):
    def post(self,request,category_id):
        req_data=request.data

        serializer_instance = core_serializers.ProductSerializer(data=req_data)
        if not serializer_instance.is_valid():
            return core_utils.create_response(serializer_instance.errors , 400)

        category_instance=core_models.Category.objects.filter(
            category_id=category_id
        ).last()
        if not category_instance:
            return core_utils.create_response({"message":"Category Details NOT FOUND..!!"})

        subcategory_instance=core_models.SubCategory.objects.filter(
            category=category_instance
        ).last()

        product_instance=core_models.Product.objects.create(
            name=serializer_instance.validated_data.get("name"),
            ram=serializer_instance.validated_data.get("ram"),
            num_of_products=serializer_instance.validated_data.get("num_of_products"),
            price=serializer_instance.validated_data.get("price"),
            category=category_instance,
            sub_category=subcategory_instance,
            
        )
        return core_utils.create_response(product_instance.get_data(), 200)

    def get(self,request,category_id=None):
        product_instances=core_models.Product.objects.filter(
            category__category_id=category_id
        )
        if not product_instances:
            raise Http404

        page_number=request.GET.get("page_number",1)
        page_size=request.GET.get("page_size",5)

        data = [obj_data.get_data() for obj_data in product_instances]

        product_instances = core_utils.pagination_on_queryset(
            data, page_number, page_size
        )

        return core_utils.create_response(product_instances, 200)

    def put(self,request,product_id=None):
        req_data=request.data

        serializer_instance = core_serializers.UpdateProductSerializer(data=req_data)
        if not serializer_instance.is_valid():
            return core_utils.create_response(serializer_instance.errors ,400)

        product_instance=core_models.Product.objects.filter(
            product_id=product_id
        ).last()
        if not product_instance:
            return core_utils.create_response({"message":"Product Details NOT FOUND..!"}, 400)

        product_instance.name=serializer_instance.validated_data.get("name")
        product_instance.ram=serializer_instance.validated_data.get("ram")
        product_instance.price=serializer_instance.validated_data.get("price")
        product_instance.num_of_products=serializer_instance.validated_data.get("num_of_products")

        product_instance.save(update_fields=['name','ram','price'])

        return core_utils.create_response(product_instance.get_data() ,200)

    def delete(self,request,product_id=None):
        product_instance=core_models.Product.objects.filter(
            product_id=product_id
        ).last()
        if not product_instance:
            raise Http404

        product_instance.delete()
        return core_utils.create_response({"message":"Product Data Deleted"}, 200)


class AddressViewset(APIView):
    def post(self,request,customer_id=None):
        req_data=request.data

        serializer_instance=core_serializers.AddressSerializer(data=req_data)
        if not serializer_instance.is_valid():
            return core_utils.create_response(serializer_instance.errors, 400)

        customer_instance=core_models.Customer.objects.filter(
            customer_id=customer_id
        ).last()
        if not customer_instance:
            return core_utils.create_response({"message":"Customer Details NOT FOUND..!"})

        address_instance=core_models.Address.objects.create(
            addr1=serializer_instance.validated_data.get("addr1"),
            addr2=serializer_instance.validated_data.get("addr2"),
            pincode=serializer_instance.validated_data.get("pincode"),
            is_default=serializer_instance.validated_data.get("is_default"),
            customer=customer_instance,
        )

        return core_utils.create_response(address_instance.get_data(), 200)

    def get(self,request,customer_id=None):
        address_instances=core_models.Address.objects.filter(
            customer__customer_id=customer_id
        )
        if not address_instances:
            raise Http404

        data = [obj_data.get_data() for obj_data in address_instances]
       
        return core_utils.create_response(data, 200)

    def delete(self,request,address_id=None):
        address_instance=core_models.Address.objects.filter(
            address_id=address_id
        ).last()
        if not address_instance:
            raise Http404

        address_instance.delete()
        return core_utils.create_response({"message":"Address data Deleted"} ,200)

    def put(self,request,address_id=None):
        req_data=request.data

        serializer_instance=core_serializers.UpdateAddressSerializer(data=req_data)
        if not serializer_instance.is_valid():
            return core_utils.create_response(serializer_instance.errors, 400)

        address_instance=core_models.Address.objects.filter(
            address_id=address_id
        ).last()

        address_instance.addr1=serializer_instance.validated_data.get("addr1")
        address_instance.addr2=serializer_instance.validated_data.get("addr2")
        address_instance.pincode=serializer_instance.validated_data.get("pincode")
        address_instance.is_default=serializer_instance.validated_data.get("is_default")

        address_instance.save(update_fields=["addr1","addr2","pincode","is_default"])

        return core_utils.create_response(address_instance.get_data(), 200)


class AddToCartViewset(APIView):
    def post(self,request,customer_id=None):
        req_data=request.data

        serializer_instance=core_serializers.AddToCartSerializer(data=req_data)
        if not serializer_instance.is_valid():
            return core_utils.create_response(serializer_instance.errors, 400)

        customer_instance=core_models.Customer.objects.filter(
            customer_id=customer_id
        ).last()
        if not customer_instance:
            raise Http404

        product_instance=core_models.Product.objects.filter(
            product_id=serializer_instance.validated_data.get("product_id")
        ).last()
        if not product_instance:
            return core_utils.create_response({"message":"Product data NOT FOUND..!"}, 400)

        cart = core_models.AddToCart.objects.filter(customer=customer_instance,product=product_instance).last()
        if cart:

            if not serializer_instance.validated_data.get("is_plus"):
                cart.num_of_products -= 1
                cart.save(update_fields=["num_of_products"])
                user_cart=[obj.get_data() for obj in core_models.AddToCart.objects.filter(customer=customer_instance)]

                return core_utils.create_response(user_cart, 200)
           
            total_cart_product = core_models.AddToCart.objects.filter(
                product=product_instance).aggregate(total=Sum('num_of_products'))

            if total_cart_product['total'] >= product_instance.num_of_products:
                return core_utils.create_response({"message":"Product are not in stock"}, 400)
            
            cart.num_of_products += 1
        
            cart.save(update_fields=["num_of_products"])
            return core_utils.create_response(cart.get_data(), 200)

        else:
            cart_instance=core_models.AddToCart.objects.create(
                num_of_products=1,
                customer=customer_instance,
                product=product_instance,
                
            )

            return core_utils.create_response(cart_instance.get_data(), 200)

    def get(self,request,customer_id=None):
        carts=[obj.get_data() for obj in core_models.AddToCart.objects.filter(
            customer__customer_id=customer_id
        )]

        total = 0

        num_of_products = ""
        for carts_data in carts:
            num_of_products=int(carts_data.get("product").get("num_of_products"))
            price=int(carts_data.get("product").get("price"))

            total = total + (num_of_products*price)

        return core_utils.create_response(
            {
            "carts":carts,
            "total_price":total
            }, 200)
