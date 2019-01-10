"""this import hairball plugins"""

from hairball.plugins import HairballPlugin
from collections import Counter
import kurt

class Perceptivos(HairballPlugin):
    """ todos los criterios analizados devuelta en un solo diccionario
    """
    def __init__(self):
        super(Perceptivos, self).__init__()
        self.blocks = Counter()
        self.concepts = {} # CT concepts or capabilities

    def finalize(self):
        """Output the overall programming competence"""
        total = 0
        for i in self.concepts.items():
            total += i[1]
        self.concepts['puntaje'] = str(total) 
        average =  float (total) / 7
        print self.concepts
        
    def analyze(self, scratch):
        """Run and return the results from the Mastery plugin."""
        file_blocks = Counter()
        for script in self.iter_scripts(scratch):
            if self.script_start_type(script) != self.NO_HAT:
                for name, _, _ in self.iter_blocks(script.blocks):
                    file_blocks[name] += 1
        self.blocks.update(file_blocks)  # Update the overall count
        self.dialogos(file_blocks, scratch)
        self.eventos(file_blocks, scratch)
        self.puntuacion(file_blocks, scratch)
        self.acciones(file_blocks, scratch)
        self.objetivo(file_blocks, scratch)
        self.mecanica(file_blocks, scratch)
        return {'types': file_blocks}

    def dialogos(self, file_blocks, scratch):
        """cuenta los bloques say"""
        dialogos = 0
        color = 0
        comentario = ""
        for script in self.iter_scripts(scratch):
            for name, _, _ in self.iter_blocks(script.blocks):
                if not name.find("say"):
                   dialogos += 1          
        if dialogos >= 3:
            color = "green"
            comentario = "Excelente"
            dialogos = 3
        elif dialogos == 2:
            color = "light green"
            comentario = "Muy Bien"
        elif dialogos == 1:
            color = "yellow"
            comentario = "Bien"
        else:        
            color = "white"
            comentario = "No Encontrado o No aplica"
        self.concepts['Dialogos'] = dialogos

    def eventos(self,file_blocks, scratch):
        """cuenta los bloques when"""
        eventos = 0
        color = 0
        comentario = ""
        for script in self.iter_scripts(scratch):
            for name, _, _ in self.iter_blocks(script.blocks):
                if not name.find("when"):
                   eventos += 1  
        if eventos >= 3:
            color = "green"
            comentario = "Excelente"
            eventos = 3
        elif eventos == 2:
            color = "light green"
            comentario = "Muy Bien"
        elif eventos == 1:
            color = "yellow"
            comentario = "Bien"
        else:        
            color = "white"
            comentario = "No Encontrado o No aplica"
        self.concepts['Eventos'] = eventos
       
    def puntuacion(self, file_blocks, scratch):
        """cuenta los bloques change by"""
        color = "" 
        comentario = "" 
        puntuacion = 0
        for script in self.iter_scripts(scratch):
            for name, _, _ in self.iter_blocks(script.blocks):
                if not name.find("change"):
                   puntuacion += 1  
        if puntuacion >= 3:
            color = "green"
            comentario = "Excelente"
            puntuacion = 3
        elif puntuacion == 2:
            color = "light green"
            comentario = "Muy Bien"
        elif puntuacion == 1:
            color = "yellow"
            comentario = "Bien"
        else:        
            color = "white"
            comentario = "No Encontrado o No aplica"
        self.concepts['Puntuacion'] = puntuacion
        
    def acciones(self, file_blocks, scratch):
        """cuenta los bloques move"""
        color = ""
        comentario = "" 
        acciones = 0
        for script in self.iter_scripts(scratch):
            for name, _, _ in self.iter_blocks(script.blocks):
                if not name.find("move"):
                   acciones += 1  
        if acciones >= 3:
            color = "green"
            comentario = "Excelente"
            acciones = 3
        elif acciones == 2:
            color = "light green"
            comentario = "Muy Bien"
        elif acciones == 1:
            color = "yellow"
            comentario = "Bien"
        else:        
            color = "white"
            comentario = "No Encontrado o No aplica"
        self.concepts['Acciones'] = acciones

    def objetivo(self, file_blocks, scratch):
        total = 0
        color = ""
        comentario = "" 
        objetivo = 0
        """verifica si el juego parece acabar."""          
        for script in self.iter_scripts(scratch):
            for name, _, _ in self.iter_blocks(script.blocks):
                if name.find("stop"):
                    total += 1
                    all_scripts = list(self.iter_scripts(scratch))
        if total > 0:
            objetivo = 3
            color = "green"
            comentario = "Excelente"
        else:
            color = "white"
            comentario = "No Encontrado o No aplica"
        self.concepts['Objetivo'] = objetivo

    def mecanica(self, file_blocks, scratch):
        backdropWhenGreenFlag = 0
        spritesHidden = []
        spritesShown = 0
        actions = []
        color = ""
        comentario = "" 
        mecanica = 0
        """Run and return the results of the Mecanica plugin."""          
        all_scripts = list(self.iter_scripts(scratch))
        backdropWhenGreenFlag = self.backdropGreenFlag(all_scripts)
        spritesHidden = self.getHiddenSprites(scratch)
        #ToDo: Check if there are variables and lists and if so check if they are hidden when launched
        actions = self.getActions(spritesHidden, scratch)
        spritesShown = self.getShownSprites(spritesHidden,actions ,scratch)
        #ToDo: Check if there are variables and lists and if so check if they are shown after actions
        if (backdropWhenGreenFlag > 0 
            and len (spritesHidden) > 0
            and spritesShown >0
            and len(actions) > 0):
            color = "green"
            comentario = "Excelente"
            mecanica = 3
        else:
            color = "white"
            comentario = "No Encontrado o No aplica"
        self.concepts['Mecanica'] = mecanica   
 
    def backdropGreenFlag (self, all_scripts):
        """
            Check if a specific backdrop is displayed when green flag
        """
        backdropWhenGreenFlag = 0
        for script in all_scripts:
            if self.script_start_type(script) == self.HAT_GREEN_FLAG:
                for name, _, block in self.iter_blocks(script.blocks):
                    if name == 'switch backdrop to %s':
                        backdropWhenGreenFlag = block.args[0].lower()
                        break
            if backdropWhenGreenFlag != 0:
                break
        return backdropWhenGreenFlag

    def getHiddenSprites (self, scratch):
        """
            Check if there are sprites that are hidden when green flag
        """
        spritesHidden = []
        for sprite in scratch.sprites:
            hide = 0
            wait = 0
            for script in sprite.scripts:
                if not isinstance(script, kurt.Comment):
                    if self.script_start_type(script) == self.HAT_GREEN_FLAG:
                        for name, _, _ in self.iter_blocks(script.blocks):
                            if name == 'hide':
                                spritesHidden.append(sprite)
                                hide = 1
                            elif name == 'wait %s secs' and hide == 1:
                                wait = 1
                            elif name == 'show' and hide == 1 and wait == 1:
                                spritesHidden.remove(sprite)
        return spritesHidden

    def getActions (self,spritesHidden2 ,scratch):
        """
            Find messages sent or backdrops displayed or variables modified
            right after an user action (press key or mouse click)
        """
        spritesHidden = spritesHidden2
        actions = []
        for sprite in scratch.sprites:
            if sprite not in spritesHidden: 
                for script in sprite.scripts:
                    if (self.script_start_type(script) == self.HAT_MOUSE
                        or self.script_start_type(script) == self.HAT_KEY):
                        for name, _, block in self.iter_blocks(script.blocks):
                            if (name == 'switch backdrop to %s' 
                                or name == 'switch backdrop to %s and wait' 
                                or name == 'change %s by %s' 
                                or name == 'set %s to %s' 
                                #or name == 'when %s key pressed' 
                                or name == 'broadcast %s' 
                                or name == 'broadcast %s and wait'):
                                    actions.append(block.args[0].lower())
                    ### para aniadir vars modificadas tras un "si tecla x pulsada"
        for script in scratch.stage.scripts:
            if (self.script_start_type(script) == self.HAT_MOUSE
                or self.script_start_type(script) == self.HAT_KEY):
                for name, _, block in self.iter_blocks(script.blocks):
                    if (name == 'switch backdrop to %s' 
                        or name == 'switch backdrop to %s and wait'
                        or name == 'change %s by %s' 
                        or name == 'set %s to %s' 
                        #or name == 'when %s key pressed' 
                        or name == 'broadcast %s' 
                        or name == 'broadcast %s and wait'):
                            actions.append(block.args[0].lower())
                    elif name =='next backdrop' and self.backdropWhenGreenFlag != 0:
                        backs = []
                        for back in scratch.stage.backgrounds:
                            backs.append(back.name.lower())
                        #print backs
                        if (backs.index(self.backdropWhenGreenFlag) + 1 < len (backs)):
                            actions.append(backs[backs.index(self.backdropWhenGreenFlag) + 1])
                        elif len(backs) > 0:
                            actions.append(backs[0])
        #ToDo: En ocasiones en lugar de "al presionar" se usa un "esperar hasta que tecla x pulsada"
        #ToDo: En ocasiones en lugar de "al hacer click sobre este objeto" se usa un "tocando mouse"
        return actions

    def getShownSprites (self,spritesHidden2 ,actions2 ,scratch):
        """
            Check if there are sprites that are shown after one of the actions
        """
        actions = actions2
        spritesHidden = spritesHidden2
        spritesShown = 0
        for sprite in scratch.sprites:
            if sprite in spritesHidden:
                for script in sprite.scripts:
                    if not isinstance(script, kurt.Comment):
                        if (self.script_start_type(script) == self.HAT_BACKDROP 
                            or self.script_start_type(script) == self.HAT_WHEN_I_RECEIVE
                            or self.script_start_type(script) == self.HAT_KEY):
                            if script.blocks[0].args[0].lower() in actions:
                                for name, _, _ in self.iter_blocks(script.blocks):
                                    if name == 'show':
                                        spritesShown += 1
                                        break
                        #ToDo: comprobar que el show esta despues que la variable
                        elif self.script_start_type(script) == self.HAT_GREEN_FLAG:
                            variableAction = 0
                            show = 0
                            for name, _, block in self.iter_blocks(script.blocks):
                                if name == '%s' and block.args[0].lower() in actions:
                                    variableAction += 1
                                    break
                                elif name == 'show':
                                    spritesShown += 1
                            if variableAction > 0 and show > 0:
                                spritesShown += 1
                        #ToDo: check if clones are created after action, and clones are in turn shown
        return spritesShown

