import bpy
import copy
import random
def get_objs(collection):                   # Returns all meshes in a collection
    collection = bpy.data.collections[collection]
    for obj in collection.all_objects:
        ob = bpy.data.objects[str(obj.name)]
        if ob.type == 'MESH':
            mesh_name = obj.name
            #shapekey_name = shapekey_name.split()
    return mesh_name 

def clamp(num, min_value, max_value):
   return max(min(num, max_value), min_value)

class Defines():
    shape_defs = dict(              # 29 shapes
        cheekPuff = 'mouthInflate',
        jawOpen = 'Expressions_mouthOpen_max',
        jawForward = 'Expressions_jawOut_max',     # added
        jawLeft = 'jawLeft',     # added
        jawRight = 'jawRight',     # added
        mouthFunnel = 'mouthFunnel',     # added
        mouthPucker = 'mouthPucker', # fixed in vrcft master
        mouthLeft = 'mouthLeft',     # added
        mouthRight = 'mouthRight',     # added
        mouthRollUpper = 'mouthRollUpper',     # fixed in vrcft master
        mouthRollLower = 'mouthRollLower',     # fixed in vrcft master
        mouthShrugUpper = 'mouthShrugUpper',     # added
        mouthShrugLower = 'mouthShrugLower',     # added
        mouthClose = 'mouthClose',             # MUST BE EQUAL TO jawOpen
        mouthSmileLeft = 'mouthSmileL',     # added
        mouthSmileRight = 'mouthSmileR',    # added
        mouthFrownLeft = 'mouthFrownLeft',     # added
        mouthFrownRight = 'mouthFrownRight',     # added
        mouthDimpleLeft = 'mouthDimple_L',   # added
        mouthDimpleRight = 'mouthDimple_R',      # added
        mouthUpperUpLeft = 'mouthUpperUp_L',      # added		
        mouthUpperUpRight = 'mouthUpperUp_R',      # added
        mouthLowerDownLeft = 'mouthLowerDown_L', 	 # added	
        mouthLowerDownRight = 'mouthLowerDown_R',      # added
        mouthPressLeft = 'mouthPress_L',      # added
        mouthPressRight = 'mouthPress_R',      # added
        mouthStretchLeft = 'mouthStretch_L',     # added
        mouthStretchRight = 'mouthStretch_R',    # added
        tongueOut = 'tongueOut' 
    )

    shape_index = ["cheekPuff", "jawOpen", "jawForward", "jawLeft", "jawRight", "mouthFunnel", "mouthPucker", "mouthLeft", "mouthRight", 
    "mouthRollUpper", "mouthRollLower", "mouthShrugUpper", "mouthShrugLower", "mouthClose", "mouthSmileLeft", 
    "mouthSmileRight", "mouthFrownLeft", "mouthFrownRight", "mouthDimpleLeft", "mouthDimpleRight", "mouthUpperUpLeft", 
    "mouthUpperUpRight", "mouthLowerDownLeft", "mouthLowerDownRight", "mouthPressLeft", "mouthPressRight", "mouthStretchLeft", 
    "mouthStretchRight", "tongueOut"]
    
    exclusives = [            # mark these combinations for special treatment when generating values(combined values, etc...)
        ['mouthClose', 'jawOpen'],
        ['mouthShrugUpper', 'mouthShrugLower'],
        ['tongueOut', 'jawOpen']
                    ]

    shape_bl = dict(  
        cheekPuff = ['cheekPuff', 'jawOpen', 'mouthFunnel', 'mouthShrugUpper', 'mouthShrugLower', 'mouthClose', 'mouthUpperUpLeft', 'mouthUpperUpRight', 'mouthLowerDownLeft', 'mouthLowerDownRight', 'tongueOut'],
        jawOpen = ['cheekPuff', 'jawOpen', 'mouthShrugLower', 'mouthShrugUpper'],
        jawForward = ['jawForward'],
        jawLeft = ['jawLeft', 'jawRight'],
        jawRight = ['jawRight', 'jawLeft'],
        mouthFunnel = ['mouthFunnel', 'cheekPuff', 'mouthPucker', 'mouthRollUpper', 'mouthRollLower', 'mouthClose'],
        mouthPucker = ['mouthPucker', 'jawLeft', 'jawRight', 'mouthFunnel', 'mouthRollUpper', 'mouthRollLower', 'mouthClose'],
        mouthLeft = ['mouthLeft', 'mouthRight'],
        mouthRight = ['mouthRight', 'mouthLeft'],
        mouthRollUpper = ['mouthRollUpper', 'jawOpen', 'mouthFunnel', 'mouthPucker', 'mouthClose', 'mouthUpperUpLeft', 'mouthUpperUpRight'],
        mouthRollLower = ['mouthRollLower', 'jawOpen', 'mouthFunnel', 'mouthPucker', 'mouthClose', 'mouthLowerDownLeft', 'mouthLowerDownRight'],
        mouthShrugUpper = ['mouthShrugUpper', 'jawOpen', 'mouthClose', 'tongueOut'],
        mouthShrugLower = ['mouthShrugLower', 'jawOpen', 'mouthClose', 'tongueOut'],
        mouthClose = ['mouthFunnel', 'mouthPucker', 'mouthClose', 'mouthShrugUpper', 'mouthShrugLower'],
        mouthSmileLeft = ['mouthSmileLeft', 'mouthFrownLeft', 'mouthDimpleLeft', 'mouthPressLeft', 'mouthStretchLeft', 'mouthShrugUpper', 'mouthShrugLower'],
        mouthSmileRight = ['mouthSmileRight', 'mouthFrownRight', 'mouthDimpleRight', 'mouthPressRight', 'mouthStretchRight', 'mouthShrugUpper', 'mouthShrugLower'],
        mouthFrownLeft = ['mouthSmileLeft', 'mouthFrownLeft', 'mouthDimpleLeft', 'mouthPressLeft', 'mouthStretchLeft'],
        mouthFrownRight = ['mouthSmileRight', 'mouthFrownRight', 'mouthDimpleRight', 'mouthPressRight', 'mouthStretchRight'],
        mouthDimpleLeft = ['mouthSmileLeft', 'mouthFrownLeft', 'mouthDimpleLeft', 'mouthPressLeft', 'mouthStretchLeft'],
        mouthDimpleRight = ['mouthSmileRight', 'mouthFrownRight', 'mouthDimpleRight', 'mouthPressRight', 'mouthStretchRight'],
        mouthUpperUpLeft = ['mouthUpperUpLeft', 'mouthRollUpper'],
        mouthUpperUpRight = ['mouthUpperUpRight', 'mouthRollUpper'],	
        mouthLowerDownLeft = ['mouthLowerDownLeft', 'mouthRollLower'],
        mouthLowerDownRight = ['mouthLowerDownRight', 'mouthRollLower'],		
        mouthPressLeft = ['mouthSmileLeft', 'mouthFrownLeft', 'mouthDimpleLeft', 'mouthPressLeft', 'mouthStretchLeft'],
        mouthPressRight = ['mouthSmileRight', 'mouthFrownRight', 'mouthDimpleRight', 'mouthPressRight', 'mouthStretchRight'],
        mouthStretchLeft = ['mouthSmileLeft', 'mouthFrownLeft', 'mouthDimpleLeft', 'mouthPressLeft', 'mouthStretchLeft'],
        mouthStretchRight = ['mouthSmileRight', 'mouthFrownRight', 'mouthDimpleRight', 'mouthPressRight', 'mouthStretchRight'],
        tongueOut = ['tongueOut', 'mouthClose']
        )

