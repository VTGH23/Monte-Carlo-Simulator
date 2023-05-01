from montecarlo import Die
from montecarlo import Game
from montecarlo import Analyzer
import pandas as pd
import numpy as np
import unittest

class DieTestSuite(unittest.TestCase):
    """
    Tests methods in the Die class in a Monte Carlo simulator. 
    """
    def test_1_change_weight(self):
        """
        Test a valid weight change for a valid face.
        """ 
        test_1_object = Die(np.array(['one','two','three','four','five','six']))
        test_1_object.change_weight("one", 100)
        
        self.assertTrue((test_1_object.df.loc[test_1_object.df['faces'] == 'one', 'weights'].iloc[0])==100)

    def test_2_change_weight(self):
        """
        Test an invalid weight change for a valid face.
        """  
        test_2_object = Die(np.array(['one','two','three','four','five','six']))

        self.assertTrue(test_2_object.change_weight("one", 'one hundred') == "Not a valid weight. Try again")

    def test_3_change_weight(self): 
        """
        Test a valid weight change for a invalid face.
        """  
        test_3_object = Die(np.array(['one','two','three','four','five','six']))

        self.assertTrue(test_3_object.change_weight("seven", 100) == "Please choose a valid face value.")

    def test_4_roll(self):
        """
        Test length of returned list equals number of rolls specified.
        """
        test_4_object = Die(np.array(['one','two','three','four','five','six']))
        
        self.assertTrue(len(test_4_object.roll(num_rolls=10))==10)

    def test_5_roll(self):
        """
        Test that all faces in randomized roll list are a subset of the initialized faces array.
        """
        test_5_object = Die(np.array(['one','two','three','four','five','six']))
        test_5_list = test_5_object.roll(num_rolls=10)
        test_5_faces_list = list(test_5_object.faces)
        self.assertTrue(set(test_5_list).issubset(set(test_5_faces_list)))

    def test_6_show_current(self):
        """
        Test of show_current method returns the df dataframe attribute as specified.
        """        
        test_6_object = Die(np.array(['one','two','three','four','five','six']))
        
        self.assertTrue(test_6_object.show_current().equals(test_6_object.df))

    def test_7_show_current(self):
        """
        Test if show_current method correctly returns the updated df dataframe attribute after a weight change.
        """     
        test_7_object = Die(np.array(['one','two','three','four','five','six']))
        test_7_object.change_weight("one", 100)

        self.assertTrue(test_7_object.show_current().equals(test_7_object.df))

class GameTestSuite(unittest.TestCase):
    """
    Tests methods in the Game class in a Monte Carlo simulator. 
    """
    def test_8_play(self):
        """
        Test if private dataframe created is of shape N rolls by M dice.
        The public attribute for the wide dataframe created in the show method is equivalent to the private dataframe created in the play method.
        It is sufficient to perform this test using this public attribute. 
        """  
        test_8_object = Game([Die(np.array(['one','two','three','four','five','six'])),Die(np.array(['one','two','three','four','five','six']))])
        test_8_object.play(8)
        test_8_object.show(form='wide')
        self.assertTrue(test_8_object.game_df_wide.shape == (8,2))

    def test_9_play(self):
        """
        Test all values in private dataframe exist in the Die faces list.
        The public attribute for the wide dataframe created in the show method is equivalent to the private dataframe created in the play method.
        It is sufficient to perform this test using this public attribute. 
        """  
        test_9_object = Game([Die(np.array(['one','two','three','four','five','six'])),Die(np.array(['one','two','three','four','five','six']))])
        test_9_object.play(8)
        test_9_object.show(form='wide')        
        
        test_9_list = test_9_object.game_df_wide.stack().tolist()
        test_9_faces_list = ['one','two','three','four','five','six']
        self.assertTrue(set(test_9_list).issubset(set(test_9_faces_list)))

    def test_10_show(self):
        """
        Test if show method returns error message if invalid form is passed as parameter.
        """   
        test_10_object = Game([Die(np.array(['one','two','three','four','five','six'])),Die(np.array(['one','two','three','four','five','six']))])
        test_10_object.play(8)
        
        self.assertTrue(test_10_object.show(form='invalid')=="Not a valid form. Try again.")            

    def test_11_show(self):
        """
        Test expected dimensions of wide form.
        """ 
        test_11_object = Game([Die(np.array(['one','two','three','four','five','six'])),Die(np.array(['one','two','three','four','five','six']))])
        test_11_object.play(8)
        test_11_object.show(form = 'wide')

        self.assertTrue(test_11_object.game_df_wide.shape == (8,2))

    def test_12_show(self):
        """
        Test expected dimensions of narrow form.
        """ 
        test_12_object = Game([Die(np.array(['one','two','three','four','five','six'])),Die(np.array(['one','two','three','four','five','six']))])
        test_12_object.play(8)
        test_12_object.show(form = 'narrow')

        self.assertTrue(test_12_object.game_df_narrow.shape == (16,))