class Dialogos(HairballPlugin):
    """
        Este plugin verifica y cuenta cuantos personajes tienen bloques de dialogo say
        retorna color amarillo si consigue un personaje con say
        retorna color verde claro si consigue dos personajes
        retorna color verde oscuro si consigue tres personajes

        this plugin checks and counts how many characters have blocks of dialog say
        returns color yellow if it finds one character with say
        returns color light green if it finds two character with say
        returns color green if it finds three or more characters with say
    """
    def __init__(self):
        """ el metodo constructor """
        super(Dialogos, self).__init__()
        self.color = ""
        self.comentario = "" 
        self.dialogos = 0

    def analyze(self,scratch):
        """cuenta los bloques say"""
        file_blocks = Counter()
        self.dialogos = 0
        for script in self.iter_scripts(scratch):
            for name, _, _ in self.iter_blocks(script.blocks):
                if not name.find("say"):
                   self.dialogos += 1          
        return 

    def finalize(self):
        if self.dialogos >= 3:
            self.color = "green"
            self.comentario = "Excelente"
        elif self.dialogos == 2:
            self.color = "light green"
            self.comentario = "Muy Bien"
        elif self.dialogos == 1:
            self.color = "yellow"
            self.comentario = "Bien"
        else:        
            self.color = "white"
            self.comentario = "No Encontrado o No aplica"
        print (self.color)
        print (self.comentario)
        print (str(self.dialogos))    
    
