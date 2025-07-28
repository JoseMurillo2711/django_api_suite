from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

import uuid

# Simulación de base de datos local en memoria
data_list = []

# Añadiendo algunos datos de ejemplo para probar el GET
data_list.append({'id': str(uuid.uuid4()), 'name': 'User01', 'email': 'user01@example.com', 'is_active': True})
data_list.append({'id': str(uuid.uuid4()), 'name': 'User02', 'email': 'user02@example.com', 'is_active': True})
data_list.append({'id': str(uuid.uuid4()), 'name': 'User03', 'email': 'user03@example.com', 'is_active': False}) # Ejemplo de item inactivo

class DemoRestApi(APIView):
    name = "Demo REST API"

    def get(self, request):

      # Filtra la lista para incluir solo los elementos donde 'is_active' es True
      active_items = [item for item in data_list if item.get('is_active', False)]
      return Response(active_items, status=status.HTTP_200_OK)
    
    def post(self, request):
      data = request.data

      # Validación mínima
      if 'name' not in data or 'email' not in data:
         return Response({'error': 'Faltan campos requeridos.'}, status=status.HTTP_400_BAD_REQUEST)

      data['id'] = str(uuid.uuid4())
      data['is_active'] = True
      data_list.append(data)

      return Response({'message': 'Dato guardado exitosamente.', 'data': data}, status=status.HTTP_201_CREATED)

    def put(self, request):
        data = request.data
        item_id = data.get('id')
        if not item_id:
            return Response({'error': 'Se requiere el campo \"id\".'}, status=status.HTTP_400_BAD_REQUEST)

        for idx, item in enumerate(data_list):
            if item['id'] == item_id:
                if 'name' not in data or 'email' not in data:
                    return Response({'error': 'Faltan campos requeridos: name y email.'}, status=status.HTTP_400_BAD_REQUEST)
                updated = {
                    'id': item_id,
                    'name': data['name'],
                    'email': data['email'],
                    'is_active': data.get('is_active', item.get('is_active', True))
                }
                data_list[idx] = updated
                return Response({'message': 'Item reemplazado exitosamente.', 'data': updated}, status=status.HTTP_200_OK)

        return Response({'error': 'Item no encontrado.'}, status=status.HTTP_404_NOT_FOUND)

    def patch(self, request):
        data = request.data
        item_id = data.get('id')
        if not item_id:
            return Response({'error': 'Se requiere el campo \"id\".'}, status=status.HTTP_400_BAD_REQUEST)

        for item in data_list:
            if item['id'] == item_id:
                for key in ['name', 'email', 'is_active']:
                    if key in data:
                        item[key] = data[key]
                return Response({'message': 'Item actualizado exitosamente.', 'data': item}, status=status.HTTP_200_OK)

        return Response({'error': 'Item no encontrado.'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request):
        data = request.data
        item_id = data.get('id')
        if not item_id:
            return Response({'error': 'Se requiere el campo \"id\".'}, status=status.HTTP_400_BAD_REQUEST)

        for item in data_list:
            if item['id'] == item_id:
                item['is_active'] = False
                return Response({'message': 'Item eliminado lógicamente (is_active=False).'}, status=status.HTTP_200_OK)

        return Response({'error': 'Item no encontrado.'}, status=status.HTTP_404_NOT_FOUND)
