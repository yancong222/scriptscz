"""yan cong lm_sent.py
"""
import turicreate
import os
os.getcwd()

sf = turicreate.SFrame('...')

pdtb_relations = ['pdtb.adjacent.comparison.3f.scaled', 'pdtb.adjacent.contingency.4f.scaled', 
                  'pdtb.adjacent.expansion.5f.scaled', 'pdtb.adjacent.temporal.2f.scaled', 
                  'pdtb.adjacent.norel.scaled', 'pdtb.adjacent.entrel.scaled']

nlp = ['loss_sum', 'loss_min', 'loss_max', 'word_count',
               'pdtb.adjacent.comparison.3f.scaled', 'pdtb.adjacent.contingency.4f.scaled', 
                  'pdtb.adjacent.expansion.5f.scaled', 'pdtb.adjacent.temporal.2f.scaled', 
                  'pdtb.adjacent.norel.scaled', 'pdtb.adjacent.entrel.scaled']

groupin = ['1', '2']
sf_2group = sf[sf['group'].is_in(groupin)]

#sf_2group.show()
In [9]:
taskin = ['..', '..']
freespeech = sf_2group[sf_2group['task'].is_in(taskin)]

train_data, test_data = freespeech.random_split(.8,seed=0)

norel_model_freespeech = turicreate.logistic_classifier.create(train_data, 
                                                              target = 'group', 
                                                              features = norel,
                                                             validation_set = test_data)
norel_model_freespeech.evaluate(test_data)
