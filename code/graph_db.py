from py2neo import Graph, Node, Relationship
from base64 import b64encode

graph = Graph("neo4j://neo4j2:7687", auth=("neo4j", "adminpass"))
def Vrat_pocet_profilu():
    result = graph.run(f"""MATCH (n) RETURN count(n) AS profile_count""").data()
    id = result[0]['profile_count'] if result else 0
    return id
def Vytvor_profil_Node(node_id,jmeno,vek,orientace,konicky,popis):
    profil = Node("Osoba", node_id=node_id, name=jmeno, age=vek, orintace=orientace, hobbies=konicky, popis_profilu=popis)
    graph.create(profil)
def Add_profile_neo(node_id,jmeno,prijmeni,pohlavi,email,heslo,vek,orientace,konicky,popis):
    query = f"""
    MERGE (o:Osoba {{node_id: $node_id}}) 
    SET o.name = $name,
        o.surname = $surname,
        o.pohlavi = $pohlavi,
        o.email = $email,
        o.heslo = $heslo,
        o.age = $age,
        o.orientace = $orientace,
        o.hobbies = $hobbies,
        o.popis_profilu = $popis_profilu
    RETURN o
    """    
    result = graph.run(query, node_id=node_id, name=jmeno,surname=prijmeni,pohlavi=pohlavi,email=email,heslo=heslo,age=vek,orientace=orientace,hobbies=konicky,popis_profilu=popis)
    return result
def Kontrola_existence_profilu(email):
    query = f"""
    MATCH (o:Osoba {{email: $email}})
    RETURN COUNT(o) > 0 AS profileExists
    """    
    result = graph.run(query, email=email).evaluate()
    return result
def Vrat_uzivatele_podle_id(email):
    query = f"""
    MATCH (o:Osoba {{email: $email}})
    RETURN o
    """
    result = graph.run(query, email=email).data()
    if not result:
        return None
    if result: return result[0]['o'] 
    return None
def Vrat_prihlasovaci_udaje(email):
    query = """
    MATCH (o:Osoba {email: $email})
    RETURN o
    """
    result = graph.run(query, email=email).data()
    if result: return result[0]['o']
    return None        
def Vymaz_vsechny_prfily():
    query = f"""
    MATCH (n)
    DETACH DELETE n
    """    
    result = graph.run(query)
    return result
def Vymaz_profil(id_uziv):
    query = f"""
    MATCH (n:Person {{node_id: $id_uziv}})
    DELETE n
    """    
    result = graph.run(query)
    return result
def Vrat_vsechny_profily(pohlavi=None):
    query = f"""MATCH (n) RETURN n"""    
    result = graph.run(query)
    return [record['n'] for record in result]

def Like_profile(node_id_1,node_id_2):
    node1 = graph.evaluate("MATCH (o:Osoba) WHERE o.node_id = $node_id RETURN o", node_id=node_id_1)
    node2 = graph.evaluate("MATCH (o:Osoba) WHERE o.node_id = $node_id RETURN o", node_id=node_id_2)
    print(node1,node2)
    if node1 and node2: 
        result = graph.evaluate("MATCH (a)-[r:LIKES]->(b) WHERE a.node_id = $id1 AND b.node_id = $id2 RETURN r",id1=node_id_1, id2=node_id_2)
        if result: return "Like"
        else:
            relationship = Relationship(node1, "LIKES", node2); graph.create(relationship); return "Relation"
    else:
        return None
def delete_like(node_id_1,node_id_2):
    query = """
    MATCH (a)-[r:LIKES]->(b)
    WHERE a.node_id = $node_id_1 AND b.node_id = $node_id_2
    DELETE r
    """
    result = graph.run(query, node_id_1=node_id_1, node_id_2=node_id_2)
    if result: return True
    return None

def get_user_likes(node_id): #zjistím komu uživatel s daným id již dal like
    query = f"""
        MATCH (n)-[:LIKES]->(liker)
        WHERE n.node_id = $node_id
        RETURN liker.node_id AS liker_id
        """
    results = graph.run(query, node_id=node_id).data()
    return [int(record['liker_id']) for record in results]
    

##jednotliva pridavani
#fotky
def Pridej_fotku(node_id,image_path): #pridam fotku a zasifruji primo ze systemu, pokud mám adresar
    with open(image_path, "rb") as image_file: image = b64encode(image_file.read()).decode('utf-8')
    query = f"""
    MATCH (o:Osoba {{node_id: $node_id}})
    SET o.picture = $encoded_picture
    RETURN o
    """
    result = graph.run(query, node_id=node_id, encoded_picture=image).data()
    return result
def Pridej_fotku_data(node_id,image_file): #zde predavam přímo data nahrané fotky, která potom zakoduji a ulozim do db
    image_file = b64encode(image_file)
    query = f"""
    MATCH (n {{node_id: $node_id}})
    SET n.picture = $encoded_picture
    RETURN n
    """
    result = graph.run(query, node_id=node_id, encoded_picture=image_file).data()
    return result
def Vrat_fotku(node_id):
    query = f"""
    MATCH (o:Osoba {{node_id: $node_id}})
    RETURN o.picture as fotka
    """
    result = graph.run(query, node_id=node_id).data()
    return result[0]['fotka'] # vrátím fotku
def Pridej_cislo(node_id,tel_cislo):
    query = f"""
    MATCH (o:Osoba {{node_id: $node_id}})
    SET o.telefoni_cislo = $telefoni_cislo
    RETURN o
    """
    result = graph.run(query, node_id=node_id, telefoni_cislo=tel_cislo).data()
    return result
def Zmen_konicky(node_id, konicky):
    query = f"""
    MATCH (o:Osoba {{node_id: $node_id}})
    SET o.hobbies = $hobbies
    RETURN o
    """
    result = graph.run(query, node_id=node_id, hobbies=konicky).data()
    return result

def Pridej_popis(node_id, popis):
    query = f"""
    MATCH (o:Osoba {{node_id: $node_id}})
    SET o.popis_profilu = $popis_
    RETURN o
    """
    result = graph.run(query, node_id=node_id, popis_=popis).data()
    return result
def Vrat_konicky(node_id):
    query = f"""
    MATCH (o:Osoba {{node_id: $node_id}})
    RETURN o.hobbies as hobbies
    """
    result = graph.run(query, node_id=node_id).data()
    return result[0]['hobbies'] 

def Vrat_popis(node_id):
    query = f"""
    MATCH (o:Osoba {{node_id: $node_id}})
    RETURN o.popis_profilu as popis
    """
    result = graph.run(query, node_id=node_id).data()
    return result[0]['popis'] # vrátím fotku