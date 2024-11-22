from skspatial.objects import Plane, Vector

plane = Plane((1,0,1), (0,1,0))
vector = Vector((10, 10, 10))

projected_vector = plane.project_vector(vector)

print("Projected vector:", projected_vector)
