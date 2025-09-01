from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import firebase_admin
from firebase_admin import db
from datetime import datetime

class LandingAPI(APIView):
    name = "Landing API"
    collection_name = "landing_data"  # Nombre de tu colección en Firebase

    def get(self, request):

      # Referencia a la colección
      ref = db.reference(f'{self.collection_name}')

      # get: Obtiene todos los elementos de la col ección
      data = ref.get()

      # Devuelve un arreglo JSON
      return Response(data, status=status.HTTP_200_OK)

    def post(self, request):

      data = request.data

      # Referencia a la colección
      ref = db.reference(f'{self.collection_name}')

      current_time  = datetime.now()
      custom_format = current_time.strftime("%d/%m/%Y, %I:%M:%S %p").lower().replace('am', 'a. m.').replace('pm', 'p. m.')
      data.update({"timestamp": custom_format })

      # push: Guarda el objeto en la colección
      new_resource = ref.push(data)

      # Devuelve el id del objeto guardado
      return Response({"id": new_resource.key}, status=status.HTTP_201_CREATED)

    def put(self, request, pk=None, format=None):
        if not pk:
            return Response({"detail": "PUT sobre colección no permitido. Use /landing/<pk>/"},
                            status=status.HTTP_405_METHOD_NOT_ALLOWED)
        ref = db.reference(f"{self.collection_name}/{pk}")
        if ref.get() is None:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        payload = request.data.copy()
        payload.update({"updated_at": self._now_str()})
        # set reemplaza completamente el nodo
        ref.set(payload)
        return Response({"id": pk, "data": payload}, status=status.HTTP_200_OK)

    def patch(self, request, pk=None, format=None):
        if not pk:
            return Response({"detail": "PATCH sobre colección no permitido. Use /landing/<pk>/"},
                            status=status.HTTP_405_METHOD_NOT_ALLOWED)
        ref = db.reference(f"{self.collection_name}/{pk}")
        if ref.get() is None:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        payload = request.data.copy()
        payload.update({"updated_at": self._now_str()})
        # update hace merge de campos
        ref.update(payload)
        updated = ref.get()
        return Response({"id": pk, "data": updated}, status=status.HTTP_200_OK)

    def delete(self, request, pk=None, format=None):
        if not pk:
            # Opcional: podrías permitir borrar todo, pero mejor no por seguridad.
            return Response({"detail": "Para eliminar un item debe especificar su id (/landing/<pk>/)."},
                            status=status.HTTP_405_METHOD_NOT_ALLOWED)
        ref = db.reference(f"{self.collection_name}/{pk}")
        if ref.get() is None:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        ref.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