class AnalyzerTestSuite(unittest.TestCase):
    """
    Tests methods in the Analyzer class in a Monte Carlo simulator. 
    """
    def test_13_jackpot(self):
        """
        Test jackpot works as expected with test Game data (three jackpots expected).
        """  
        test_13_object = Game([Die(np.array(['one','two','three','four','five','six'])),Die(np.array(['one','two','three','four','five','six']))])
        test_13_object.play(3)
        test_13_object.show(form = 'narrow')
        test_data_13 = {'col1': ['one','two','three'], 'col2': ['one','two','three']}
        test_13_object.game_df_wide = pd.DataFrame(data=test_data_13)

        test_13_analyzer_object = Analyzer(test_13_object)

        self.assertTrue(test_13_analyzer_object.jackpot()==3)

    def test_14_jackpot(self): 
        """
        Test jackpot works as expected with test Game data (zero jackpots expected).
        """  
        test_14_object = Game([Die(np.array(['one','two','three','four','five','six'])),Die(np.array(['one','two','three','four','five','six']))])
        test_14_object.play(3)
        test_14_object.show(form = 'wide')
        test_Game_data_14 = {'col1': ['two','three','one'], 'col2': ['one','two','three']}
        test_14_object.game_df_wide = pd.DataFrame(data=test_Game_data_14)

        test_14_analyzer_object = Analyzer(test_14_object)

        self.assertTrue(test_14_analyzer_object.jackpot()==0)

    def test_15_combo(self):
        """
        Test combo method works as expected with test Game data
        """   
        test_15_object = Game([Die(np.array(['one','two','three','four','five','six'])),Die(np.array(['one','two','three','four','five','six']))])
        test_15_object.play(3)
        test_15_object.show(form = 'wide')
        test_Game_data_15 = {'Die 1': ['two','two','one'], 'Die 2': ['two','two','three']}
        test_15_object.game_df_wide = pd.DataFrame(data=test_Game_data_15)

        test_expected_result_15_list = {'Die 1': ['two','one'], 'Die 2': ['two','three'], 'count': [2, 1]} 
        test_expected_result_15_df = pd.DataFrame(data=test_expected_result_15_list)
        test_expected_result_15_df_indexed = test_expected_result_15_df.set_index(['Die 1', 'Die 2'])

        test_15_analyzer_object = Analyzer(test_15_object)
        test_15_analyzer_object_combo = test_15_analyzer_object.combo()

        self.assertTrue(test_15_analyzer_object.combo_results_index.equals(test_expected_result_15_df_indexed))
    

    def test_16_combo(self):
        """
        Test combo method works as expected with different test Game data. Also includes testing for sorting requirement.
        """    
        test_16_object = Game([Die(np.array(['one','two','three','four','five','six'])),Die(np.array(['one','two','three','four','five','six']))])
        test_16_object.play(5)
        test_16_object.show(form = 'wide')
        test_Game_data_16 = {'Die 1': ['one','one','three','two','two',], 'Die 2': ['one','one','four','two','two']}
        test_16_object.game_df_wide = pd.DataFrame(data=test_Game_data_16)

        test_expected_result_16_list = {'Die 1': ['one','two','three'], 'Die 2': ['one','two','four'], 'count': [2,2,1]} 
        test_expected_result_16_df = pd.DataFrame(data=test_expected_result_16_list)
        test_expected_result_16_df_indexed = test_expected_result_16_df.set_index(['Die 1', 'Die 2'])

        test_16_analyzer_object = Analyzer(test_16_object)
        test_16_analyzer_object.combo()

        self.assertTrue(test_16_analyzer_object.combo_results_index.equals(test_expected_result_16_df_indexed))

    def test_17_face_counts_per_roll(self):
        """
        Test face_counts_per_roll method works as expected with test Game data.
        """    
        test_17_object = Game([Die(np.array(['one','two','three','four','five','six'])),Die(np.array(['one','two','three','four','five','six'])),Die(np.array(['one','two','three','four','five','six']))])
        test_17_object.play(5)
        test_17_object.show(form = 'wide')
        test_Game_data_17 = {'Die 1': ['one','five','six','one','six'], 
                             'Die 2': ['four','one','five','two','two'],
                             'Die 3': ['four','two','three','six','one'],
                             'roll #': [1,2,3,4,5]}
        test_17_object.game_df_wide = pd.DataFrame(data=test_Game_data_17)
        test_17_object.game_df_wide = test_17_object.game_df_wide.set_index('roll #')

        test_expected_result_17_list = {'five': [0.0,1.0,1.0,0.0,0.0], 'four': [2.0,0.0,0.0,0.0,0.0], 'one': [1.0,1.0,0.0,1.0,1.0],
                                        'six': [0.0,0.0,1.0,1.0,1.0], 'three': [0.0,0.0,1.0,0.0,0.0], 'two': [0.0,1.0,0.0,1.0,1.0],
                                        'roll #': [1,2,3,4,5]} 
        test_expected_result_17_df = pd.DataFrame(data=test_expected_result_17_list)
        test_expected_result_17_df_indexed = test_expected_result_17_df.set_index(['roll #'])
        
        test_17_analyzer_object = Analyzer(test_17_object)
        test_17_analyzer_object.face_counts_per_roll()

        self.assertTrue(test_17_analyzer_object.face_counts_per_roll_results.equals(test_expected_result_17_df_indexed))

    def test_18_face_counts_per_roll(self):
        """
        Test face_counts_per_roll method works as expected with different test Game data
        """ 
        test_18_object = Game([Die(np.array(['one','two','three','four','five','six'])),Die(np.array(['one','two','three','four','five','six'])),Die(np.array(['one','two','three','four','five','six'])),
                               Die(np.array(['one','two','three','four','five','six'])),Die(np.array(['one','two','three','four','five','six'])),Die(np.array(['one','two','three','four','five','six'])),
                               Die(np.array(['one','two','three','four','five','six'])),Die(np.array(['one','two','three','four','five','six'])),Die(np.array(['one','two','three','four','five','six']))])
        test_18_object.play(3)
        test_18_object.show(form = 'wide')
        test_Game_data_18 = {'Die 1': ['one','five','six'], 
                             'Die 2': ['four','one','five'],
                             'Die 3': ['four','two','three'],
                             'Die 4': ['five','six','two'],
                             'Die 5': ['one','three','five'],
                             'Die 6': ['six','two', 'one'],
                             'Die 7': ['five','five','three'],
                             'Die 8': ['one', 'four','four'],
                             'Die 9': ['six', 'three', 'five'],
                             'roll #': [1,2,3]}
        test_18_object.game_df_wide = pd.DataFrame(data=test_Game_data_18)
        test_18_object.game_df_wide = test_18_object.game_df_wide.set_index('roll #')

        test_expected_result_18_list = {'five': [2.0,2.0,3.0], 'four': [2.0,1.0,1.0], 'one': [3.0,1.0,1.0],
                                        'six': [2.0,1.0,1.0], 'three': [0.0,2.0,2.0], 'two': [0.0,2.0,1.0],
                                        'roll #': [1,2,3]} 
        test_expected_result_18_df = pd.DataFrame(data=test_expected_result_18_list)
        test_expected_result_18_df_indexed = test_expected_result_18_df.set_index(['roll #'])
        
        test_18_analyzer_object = Analyzer(test_18_object)
        test_18_analyzer_object.face_counts_per_roll()

        self.assertTrue(test_18_analyzer_object.face_counts_per_roll_results.equals(test_expected_result_18_df_indexed))

if __name__ == '__main__':
    unittest.main(verbosity=3)