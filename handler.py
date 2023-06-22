try:
    import unzip_requirements
except ImportError:
    pass

import time
import pandas as pd
from datetime import datetime
import io
from functions import (
    set_bacia,
    busca_s3_arquivo,
    salvar_s3_arquivo,
)


def bacias(event, context):
    nome = event["Records"][0]["s3"]["object"]["key"].split("/")[0]
    time.sleep(10)
    modelo_bacia = set_bacia(nome)
    arquivo_s3_sintegre = busca_s3_arquivo(modelo_bacia["nome_arquivo"])
    dt_sintegre = pd.read_table(
        io.BytesIO(arquivo_s3_sintegre),
        sep="\s+",
        header=None,
        names=modelo_bacia["datanames_sintegre"],
    )
    arquivo_s3_relacao_bacias = busca_s3_arquivo("relacao_macro.xlsx")
    dt_relacao = pd.read_excel(
        io.BytesIO(arquivo_s3_relacao_bacias),
        header=None,
        names=["Codigo ANA", "Nome", "Macro-Bacia"],
    )
    dt_merge = pd.merge(dt_sintegre, dt_relacao, how="inner", on="Codigo ANA")
    lista_macro = dt_merge["Macro-Bacia"].drop_duplicates()
    bacias = []
    for item in lista_macro:
        t = dt_merge[dt_merge["Macro-Bacia"] == item]
        media = []
        media.append(item)
        for i in range(modelo_bacia["dias"]):
            result = t["d{}".format(i + 1)].mean()
            media.append(result)
        bacias.append(media)
    df = pd.DataFrame(bacias, columns=modelo_bacia["datanames_column"])
    df = df.assign(modelo=modelo_bacia["modelo"])
    df = df.assign(datetoday=(datetime.today()).strftime("%Y/%m/%d"))
    df = df[modelo_bacia["datanames_final"]]
    csv_buffer = io.StringIO()
    df.to_csv(csv_buffer, header=False, index=False)
    salvar_s3_arquivo(csv_buffer, nome)