class Eventos(HairballPlugin):
    """
        Este plugin verifica y cuenta cuantos eventos bloques de when
        retorna color amarillo si consigue un bloque when
        retorna color verde claro si consigue dos bloques when
        retorna color verde oscuro si consigue tres personajes

        this plugin checks and counts how many characters have blocks of dialog say
        returns color yellow if it finds one character with say
        returns color light green if it finds two character with say
        returns color green if it finds three or more characters with say
    """
    def __init__(self):
        """ el metodo constructor """
        super(Eventos, self).__init__()
        self.color = ""
        self.comentario = "" 
        self.eventos = 0

    def analyze(self,scratch):
        """cuenta los bloques when"""
        file_blocks = Counter()
        for script in self.iter_scripts(scratch):
            for name, _, _ in self.iter_blocks(script.blocks):
                if not name.find("when"):
                   self.eventos += 1  
        return 

    def finalize(self):
        if self.eventos >= 3:
            self.color = "green"
            self.comentario = "Excelente"
        elif self.eventos == 2:
            self.color = "light green"
            self.comentario = "Muy Bien"
        elif self.eventos == 1:
            self.color = "yellow"
            self.comentario = "Bien"
        else:        
            self.color = "white"
            self.comentario = "No Encontrado o No aplica"
        print (self.color)
        print (self.comentario)
        print (str(self.eventos))   

