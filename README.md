# Monte-Carlo-Simulator
Monte Carlo Simulator DS5100

# Metadata
Name: Victor Teelucksingh
Project Name: Monte Carlo Simulator

# Synopsis
## Install
Clone the repository (https://github.com/VTGH23/Monte-Carlo-Simulator) to your local machine.
Navigate to the directory of the repository within the file structure of your machine, then execute the following code at the command line (assumes you have pip installed) 

```
pip install .
```
You can also try executing the following code using Windows Command Prompt.

```
python -m pip install .
```

## Import
Execute the code below to import the relevant classes from the montecarlo module for use in a .py file or jupyter notebook.

```
from montecarlo import Die
from montecarlo import Game
from montecarlo import Analyzer
import pandas as pd
import numpy as np
```

## Creating dice
Create a Die object with the Die class by passing a numpy array of faces (str or numeric). In this example, we choose a numpy array (str) using the sides of a typical Die.

```
demo_Die_object_1 = Die(np.array(['one','two','three','four','five','six']))
```

A weight array (numeric) is initialized when creating a Die object. By default all weights are 1, but you can change weights for a particular face value using the change_weight() method (see API description for additional detail on all methods for all classes in the package). Change_weight() takes two arguments, the face value whose weight will be changed, and the new weight (numeric).

Below we change the weight of the 'one' face to 5. (Weights for faces 'two','three','four','five','six' remain 1 by default).

```
demo_Die_object_1 = Die(np.array(['one','two','three','four','five','six']))
demo_Die_object_1.change_weight('one',5)
```

You can roll a Die object to generate a random vector of faces based on the current set of weights. The roll() method takes an int for the number of rolls (i.e., expected length of the random vector of faces).

```
print(demo_Die_object_1.roll(5))
```

Use the show_current() method to return a dataframe of the current faces and weights for a particular Die object.

```
print(demo_Die_object_1.show_current())
```

## Playing games

Create a Game object with the Game class by passing a list of already instantiated Die objects.

```
demo_Game_object_1 = Game([Die(np.array(['one','two','three','four','five','six'])),Die(np.array(['one','two','three','four','five','six']))])
```

Similar to the roll() method in the Die class, a Game object can use the play() method to roll each Die and save results in an N rolls x M dice dataframe. The play() method takes an int input for the number of plays.

```
demo_Game_object_1.play(10)
```

You can see results of the most recent play by using the show() method. show() takes an input for the form of the returned dataframe ('wide' or 'narrow' forms).
The narrow form of the dataframe will have a two-column index with the roll number and the die number, and a column for the face rolled.
The wide form of the dataframe will a single column index with the roll number, and each die number as a column.

```
print(demo_Game_object_1.show('wide'))
```

## Analyzing games
Create an Analyzer object with the Analyzer class by passing an already instantiated Game object.

```
demo_Analyzer_object_1 = Analyzer(demo_Game_object_1)
```

Analyzer has a few useful methods that give you additional detail on the results of the Game. The jackpot() method counts how many times all Die faces were rolled the same over the course of the game. It returns an integer and stores results as a dataframe in a public attribute.

```
print(demo_Analyzer_object_1.jackpot())
```

The combo() method computes the distinct combinations of faces rolled, along with their counts. It stores these results as a dataframe in a public attribute.

```
demo_Analyzer_object_1.combo()
print(demo_Analyzer_object_1.combo_results_index)
```

The face_counts_per_roll() method computes how many times a given face is rolled in each event. It stores the results as a dataframe in a public attribute.

```
demo_Analyzer_object_1.face_counts_per_roll()
print(demo_Analyzer_object_1.face_counts_per_roll_results)
```

# API description

## Die Class
"""
    A class to represent a Die in a Monte Carlo simulator

    ...

    Attributes
    ----------
    faces : array (dtype string or numeric)
        Array of die faces
    weights : array (dtype numeric)
        Array of weights associated with each face

    Methods
    -------
    change_weight(face_value, new_weight):
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
    roll(num_rolls=1):
        '''
        PURPOSE: This method rolls the die one or more times.
    
        INPUTS: 
        num_rolls int 
    
        OUTPUT:
        Returns a random sample from the vector of faces according to the weights with specified length.
        '''
    show_current():
        '''
        PURPOSE: This method shows the user the die's current set of faces and weights.
    
        INPUTS: 
        None
    
        OUTPUT:
        Dataframe
        '''
"""

## Game class
"""
    A class to represent a Game in a Monte Carlo simulator

    ...

    Attributes
    ----------
    DieList : list
        List of already instantiated similar Die objects
    game_df_wide : dataframe
        Game results in wide form as an attribute.
    game_df_narrow : dataframe
        Game results in narrow form as an attribute.

    Methods
    -------
    play(num_plays):
        '''
        PURPOSE: This method plays a game (i.e., rolls all of the dice a given number of times)
    
        INPUTS: 
        num_plays int
    
        OUTPUT:
        Saves results to a private dataframe of shape N rolls by M dice
        '''
    show(form='wide')
        '''
        PURPOSE: This method shows the user the results of the most recent play. 
        It passes the private dataframe created in the play method to the user.
    
        INPUTS: 
        form str
    
        OUTPUT:
        Returns a dataframe in narrow or wide form depending on chosen parameter.
        Also creates public attributes for wide and narrow dataframes. 
        '''
"""

## Analyzer class
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
        '''
        PURPOSE: This method computes how many times the game resulted in all faces being identical.
    
        INPUTS: 
        None
    
        OUTPUT:
        Returns an integer for the number of times to the user
        '''
    combo():
        '''
        PURPOSE: This method computes the distinct combinations of faces rolled, along with their counts for a Game.
    
        INPUTS: 
        None
    
        OUTPUT:
        Stores the results as a dataframe in a public attribute. 
        '''
    face_counts_per_roll():
        '''
        PURPOSE: This method computes how many times a given face is rolled in each event for a Game. 
    
        INPUTS: 
        None
    
        OUTPUT:
        Stores the results as a dataframe in a public attribute.
        '''
"""

# Manifest
## Monte-Carlo-Simulator:
* FinalProjectSubmissionTemplate.ipynb
* LICENSE
* README.md
* montecarlo_dir/
* montecarlo_dir.egg-info/
* montecarlo_results.txt
* montecarlo_test.py
* setup.py

## montecarlo_dir:
* \__init__.py
* \___pycache__/
* montecarlo.py

## montecarlo_dir/\__pycache__:
* \__init__.cpython-311.pyc
* montecarlo.cpython-311.pyc

## montecarlo_dir.egg-info:
* PKG-INFO
* SOURCES.txt
* dependency_links.txt
* top_level.txt