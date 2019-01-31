class Analysis():

    def __init__(self, filename):
        self.flnm = filename



    def data_prep(self):
        df = pd.read_pickle(f'pickles/{self.flnm}')
        

    