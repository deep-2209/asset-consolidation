from django.urls import path

from .views import (
    create_supplier,
    create_buyer,
    create_season,
    create_drop,
    create_product,
    create_order,
    create_delivery,
    SupplierListView,
    BuyerListView,
    SeasonListView,
    DropListView,
    ProductListView,
    OrderListView,
    DeliveryListView,
    # DashboardView,
    update_supplier,
    delete_supplier,
    update_buyer,
    delete_buyer,
    update_season,
    delete_season,
    update_product,
    delete_product,
    download_pdf,
    dashboard
)

urlpatterns = [

    path('create-supplier/', create_supplier, name='create-supplier'),
    path('create-buyer/', create_buyer, name='create-buyer'),
    path('create-season/', create_season, name='create-season'),
    path('create-drop/', create_drop, name='create-drop'),
    path('create-product/', create_product, name='create-product'),
    path('create-order/', create_order, name='create-order'),
    path('create-delivery/', create_delivery, name='create-delivery'),

    path('supplier-list/', SupplierListView.as_view(), name='supplier-list'),
    path('buyer-list/', BuyerListView.as_view(), name='buyer-list'),
    path('season-list/', SeasonListView.as_view(), name='season-list'),
    path('drop-list/', DropListView.as_view(), name='drop-list'),
    path('product-list/', ProductListView.as_view(), name='product-list'),
    path('order-list/', OrderListView.as_view(), name='order-list'),
    path('delivery-list/', DeliveryListView.as_view(), name='delivery-list'),

    path('delete_supplier/<str:pk>', delete_supplier, name='delete_supplier'),
    path('update_supplier/<str:pk>', update_supplier, name='update_supplier'),
    
    path('delete_buyer/<str:pk>', delete_buyer, name='delete_buyer'),
    path('update_buyer/<str:pk>', update_buyer, name='update_buyer'),

    path('delete_season/<str:pk>', delete_season, name='delete_season'),
    path('update_season/<str:pk>', update_season, name='update_season'),

    # path('delete_drop/<str:pk>', delete_drop, name='delete_drop'),
    # path('update_drop/<str:pk>', update_drop, name='update_drop'),

    path('delete_product/<str:pk>', delete_product, name='delete_product'),
    path('update_product/<str:pk>', update_product, name='update_product'),
    
    path('download-pdf/', download_pdf, name='download_pdf'),

]
