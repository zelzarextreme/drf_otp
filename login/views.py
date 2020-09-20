from django.shortcuts import render
from .models import UserLogin,UserOTP
import random
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import CreateUserSerializer


class ValidatePhoneSendOTP(APIView):
     def post(self,request,*args,**kwargs):
         phone_number=request.data.get('phone')
         if phone_number:
             phone=str(phone_number)
             user=UserLogin.objects.filter(phone=phone)
             otp=generateotp(phone)
             if otp:
                old=UserOTP.objects.filter(phone=phone)
                if old.exists():
                    old=old.first()
                    print(otp)
                    old.save()
                    return Response(
                     {
                         'status':True,
                         'detail':'OTP has already been sent'
                     } 
                     )
                else:
                    UserOTP.objects.create(phone=phone,otp=otp)
                    print(otp)
                    return Response(
                     {
                         'status':True,
                         'detail':'OTP sent successfully'
                     } 
                     )

             else:
                 return Response({
                 'status': False,
                 'detail':'otp not sent'
                    })    

                  

         else:
             return Response({
                 'status': False,
                 'detail':'phone number absent'
             })    



def generateotp(phone):
    if phone:
        otp=random.randint(999,9999)
        return otp
    else:
        return False
        

class ValidateOTP(APIView):
    def post(self,request,*args,**kwargs):
        phone=request.data.get('phone')
        otp_sent=request.data.get('otp')

        if phone and otp_sent:
            old=UserOTP.objects.filter(phone=phone)
            if old.exists():
                old=old.first()
                otp=old.otp
                if str(otp_sent)==str(otp):
                    old.is_verified=True
                    old.save()
                    return Response(
                        {
                            'status':True,
                            'details':'OTP validated. '
                        }
                    )
                else:
                    return Response(
                        {
                            'status':False,
                            'details':'OTP is incorrect'
                        }
                    )
            else:
             return Response(
                    {
                        'status':False,
                        'details':'Register phone to get OTP'
                    }
                )
        else:
            return Response(
                    {
                        'status':False,
                        'details':'Provide both OTP and phone number for matching.'
                    }
                )


class Register(APIView):
    def post(self,request,*args,**kwargs):
        phone=request.data.get('phone')
        user=request.data.get('user')
        if phone and user:
            old=UserOTP.objects.filter(phone=phone)
            if old.exists():
                old=old.first()
                is_verified=old.is_verified
                if is_verified:
                    temp={
                        'phone':phone,
                        'user':user
                    }
                    serializer=CreateUserSerializer(data=temp)
                    serializer.is_valid(raise_exception=True)
                    user=serializer.save()
                    old.delete()
                    return Response(
                    {
                        'status':True,
                        'details':'account created succesfully'
                    }
                ) 
                else:
                    return Response(
                    {
                        'status':False,
                        'details':'OTP has not been verified'
                    }
                )


            else:
                return Response(
                    {
                        'status':False,
                        'details':'Register phone to get OTP'
                    }
                )


        else:
             return Response(
                    {
                        'status':False,
                        'details':'Provide both password and phone number for registration.'
                    }
                )
        

#view when user would be logged in,keep getting en error of nonetype has no attribute is_verified
'''class LoggedIn(APIView):
     def post(self,request,*args,**kwargs):
         phone_number=request.data.get('phone')
         if phone_number:
             phone=str(phone_number)
             user=UserOTP.objects.filter(phone=phone)
             user=user.first()
             if user.is_verified:
                 user=UserLogin.objects.filter(phone=phone)
                 print(user.user)
                 return Response(
                    {
                        'status':True,
                        'details':'Logged in.'
                    }
                )
             else:   
                return Response(
                    {
                        'status':False,
                        'details':'OTP not validated.NOT LOGGED IN'
                    }
                )
         else:
             return Response(
                    {
                        'status':False,
                        'details':'Provide phone number for login.'
                    }
                )

'''
