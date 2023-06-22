import os
import boto3
from dict import Eta40, Gefs50, ECMWF

session = boto3.Session(
    aws_access_key_id=os.environ.get("ACCESS_KEY"),
    aws_secret_access_key=os.environ.get("ACCESS_SECRET"),
    region_name=os.environ.get("REGION"),
)
s3 = session.resource("s3")


def set_bacia(nome):
    nome_arquivo = ""
    datanames_sintegre = []
    datanames_final = []
    datanames_column = []
    dias = 0
    modelo = 0

    if nome == "Eta40":
        nome_arquivo = Eta40["nome_arquivo"]
        datanames_sintegre = Eta40["datanames_sintegre"]
        datanames_final = Eta40["datanames_final"]
        datanames_column = Eta40["datanames_column"]
        dias = Eta40["dias"]
        modelo = Eta40["numero_modelo"]

    if nome == "Gefs50":
        nome_arquivo = Gefs50["nome_arquivo"]
        datanames_sintegre = Gefs50["datanames_sintegre"]
        datanames_final = Gefs50["datanames_final"]
        datanames_column = Gefs50["datanames_column"]
        dias = Gefs50["dias"]
        modelo = Gefs50["numero_modelo"]

    if nome == "ECMWF":
        nome_arquivo = ECMWF["nome_arquivo"]
        datanames_sintegre = ECMWF["datanames_sintegre"]
        datanames_final = ECMWF["datanames_final"]
        datanames_column = ECMWF["datanames_column"]
        dias = ECMWF["dias"]
        modelo = ECMWF["numero_modelo"]

    result = {
        "nome_arquivo": nome_arquivo,
        "datanames_sintegre": datanames_sintegre,
        "datanames_final": datanames_final,
        "datanames_column": datanames_column,
        "dias": dias,
        "modelo": modelo,
    }

    return result


def busca_s3_arquivo(nome_arquivo):
    my_bucket = s3.Bucket("bucket-docs-nodejs")
    for my_bucket_object in my_bucket.objects.all():
        if nome_arquivo in my_bucket_object.key:
            return my_bucket_object.get()["Body"].read()


def salvar_s3_arquivo(arquivo, nome):
    s3.Object("bucket-docs-nodejs", "{}/{}.csv".format(nome, nome)).put(
        Body=arquivo.getvalue()
    )
