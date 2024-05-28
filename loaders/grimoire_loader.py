from langchain_community.document_loaders import JSONLoader
from langchain.docstore.document import Document
import json
import os
from pprint import pprint


def _get_class_docs(class_json_path: str):
    all_docs = []

    with open(class_json_path, 'r') as f:
        data = json.load(f)

    main_stats = f"""Classe {data['name']}
HP: {data['hp']} + {data['addHP']} por nível.
PM: {data['pm']}
Perícias:
- {'\n- '.join(data['skills'])}
Você escolhe mais {data['extraSkillsQty']} perícias da seguinte lista:
- {'\n- '.join(data['extraSkills'])}
"""

    all_docs.append(Document(main_stats, metadata={"source": class_json_path}))

    class_name = data['name']
    schema = f'.abilities[] | "Habilidade de {class_name}: \\(.name) - \\(.description)"'
    loader = JSONLoader(file_path=class_json_path, jq_schema=schema)
    all_docs += loader.load()

    return all_docs


def _get_race_docs(race_json_path: str):
    all_docs = []

    with open(race_json_path, 'r') as f:
        data = json.load(f)

    main_stats = f"""Raça: {data['name']}
Deslocamento: {data['displacement']}m
Tamanho: {data['size']}
Atributos:
"""
    for attribute in data["attributes"]:
        main_stats += f"  - {str.upper(attribute['attr'])}: {attribute['mod']}\n"

    all_docs.append(Document(main_stats, metadata={"source": race_json_path}))

    race_name = data['name']
    schema = f'.abilities[] | "Habilidade de {race_name}: \\(.name) - \\(.description)"'
    loader = JSONLoader(file_path=race_json_path, jq_schema=schema)
    all_docs += loader.load()

    return all_docs


def _get_spell_docs(spell_json_path: str):
    all_docs = []

    with open(spell_json_path, 'r') as f:
        data = json.load(f)

    for spell in data["spells"]:
        main_stats = f'''
Nome: {spell["name"]} - Magia de {spell["circle"]}º Círculo
Tipo de magia: {spell["type"]}
Alcance: {spell["range"]}
Alvo: {spell["target"]}
Duração: {spell["duration"]}
Execução: {spell["execution"]}
Resistência: {spell["resistance"]}
Área: {spell["area"]}
Efeito: {spell["effect"]}
Descrição: {spell["description"]}

Melhorias:
'''
        for implement in spell["implements"]:
            main_stats += f'''   - Custo: {implement["cost"]}
            Descrição: {implement["description"]}
        '''
        all_docs.append(Document(main_stats, metadata={"source": spell_json_path}))

    return all_docs


def _get_book_docs(book_json_path):

    with open(book_json_path, "r") as f:
        data = json.load(f)

    def iterate_and_generate_doc(folder_items, original_path):
        all_docs = []
        for i in folder_items:
            if i["type"] == "item":
                text = f'{i["name"]} - {i["description"]}'
                doc = Document(text, metadata={"source": original_path})
                all_docs.append(doc)
            else:
                all_docs += iterate_and_generate_doc(i["items"], original_path)
        return all_docs

    return iterate_and_generate_doc(data["items"], book_json_path)


def _get_docs_from_schema(json_path: str, schema: str):
    all_docs = []

    loader = JSONLoader(file_path=json_path, jq_schema=schema)
    all_docs += loader.load()

    return all_docs


def create_grimoire_docs():

    armor_schema = '.items[] | "Equipamento: \\(.name)\n\nPreço: \\(.price)\n\nBônus de Defesa: \\(.defenseBonus)\n\nPenalidade de Armadura: \\(.armorPenalty)\n\nEspaços ocupados: \\(.spaces)\n\nProficiência necessária: \\(.proficiency)"'
    weapon_schema = '.items[] | "Equipamento: \\(.name)\n\nPreço: \\(.price)\n\nDano: \\(.damage)\n\nCrítico: \\(.critical)\n\nAlcance: \\(.range)\n\nTipo de Dano: \\(.damageType)\n\nEspaços ocupados: \\(.spaces)\n\nProficiência necessária: \\(.proficiency)\n\nTipo: \\(.purpose)\n\nEmpunhadura: \\(.grip)"'
    items_schema = '.items[] | "Item: \\(.name)\n\nPreço: \\(.price)\n\nEspaços ocupados: \\(.spaces)\n\nCategoria: \\(.category)"'

    equipments = [
        ("./data/t20_grimoire/equipments/Armaduras & Escudos.json", armor_schema),
        ("./data/t20_grimoire/equipments/Armas.json", weapon_schema),
        ("./data/t20_grimoire/equipments/Itens Gerais.json", items_schema),
    ]

    origin_powers_schema = '.powers[] | "Origem: \\(.source)\n\nPoder da Origem: \\(.name)\n\nDescrição: \\(.description)"'
    conceded_powers_schema = '.powers[] | "Poder da Concedido: \\(.name)\n\nDescrição: \\(.description)"'
    tormenta_powers_schema = '.powers[] | "Poder da Tormenta: \\(.name)\n\nDescrição: \\(.description)"'
    combat_powers_schema = '.powers[] | "Poder de Combate: \\(.name)\n\nDescrição: \\(.description)"'
    destiny_powers_schema = '.powers[] | "Poder de Destino: \\(.name)\n\nDescrição: \\(.description)"'
    magic_powers_schema = '.powers[] | "Poder de Magia: \\(.name)\n\nDescrição: \\(.description)"'

    powers = [
        ("./data/t20_grimoire/powers/Origens.json", origin_powers_schema),
        ("./data/t20_grimoire/powers/Poderes Concedidos.json", conceded_powers_schema),
        ("./data/t20_grimoire/powers/Poderes da Tormenta.json", tormenta_powers_schema),
        ("./data/t20_grimoire/powers/Poderes de Combate.json", combat_powers_schema),
        ("./data/t20_grimoire/powers/Poderes de Destino.json", destiny_powers_schema),
        ("./data/t20_grimoire/powers/Poderes de Magia.json", magic_powers_schema),
    ]

    classes = []
    classes_path = "./data/t20_grimoire/classes"
    for file in os.listdir(classes_path):
        if file.endswith(".json"):
            classes.append(os.path.join(classes_path, file))

    races = []
    races_path = "./data/t20_grimoire/races"
    for file in os.listdir(races_path):
        if file.endswith(".json"):
            races.append(os.path.join(races_path, file))

    spells = []
    spells_path = "./data/t20_grimoire/spells"
    for file in os.listdir(spells_path):
        if file.endswith(".json"):
            spells.append(os.path.join(spells_path, file))

    book = []
    book_path = "./data/t20_grimoire/book"
    for file in os.listdir(book_path):
        if file.endswith(".json") and file != "Tabelas.json":
            book.append(os.path.join(book_path, file))

    grimoire_docs = []

    for json_path in book:
        grimoire_docs += _get_book_docs(json_path)

    for json_path in classes:
        grimoire_docs += _get_class_docs(json_path)

    for json_path, schema in equipments:
        grimoire_docs += _get_docs_from_schema(json_path, schema)

    for json_path, schema in powers:
        grimoire_docs += _get_docs_from_schema(json_path, schema)

    for json_path in races:
        grimoire_docs += _get_race_docs(json_path)

    for json_path in spells:
        grimoire_docs += _get_spell_docs(json_path)

    return grimoire_docs
