// Create Camera nodes
CREATE (camera1:Camera {name: "camera1"})

// Create Distance nodes
CREATE (near:Distance {name: "near"})
CREATE (far:Distance {name: "far"})

// Create Bulb nodes with pin properties
CREATE (bulb1:Bulb {name: "bulb1", pin: 3})
CREATE (bulb2:Bulb {name: "bulb2", pin: 4})
CREATE (bulb3:Bulb {name: "bulb3", pin: 5})

// Create relationships
// camera1 relationships
CREATE (camera1)-[:HAS_A_AREA]->(near)
CREATE (camera1)-[:HAS_A_AREA]->(far)

// near relationships
CREATE (near)-[:CONNECTED_TO]->(bulb1)
CREATE (near)-[:CONNECTED_TO]->(bulb2)

// far relationships
CREATE (far)-[:CONNECTED_TO]->(bulb3)