class Puntuacion(HairballPlugin):
    """
        Este plugin verifica y cuenta cuantos personajes tienen bloques de dialogo say
        retorna color amarillo si consigue un personaje con say
        retorna color verde claro si consigue dos personajes
        retorna color verde oscuro si consigue tres personajes

        this plugin checks and counts how many characters have blocks of dialog say
        returns color yellow if it finds one character with say
        returns color light green if it finds two character with say
        returns color green if it finds three or more characters with say
    """
    def __init__(self):
        """ el metodo constructor """
        super(Puntuacion, self).__init__()
        self.color = ""
        self.comentario = "" 
        self.puntuacion = 0

    def analyze(self,scratch):
        """cuenta los bloques change by"""
        file_blocks = Counter()
        for script in self.iter_scripts(scratch):
            for name, _, _ in self.iter_blocks(script.blocks):
                if not name.find("change"):
                   self.puntuacion += 1  
        return 

    def finalize(self):
        if self.puntuacion >= 3:
            self.color = "green"
            self.comentario = "Excelente"
        elif self.puntuacion == 2:
            self.color = "light green"
            self.comentario = "Muy Bien"
        elif self.puntuacion == 1:
            self.color = "yellow"
            self.comentario = "Bien"
        else:        
            self.color = "white"
            self.comentario = "No Encontrado o No aplica"
        print (self.color)
        print (self.comentario)
        print (str(self.puntuacion))   

class Acciones(HairballPlugin):
    """
        Este plugin verifica y cuenta cuantos personajes tienen bloques de dialogo say
        retorna color amarillo si consigue un personaje con say
        retorna color verde claro si consigue dos personajes
        retorna color verde oscuro si consigue tres personajes

        this plugin checks and counts how many characters have blocks of dialog say
        returns color yellow if it finds one character with say
        returns color light green if it finds two character with say
        returns color green if it finds three or more characters with say
    """
    def __init__(self):
        """ el metodo constructor """
        super(Acciones, self).__init__()
        self.color = ""
        self.comentario = "" 
        self.acciones = 0

    def analyze(self,scratch):
        """cuenta los bloques move"""
        file_blocks = Counter()
        for script in self.iter_scripts(scratch):
            for name, _, _ in self.iter_blocks(script.blocks):
                if not name.find("move"):
                   self.acciones += 1  
        return 

    def finalize(self):
        if self.acciones >= 3:
            self.color = "green"
            self.comentario = "Excelente"
        elif self.acciones == 2:
            self.color = "light green"
            self.comentario = "Muy Bien"
        elif self.acciones == 1:
            self.color = "yellow"
            self.comentario = "Bien"
        else:        
            self.color = "white"
            self.comentario = "No Encontrado o No aplica"
        print (self.color)
        print (self.comentario)
        print (str(self.acciones))    

