from ninja import NinjaAPI, Schema, ModelSchema, UploadedFile
from .models import Livro
import json
from django.shortcuts import get_object_or_404

api = NinjaAPI()
from django.forms.models import model_to_dict


@api.get("livro/")
def listar(request):
    livro = Livro.objects.all()
    response = [
        {"id": i.id, "titulo": i.titulo, "descricao": i.descricao, "autor": i.autor}
        for i in livro
    ]
    return response


@api.get("livro/{id}")
def listar_livro(request, id: int):
    livro = get_object_or_404(Livro, id=id)
    return model_to_dict(livro)


@api.get("livro_consulta/")
def listar_consulta(request, id: int = 1):
    livro = get_object_or_404(Livro, id=id)
    return model_to_dict(livro)


class LivroSchema(ModelSchema):
    class Config:
        model = Livro
        model_fields = ["titulo", "descricao", "autor"]


@api.post("livro", response=LivroSchema)
def livro_criar(request, livro: LivroSchema):
    l1 = livro.dict()
    livro = Livro(titulo=l1["titulo"], descricao=l1["descricao"], autor=l1["autor"])
    livro.save()
    return livro
