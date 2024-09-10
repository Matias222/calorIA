from datetime import datetime

def convertir(cadena):

    date_obj = datetime.strptime(cadena, "%d/%m/%Y")

    new_date_str = date_obj.strftime("%m-%d-%Y")

    return new_date_str

