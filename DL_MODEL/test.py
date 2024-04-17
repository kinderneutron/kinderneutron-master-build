from neo4j import GraphDatabase

# Create a Neo4j driver instance
uri = "neo4j://neo4j-container:7687"  # Update with your Neo4j connection details
username = "neo4j"
password = "password"

driver = GraphDatabase.driver(uri, auth=(username, password))

def fetch_bulb_pins(location):
    with driver.session() as session:
        if location.lower() == "near":
            query = (
                "MATCH (:Near)-[:CONNECTED_TO]->(bulb:Bulb) "
                "RETURN bulb.name AS bulb_name, bulb.pin AS bulb_pin"
            )
        elif location.lower() == "far":
            query = (
                "MATCH (:Far)-[:CONNECTED_TO]->(bulb:Bulb) "
                "RETURN bulb.name AS bulb_name, bulb.pin AS bulb_pin"
            )
        else:
            return "Invalid location parameter. Use 'near' or 'far'."

        result = session.run(query)
        bulbs = [(record["bulb_name"], record["bulb_pin"]) for record in result]

        ans = []
        for i in bulbs:
            ans.append(i[1])
        return ans

# Usage example
location_parameter = "far"
bulbs_pins = fetch_bulb_pins(location_parameter)

print(type(bulbs_pins))
