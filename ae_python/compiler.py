from ae_python.comp import Comp
from ae_python.layer.soild_layer import SolidLayer
from ae_python.layer.null_layer import NullLayer

class Compiler:
    def __init__(self, comps: Comp):
        self.comp_list = comps

        self.js_script = ""

    """
    Compile the layers to javascript for after effects. The layer needs the comp variable(hashed value) to add a layer 
    to the comp. Also a layer variable will be created(hashed value).
    """
    def __create_layer__(self, layer, comp: Comp):
        # If the pixel aspect isn't set the layer the value is the same as in the comp
        if layer.pixel_aspect == None:
            layer.pixel_aspect = comp.pixel_aspect

        # JS script for solid layer. To identify the type of the layer the class will be identified.
        if type(layer) == SolidLayer:
            self.js_script += f"var {layer.js_variable_name} = {comp.js_variable_name}.layers.addSolid([" \
                              f"{layer.color.red},{layer.color.green},{layer.color.blue}], {layer.name}, 100,100,1);"

        # JS script for null layer.
        elif type(layer) == NullLayer:
            self.js_script += f"var {layer.js_variable_name} = {comp.js_variable_name}.layers.addNull();"

        else:
            raise ValueError("Class type is not in compiler list.")

        # Adds properties to layer.
        # Sets the position
        self.js_script += f"{layer.js_variable_name}.position.setValue([{layer.position[0]}, {layer.position[1]}, " \
                          f"{layer.position[2]}]);"

        # Sets the name
        self.js_script += f"{layer.js_variable_name}.name = '{layer.name}';"

        # Sets the comment
        if layer.comment != None:
            self.js_script += f"{layer.js_variable_name}.comment = '{layer.comment}';"

        # Sets the label
        if layer.label != None:
            self.js_script += f"{layer.js_variable_name}.label = {layer.label};"

        # Sets if looked
        if layer.locked:
            self.js_script += f"{layer.js_variable_name}.locked = true;"

        # Sets if shy
        if layer.shy:
            self.js_script += f"{layer.js_variable_name}.shy = true;"

        # Sets if solo
        if layer.solo:
            self.js_script += f"{layer.js_variable_name}.solo = true;"

        # Sets the start time
        self.js_script += f"{layer.js_variable_name}.startTime = {layer.start_time};"

        # Sets the stretch
        if layer.stretch != None:
            self.js_script += f"{layer.js_variable_name}.stretch = {layer.stretch};"

        # Sets the in point
        if layer.in_point != None:
            self.js_script += f"{layer.js_variable_name}.inPoint = {layer.in_point}"

        # Sets the out point
        if layer.out_point != None:
            self.js_script += f"{layer.js_variable_name}.outPoint = {layer.out_point}"

    """
     Compile the comps to javascript for after effects. The variable name is hashed to prevent doubling 
    """
    def __create_comp__(self, comp: Comp):
        self.js_script += f"var {comp.js_variable_name} = app.project.items.addComp('{comp.name}', {comp.width}, {comp.height}, {comp.pixel_aspect}, {comp.duration}, {comp.framerate});"

    def compile(self):
        for comp in self.comp_list:
            self.__create_comp__(comp)

            for layer in comp.layers:
                self.__create_layer__(layer, comp)

        return self.js_script