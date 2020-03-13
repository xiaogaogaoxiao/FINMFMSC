import numpy as np
import time

def incal(data,G,F,r,Tmax):
    W2 = np.square(data.W)
    delta_measure = 1
    iter_max = round(Tmax/delta_measure)+1 
    secu = 1e-12
    T       = np.empty(shape=(iter_max+1))
    T.fill(np.nan)
    RMSE    = np.empty(shape=(2,iter_max+1))
    RMSE.fill(np.nan)
    delta_G = G
    delta_F = F
    t = time.time()
    T[0]=time.time()-t
    RMSE[:,0] = np.linalg.norm(F[:,0:-1]-data.F[:,0:-1],2,axis=1)/np.sqrt(F.shape[1]-1)
    i=0
    while(time.time()-t <= Tmax+delta_measure):
        
        # Updating G
        np.put(delta_G,data.idxOG,0)
        delta_G = np.divide(
            np.multiply(
                delta_G,
                np.dot(
                    np.multiply(
                        W2,
                        secu_plus(data.X-data.Phi_G.dot(F),secu)
                    ),
                    F.T
                )
            ),
            np.dot(
                np.multiply(
                    W2,
                    delta_G.dot(F)
                ),
                F.T
            )
        )
        delta_G[np.isnan(delta_G)] = 0
        G = delta_G
        np.put(G,data.idxOG,data.sparsePhi_G)

        # Updating F 
        np.put(F,data.idxOF,0)
        delta_F = np.divide(
            np.multiply(
                delta_F,
                np.dot(
                    G.T,
                    np.multiply(
                        W2,
                        secu_plus(data.X-G.dot(data.Phi_F),secu)
                    )
                )
            ),
            np.dot(
                G.T,
                np.multiply(
                    W2,
                    G.dot(delta_F)
                )
            )
        )
        delta_F[np.isnan(delta_F)] = 0
        F = delta_F
        np.put(F,data.idxOF,data.sparsePhi_F)

        # Saving results for this iteration
        if time.time()-t - i*delta_measure >= delta_measure:
            i = i+1
            RMSE[:,i] = np.linalg.norm(F[:,0:-1]-data.F[:,0:-1],2,axis=1)/np.sqrt(F.shape[1]-1)
            T[i] = time.time()-t
            # if i%100==0:
            #     print(str(i)+'   '+str(RMSE[0,i])+'   '+str(RMSE[1,i]))
    # return {'G' : G, 'F' : F, 'RMSE' : RMSE, 'T': T}
    return {'RMSE' : RMSE, 'T': T}

def secu_plus(tutu,s):
    toto = np.maximum(tutu,s)
    toto[np.isnan(tutu)] = 0
    return toto