class ShapeSetter():
    def __init__(self):
        self.blacklist = []           
        self.randomized_shapes = []
        self.possible_shapes = []
        self.selected_shapes = []
        self.selected_shapes_index = []
        self.count = 0

    def reset(self, DefsClass):     
        defs = DefsClass
        self.blacklist = []                 
        self.randomized_shapes = []
        self.selected_shapes = []
        self.selected_shapes_index = []
        self.possible_shapes = copy.copy(defs.shape_index)
        
    def convert_to_defined(self, defs):
        defines_list = []
        for i in range(len(self.selected_shapes_index)):
            defines_list.append(defs.shape_defs[self.selected_shapes_index[i]])
        return(defines_list)

    def get_avalible_shapes(self, defs, shape):         # Adds the shape's blacklist to the list and returns the remaining potential shapes
        self.blacklist.append(defs.shape_bl[shape])
        for i in range(len(self.possible_shapes)):   
            for j in range(len(self.blacklist)):
                for k in range(len(self.blacklist[j])):     
                    if self.blacklist[j][k] in self.possible_shapes:
                        self.possible_shapes.pop(self.possible_shapes.index(self.blacklist[j][k]))
        return(self.possible_shapes)
    
    def process_exclusives(self, defs):         
        if defs.exclusives[0][0] in self.selected_shapes_index and not defs.exclusives[0][1] in self.selected_shapes_index:  # mouthClose = jawOpen
            self.selected_shapes_index.append(defs.exclusives[0][1])        # Add jawOpen value if missing 
            self.selected_shapes.append(0.0)
        if all(item in self.selected_shapes_index for item in defs.exclusives[0]):       
            self.selected_shapes[self.selected_shapes_index.index(defs.exclusives[0][1])] = self.selected_shapes[self.selected_shapes_index.index(defs.exclusives[0][0])]   # set jawOpen = mouthClose

        if defs.exclusives[1][0] in self.selected_shapes_index and not defs.exclusives[1][1] in self.selected_shapes_index:     # mouthShrugLower = mouthShrugUpper
            self.selected_shapes_index.append(defs.exclusives[1][1])        # Add jawOpen value if missing 
            self.selected_shapes.append(self.selected_shapes[self.selected_shapes_index.index(defs.exclusives[1][0])])
        if defs.exclusives[1][1] in self.selected_shapes_index and not defs.exclusives[1][0] in self.selected_shapes_index:
            self.selected_shapes_index.append(defs.exclusives[1][0])        # Add jawOpen value if missing 
            self.selected_shapes.append(self.selected_shapes[self.selected_shapes_index.index(defs.exclusives[1][1])])
        if defs.exclusives[1][1] in self.selected_shapes_index and defs.exclusives[1][0] in self.selected_shapes_index:
            self.selected_shapes[self.selected_shapes_index.index(defs.exclusives[1][1])] = self.selected_shapes[self.selected_shapes_index.index(defs.exclusives[1][0])]

        if defs.exclusives[2][0] in self.selected_shapes_index and not defs.exclusives[2][1] in self.selected_shapes_index: # tongueOut requires jawOpen >= 0.35
            self.selected_shapes_index.append(defs.exclusives[2][1])        # Add jawOpen value if missing 
            self.selected_shapes.append(0.0)
        if defs.exclusives[2][0] in self.selected_shapes_index and self.selected_shapes[self.selected_shapes_index.index(defs.exclusives[2][1])] <= 0.35:
            self.selected_shapes[self.selected_shapes_index.index(defs.exclusives[2][1])] = clamp(random.uniform(0.35, 1.05), 0, 1)

    def generate_example(self, DefsClass, range, classExample):
        defs = DefsClass
        self.reset(defs)
        if type(classExample) == int: classExample = defs.shape_index[classExample]             # Take either String or int
        if type(classExample) == str: classExample = defs.shape_index[defs.shape_index.index(classExample)]
        self.selected_shapes.append(clamp(random.uniform(range[0], range[1]), 0, 1))
        self.selected_shapes_index.append(classExample)
        shape = random.choice(self.get_avalible_shapes(defs, classExample))  
        while len(self.possible_shapes) > 0:
            if 0.75 >= random.uniform(0,1):     # 75% chance for shape to be set
                self.selected_shapes.append(clamp(random.uniform(-0.1, self.selected_shapes[0] - 0.1), 0, 1))
                self.selected_shapes_index.append(shape)
            try: shape = random.choice(self.get_avalible_shapes(defs, shape))  
            except: break
        self.process_exclusives(defs)
        
        return self.selected_shapes, self.convert_to_defined(defs)
    def tick(self):
        self.count += 1

FRAME_START = 0
FRAME_END = 100

defs = Defines()
ss = ShapeSetter()

range_list = [
              [0.5,1.05],
              [0.4, 0.7],
              [-0.2, 0.5]
              ]

ob = bpy.data.objects['MBLab_CA_M']
for shape in ob.data.shape_keys.key_blocks:
    shape.value=0

values, names = ss.generate_example(defs, range_list[1], 'tongueOut')
targetmesh_shapelist = []
ob = bpy.data.objects['MBLab_CA_M']
for i in range(len(values)):
    ob.data.shape_keys.key_blocks[names[i]].value = values[i]


print(targetmesh_shapelist)
        
print(values)
print(names)

# Selector Algo

'''
select class example
roll shape value
add blacklist to interation blacklist
select shape not in blacklist
roll shape value 
add blacklist to iteration blacklist
'''
        # LowRange

    
    
    
    
    
    