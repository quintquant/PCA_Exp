# pca_machine.py

''' Code contains the class which performs PCA and returns principal 
components, scores and other information
'''

# libraries
import numpy as np
import matplotlib.pyplot as plt


class PCAMachine:
    r''' Class which holds the functions and variables used in PCA of 
    experimental data
    '''

    def __init__(self, data_handler):
        self.pc_scores = []
        self.pc_curves = []
        self.pc_av = []
        self.pc_sing = []
        self.pc_z = []
        self.data_handler = data_handler

    def print_pca_representation(self):
        sing_total = np.sum(self.pc_sing[-1])
        sing_show = self.pc_sing[-1][:8] * 100 / sing_total
        
        print(str(int(sing_show[0])) + '%', '^')
        for i in range(10):
            print('    |', end='\t')
            for s_j in sing_show:
                if s_j / sing_show[0] < (10 - i) / 10:
                    print(' ', end='\t')
                else:
                    print('#', end='\t')
            print()
        print('    ---------------------------------------------' +
                    '-------------------->')


    def perform_pca(self, prep_ind = 0):
        data_hand = self.data_handler
        a = data_hand.prepared_data[prep_ind][0]
        av = np.sum(a, axis = 1)[np.newaxis].T / a.shape[1]
        z = a - av

        print('Performing PCA on prepared data')
        curves, sing, _ = np.linalg.svd(z)
        scores = np.dot(curves.T, z)

        print('Showing the percentage of covariance of most important PCs:')

        self.pc_scores.append(scores)
        self.pc_curves.append(curves)
        self.pc_av.append(av)
        self.pc_sing.append(sing)
        self.pc_z.append(z)

        self.print_pca_representation()

    def show_pca_results_1(self, param1, param2, res_idx=0, prep_idx=0):

        x = self.data_handler.prepared_data[prep_idx][1][:,0]
     
        fig1 = plt.figure(1, figsize=[12, 12], dpi=100)
        
        plt.subplot(221)
        plt.title('PC curves')
        plt.plot(x, self.pc_curves[res_idx][:,0], '-o', label='1st PC')
        plt.plot(x, self.pc_curves[res_idx][:,1], '-o', label='2nd PC')
        plt.plot(x, self.pc_curves[res_idx][:,2], '-o', label='3rd PC')
        plt.plot(x, self.pc_curves[res_idx][:,3], '-o', label='4th PC')
        plt.legend()
        plt.xlabel('x')
        plt.ylabel('PC vectors')

        plt.subplot(222)
        plt.title('Scree plot')
        sing_norm = 100 * self.pc_sing[res_idx] / np.sum(self.pc_sing[res_idx])
        plt.plot(np.arange(1, sing_norm.size+1), sing_norm, '-sk')
        plt.xlabel('PC no.')
        plt.ylabel('Covariance captured [%]')

        plt.subplot(223)
        plt.title('PC1 vs PC2 (param1)')
        plt.scatter(self.pc_scores[res_idx][0,:], 
                    self.pc_scores[res_idx][1,:],
                    c=param1)
        cbar = plt.colorbar(shrink=0.5, pad = 0, fraction=0.08)
        plt.xlabel('PC1 score')
        plt.ylabel('PC2 score')

        plt.subplot(224)
        plt.title('PC1 vs PC2 (param1)')
        plt.scatter(self.pc_scores[res_idx][0,:], 
                    self.pc_scores[res_idx][1,:],
                    c=param2)
        cbar = plt.colorbar(shrink=0.5, pad = 0, fraction=0.08)
        plt.xlabel('PC1 score')
        plt.ylabel('PC2 score')

        plt.tight_layout()
        plt.show()
        
        

        




    