import pandas as pd
import numpy as np
import random

class Die:
    """
    A class to represent a Die in a Monte Carlo simulator

    ...

    Attributes
    ----------
    faces : array (dtype string or numeric)
        Array of die faces
    weights : array (dtype numeric)
        Array of weights associated with each face
    __df : dataframe 
        Private dataframe built from faces and weights arrays

    Methods
    -------
    change_weight(face_value, new_weight):
        Changes the weight of a single side.
    roll(num_rolls=1):
        Rolls the die one or more times.
    show_current():
        Shows the user the die's current set of faces and weights.
    """
    def __init__(self, faces):
        """
        Constructs all the necessary attributes for the Die object.

        INPUTS:
        faces : array (dtype string or numeric)
        """
        self.faces = faces
        self.weights = np.tile(1,len(faces))
        self.__df= pd.DataFrame({'faces':faces, 'weights':self.weights})


    def change_weight(self, face_value, new_weight):
        '''
        PURPOSE: This method changes the weight of a single side.
    
        INPUTS: 
        face_value str or numeric
        new_weight numeric 
    
        OUTPUT:
        Updates weight value to new weight in weights array attribute for a given face.
        Updates weight value to new weight in faces & weights dataframe attribute for a given face.
        Returns error message for invalid face or weight.
        '''
        #Check to see if weight passed is valid
        error_message = None
        try:
            a = float(new_weight)
        except ValueError:
                error_message = "Not a valid weight. Try again"
                return error_message

        #Check to see if face passed is valid
        if (face_value in self.faces):
            i, = np.where(self.faces == face_value)
            my_index = i[0]
            self.__df.loc[my_index,'weights'] = new_weight
            self.weights[my_index] = new_weight
        else:
            error_message = "Please choose a valid face value."
            return error_message

    def roll(self, num_rolls = 1):
        '''
        PURPOSE: This method rolls the die one or more times.
    
        INPUTS: 
        num_rolls int 
    
        OUTPUT:
        Returns a random sample from the vector of faces according to the weights with specified length.
        '''
        randomList = random.choices(self.faces, self.weights, k=num_rolls)
        return randomList

    def show_current(self):
        '''
        PURPOSE: This method shows the user the die's current set of faces and weights.
    
        INPUTS: 
        None
    
        OUTPUT:
        Dataframe
        '''
        return self.__df
    
    
class Game:
    """
    A class to represent a Game in a Monte Carlo simulator

    ...

    Attributes
    ----------
    DieList : list
        List of already instantiated similar Die objects
    __game_df : dataframe
        Private dataframe of shape N rolls by M dice
    game_df_wide : dataframe
        Game results in wide form as an attribute.
    game_df_narrow : dataframe
        Game results in narrow form as an attribute.

    Methods
    -------
    play(num_plays):
        Plays a game (i.e., rolls all of the dice a given number of times)
    show(form='wide')
        Shows the user the results of the most recent play in narrow or wide form.
    """
    def __init__(self, DieList):
        """
        Constructs all the necessary attributes for the Game object.

        INPUTS:
        DieList : list of already instantiated similar Die objects
        """
        self.DieList = DieList

    def play(self, num_plays):
        '''
        PURPOSE: This method plays a game (i.e., rolls all of the dice a given number of times)
    
        INPUTS: 
        num_plays int
    
        OUTPUT:
        Saves results to a private dataframe of shape N rolls by M dice
        '''
        self.__game_df = pd.DataFrame()
        i = 1

        #Build matrix of shape N rolls by M dice
        for c in self.DieList:
            i_str = str(i)
            self.__game_df['Die ' + i_str] = c.roll(num_plays)
            i = i+1

        #Build roll # column and set as index
        game_roll_list = list(range(1,len(self.__game_df['Die 1'])+1))
        self.__game_df['roll #'] = game_roll_list
        self.__game_df = self.__game_df.set_index('roll #')

    def show(self, form = 'wide'):
        '''
        PURPOSE: This method shows the user the results of the most recent play. 
        It passes the private dataframe created in the play method to the user.
    
        INPUTS: 
        form str ('wide' or 'narrow')
    
        OUTPUT:
        Returns a dataframe in narrow or wide form depending on chosen parameter.
        Also creates public attributes for wide and narrow dataframes. 
        '''
        #Build wide and narrow forms as attributes. Return one or the other depending on parameter chosen by user.
        self.game_df_wide = self.__game_df
        self.game_df_narrow = self.game_df_wide.stack()
        if form.lower() == 'wide':
            return self.game_df_wide
        elif form.lower() == 'narrow':
            return self.game_df_narrow
        else:
            return "Not a valid form. Try again."


class Analyzer:
    """
    A class to analyze the results of a single game and compute various descriptive statistics in a Monte Carlo simulator

    ...

    Attributes
    ----------
    Game : Game object
        Already instantiated Game object
    types : str
        String identifying if faces are in string or numeric format
    jackpot_results  : dataframe (Boolean)
        Stored dataframe of jackpot results
    combo_results_sort : dataframe
        Stored dataframe of sorted combo results (wide form)
    combo_results_index : dataframe
        Stored dataframe of sorted combo results (narrow form, multi-columned index)
    face_counts_per_roll_results : dataframe
        Stored dataframe of face counts per roll results (wide form)

    Methods
    -------
    jackpot():
        Computes how many times the game resulted in all faces being identical.
    combo():
        Computes the distinct combinations of faces rolled, along with their counts for a Game.
    face_counts_per_roll():
        Computes how many times a given face is rolled in each event for a Game.
    """
    def __init__(self, Game):
        """
        Constructs all the necessary attributes for the Analyzer object.

        INPUTS:
        Game : Game object
        """
        self.Game = Game
        self.types = None
        
        #Infer the data type of the die faces used. 
        for c in Game.DieList[0].faces:
            if isinstance(c,str):
                self.types = "string"
        if self.types != "string":
            self.types = "numeric"

    def jackpot(self):
        '''
        PURPOSE: This method computes how many times the game resulted in all faces being identical.
    
        INPUTS: 
        None
    
        OUTPUT:
        Returns an integer for the number of times to the user
        '''
        #Check all columns against the first column using eq. 
        #Create a boolean dataframe where True indicates Jackpot and False indicates No Jackpot for each roll.
        self.jackpot_results = self.Game.game_df_wide.eq(self.Game.game_df_wide.iloc[:,0],axis=0).all(1)
        true_count = len(self.jackpot_results[self.jackpot_results == True])
        return true_count
    
    def combo(self):
        '''
        PURPOSE: This method computes the distinct combinations of faces rolled, along with their counts for a Game.
    
        INPUTS: 
        None
    
        OUTPUT:
        Stores the results as a dataframe in a public attribute. 
        '''
        #Group and get value counts
        combo_results = self.Game.game_df_wide.groupby(list(self.Game.game_df_wide.columns.values), as_index=False).value_counts()
        col_list = list(combo_results.columns.values)
        #sort and set multi-index
        self.combo_results_sort = combo_results.sort_values(by=['count'], ascending=False)
        self.combo_results_index = self.combo_results_sort.set_index(col_list[:-1])

    def face_counts_per_roll(self):
        '''
        PURPOSE: This method computes how many times a given face is rolled in each event for a Game. 
    
        INPUTS: 
        None
    
        OUTPUT:
        Stores the results as a dataframe in a public attribute.
        '''
        #Apply value_counts() to each row of the wide view game
        face_counts_per_roll_results_1 = self.Game.game_df_wide.apply(pd.value_counts, axis=1)
        self.face_counts_per_roll_results = face_counts_per_roll_results_1.replace(np.nan,0)
