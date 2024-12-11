from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from translator.models import Translation
from translator.serializers import TranslationSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
import google.generativeai as genai
import os
from dotenv import load_dotenv

GEMINI = os.getenv('GEMINI_API_KEY')

env_path = os.path.join(os.path.dirname(__file__), '.env')

load_dotenv(env_path)

# Create your views here.
class AllTranslation(APIView):
    def get(self, request):

        result = Translation.objects.all()
        serialized_data = TranslationSerializer(result, many=True)

        return Response(data=serialized_data.data, status=status.HTTP_200_OK)

class FrenchSpanishTranslationViewSet(APIView):


    def translate(self, source_text, source_language, target_language):
        prompt = f"Traduis moi '{source_text}' dans cette langue : {target_language}."
        genai.configure(api_key=GEMINI)

        model = genai.GenerativeModel("gemini-1.5-flash")

        response = model.generate_content(prompt)

        target_text = response.text.strip()
        
        print(f"Translated text: {target_text}")
        return target_text


    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('source_text', openapi.IN_QUERY, type=openapi.TYPE_STRING, description="source_text"),
            openapi.Parameter('source_language', openapi.IN_QUERY, type=openapi.TYPE_STRING, description="source_language"),
            openapi.Parameter('target_language', openapi.IN_QUERY, type=openapi.TYPE_STRING, description="target_language"),
        ]
    )
    
    def get(self, request):
        source_language = request.query_params.get('source_language', 'pas de langue source') 
        target_language = request.query_params.get('target_language', 'pas de langue target')
        source_text = request.query_params.get('source_text', 'pas de texte')

        data = Translation.objects.filter(source_language=source_language, target_language=target_language, source_text=source_text)
        serialized_data = TranslationSerializer(data, many=True)

        return Response(data=serialized_data.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=TranslationSerializer)
    def post(self, request):

        api_key = "AIzaSyCVmH2NwYEeTxCFbuN2I2B7d3twFvWYOyY"

        source_language = request.GET.get('source_language')
        source_text = request.GET.get('source_text')
        target_language = request.GET.get('target_language')

        if not source_language or not source_text or not target_language:
            return Response({'error': 'Missing required parameters'}, status=status.HTTP_400_BAD_REQUEST)

        target_text = self.translate(source_text, source_language, target_language)

        translation = Translation.objects.create(source_language=source_language, source_text=source_text, target_language=target_language, target_text=target_text)

        return Response({'Translation': TranslationSerializer(translation).data}, status=status.HTTP_201_CREATED)

    
    def put(self, request, pk):
        return Response(data={}, status=None)
    
    def delete(self, request, pk):
        return Response(data={}, status=None)
    
class FrenchEnglishTranslationViewSet(APIView):

    def get(self, request):
        return Response(data={}, status=None)
    
    def post(self, request):
        return Response(data={}, status=None)
    
    def put(self, request, pk):
        return Response(data={}, status=None)
    
    def delete(self, request, pk):
        return Response(data={}, status=None)

def index(request):
    return render(request, 'index.html', context={})