class Objetivo(HairballPlugin):
    """
        Este plugin verifica y cuenta cuantos personajes tienen bloques de dialogo say
        retorna color amarillo si consigue un personaje con say
        retorna color verde claro si consigue dos personajes
        retorna color verde oscuro si consigue tres personajes

        this plugin checks and counts how many characters have blocks of dialog say
        returns color yellow if it finds one character with say
        returns color light green if it finds two character with say
        returns color green if it finds three or more characters with say
    """

    def __init__(self):
        super(Objetivo, self).__init__()
        self.total = 0
        self.color = ""
        self.comentario = "" 
        self.objetivo = 0

    def finalize(self):
        """Output whether the project seems to end or not."""
        if self.total > 0:
            self.objetivo = self.total
            self.color = "green"
            self.comentario = "Excelente"
        else:
            self.color = "white"
            self.comentario = "No Encontrado o No aplica"
        print (self.color)
        print (self.comentario)
        print (str(self.objetivo))      

    def analyze(self, scratch):
        """Run and return the results of the Ending plugin."""          
        for script in self.iter_scripts(scratch):
            for name, _, _ in self.iter_blocks(script.blocks):
                if name.find("stop"):
                    self.total += 1
                    all_scripts = list(self.iter_scripts(scratch))

class Mecanica(HairballPlugin):
    """
        Este plugin verifica y cuenta cuantos personajes tienen bloques de dialogo say
        retorna color amarillo si consigue un personaje con say
        retorna color verde claro si consigue dos personajes
        retorna color verde oscuro si consigue tres personajes

        this plugin checks and counts how many characters have blocks of dialog say
        returns color yellow if it finds one character with say
        returns color light green if it finds two character with say
        returns color green if it finds three or more characters with say
    """

    def __init__(self):
        super(Mecanica, self).__init__()
        self.backdropWhenGreenFlag = 0
        self.spritesHidden = []
        self.spritesShown = 0
        self.actions = []
        self.color = ""
        self.comentario = "" 
        self.mecanica = 0

    def finalize(self):
        """Output whether the project seems to have Mecanica instructions"""
        if (self.backdropWhenGreenFlag > 0 
            and len (self.spritesHidden) > 0
            and self.spritesShown >0
            and len(self.actions) > 0):
            self.color = "green"
            self.comentario = "Excelente"
        else:
            self.color = "white"
            self.comentario = "No Encontrado o No aplica"
        print (self.color)
        print (self.comentario)
        print (str(self.mecanica))      

    def backdropGreenFlag (self, all_scripts):
        """
            Check if a specific backdrop is displayed when green flag
        """
        backdropWhenGreenFlag = 0
        for script in all_scripts:
            if self.script_start_type(script) == self.HAT_GREEN_FLAG:
                for name, _, block in self.iter_blocks(script.blocks):
                    if name == 'switch backdrop to %s':
                        backdropWhenGreenFlag = block.args[0].lower()
                        break
            if backdropWhenGreenFlag != 0:
                break
        return backdropWhenGreenFlag

    def getHiddenSprites (self, scratch):
        """
            Check if there are sprites that are hidden when green flag
        """
        spritesHidden = []
        for sprite in scratch.sprites:
            hide = 0
            wait = 0
            for script in sprite.scripts:
                if not isinstance(script, kurt.Comment):
                    if self.script_start_type(script) == self.HAT_GREEN_FLAG:
                        for name, _, _ in self.iter_blocks(script.blocks):
                            if name == 'hide':
                                spritesHidden.append(sprite)
                                hide = 1
                            elif name == 'wait %s secs' and hide == 1:
                                wait = 1
                            elif name == 'show' and hide == 1 and wait == 1:
                                spritesHidden.remove(sprite)
        return spritesHidden

    def getActions (self, scratch):
        """
            Find messages sent or backdrops displayed or variables modified
            right after an user action (press key or mouse click)
        """
        actions = []
        for sprite in scratch.sprites:
            if sprite not in self.spritesHidden: 
                for script in sprite.scripts:
                    if (self.script_start_type(script) == self.HAT_MOUSE
                        or self.script_start_type(script) == self.HAT_KEY):
                        for name, _, block in self.iter_blocks(script.blocks):
                            if (name == 'switch backdrop to %s' 
                                or name == 'switch backdrop to %s and wait' 
                                or name == 'change %s by %s' 
                                or name == 'set %s to %s' 
                                #or name == 'when %s key pressed' 
                                or name == 'broadcast %s' 
                                or name == 'broadcast %s and wait'):
                                    actions.append(block.args[0].lower())
                    ### para aniadir vars modificadas tras un "si tecla x pulsada"
        for script in scratch.stage.scripts:
            if (self.script_start_type(script) == self.HAT_MOUSE
                or self.script_start_type(script) == self.HAT_KEY):
                for name, _, block in self.iter_blocks(script.blocks):
                    if (name == 'switch backdrop to %s' 
                        or name == 'switch backdrop to %s and wait'
                        or name == 'change %s by %s' 
                        or name == 'set %s to %s' 
                        #or name == 'when %s key pressed' 
                        or name == 'broadcast %s' 
                        or name == 'broadcast %s and wait'):
                            actions.append(block.args[0].lower())
                    elif name =='next backdrop' and self.backdropWhenGreenFlag != 0:
                        backs = []
                        for back in scratch.stage.backgrounds:
                            backs.append(back.name.lower())
                        #print backs
                        if (backs.index(self.backdropWhenGreenFlag) + 1 < len (backs)):
                            actions.append(backs[backs.index(self.backdropWhenGreenFlag) + 1])
                        elif len(backs) > 0:
                            actions.append(backs[0])
        #ToDo: En ocasiones en lugar de "al presionar" se usa un "esperar hasta que tecla x pulsada"
        #ToDo: En ocasiones en lugar de "al hacer click sobre este objeto" se usa un "tocando mouse"
        return actions

    def getShownSprites (self, scratch):
        """
            Check if there are sprites that are shown after one of the actions
        """
        spritesShown = 0
        for sprite in scratch.sprites:
            if sprite in self.spritesHidden:
                for script in sprite.scripts:
                    if not isinstance(script, kurt.Comment):
                        if (self.script_start_type(script) == self.HAT_BACKDROP 
                            or self.script_start_type(script) == self.HAT_WHEN_I_RECEIVE
                            or self.script_start_type(script) == self.HAT_KEY):
                            if script.blocks[0].args[0].lower() in self.actions:
                                for name, _, _ in self.iter_blocks(script.blocks):
                                    if name == 'show':
                                        spritesShown += 1
                                        break
                        #ToDo: comprobar que el show esta despues que la variable
                        elif self.script_start_type(script) == self.HAT_GREEN_FLAG:
                            variableAction = 0
                            show = 0
                            for name, _, block in self.iter_blocks(script.blocks):
                                if name == '%s' and block.args[0].lower() in self.actions:
                                    variableAction += 1
                                    break
                                elif name == 'show':
                                    spritesShown += 1
                            if variableAction > 0 and show > 0:
                                spritesShown += 1
                        #ToDo: check if clones are created after action, and clones are in turn shown
        return spritesShown

    def analyze(self, scratch):
        """Run and return the results of the Mecanica plugin."""          
        all_scripts = list(self.iter_scripts(scratch))
        self.backdropWhenGreenFlag = self.backdropGreenFlag(all_scripts)
        self.spritesHidden = self.getHiddenSprites(scratch)
        #ToDo: Check if there are variables and lists and if so check if they are hidden when launched
        self.actions = self.getActions(scratch)
        self.spritesShown = self.getShownSprites(scratch)
        #ToDo: Check if there are variables and lists and if so check if they are shown after actions

#class Personajes(HairballPlugin):
