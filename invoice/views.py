from django.http import HttpResponse
from django.views.generic import View
from .utils import render_to_pdf
from datetime import date
from django.views.decorators.csrf import csrf_exempt
import json
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
cred = credentials.Certificate('serviceKey.json')
firebase_admin.initialize_app(cred)
db = firestore.client()
@csrf_exempt
def GeneratePdf(request):
    data = json.loads(request.body.decode('utf-8'))
    order_ref = db.collection(u'orders').document(data["id"])
    docs = order_ref.get()
    docs = docs.to_dict()
    user_ref = db.collection(u'User').document(docs["userId"])
    docsU = user_ref.get()
    docsU = docsU.to_dict()
    seller_ref = db.collection(u'merchant').document(docs["merchantId"])
    docsM = seller_ref.get()
    docsM = docsM.to_dict()
    sendData = {
        'order_id':data["id"],
        'customer_name:':docsU["userName"],
        'customer_ph':docsU["userPhone"],
        'customer_add':docs["address"],
        'seller_name':docsM["storeName"],
        'seller_gst':"",
        'seller_ph':docsM["landlineNumber"],
        'seller_add':docsM["address"],
        'products':docs["products"],
        'product_final':docs['totalAmount'],
        'today':docs["createdAt"],
        'delivery':docs["deliveryCharge"]
    }
    print(str(sendData))
    pdf = render_to_pdf('pdf/invoice.html', sendData)
    response = HttpResponse(pdf, content_type='application/pdf')
    return response