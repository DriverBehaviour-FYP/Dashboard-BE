import pickle


def load(model_name, pca, no_pca_comp, no_classes, scaler):
    # Load the scaler, PCA, and model using pickle
    if pca is True and scaler is True:
        with open(f'app/main/models/{model_name}/{model_name}-pca-{no_pca_comp}-classes-{no_classes}.pkl', 'rb') as file:
            model = pickle.load(file)
        with open(f'app/main/models/{model_name}/{model_name}-pca-{no_pca_comp}-classes-{no_classes}-scaler.pkl', 'rb') as file:
            scaler = pickle.load(file)
        with open(f'app/main/models/{model_name}/{model_name}-pca-{no_pca_comp}-classes-{no_classes}-PCA.pkl', 'rb') as file:
            pca = pickle.load(file)
        return model, scaler, pca
    
def loadKmeans(pca, scaler):
    # Load the scaler, PCA, and model using pickle
    if pca is True and scaler is True:
        with open(f'app/main/models/k-means/k-means.pkl', 'rb') as file:
            model = pickle.load(file)
        with open(f'app/main/models/k-means/standard_scaler.pkl', 'rb') as file:
            scaler = pickle.load(file)
        with open(f'app/main/models/k-means/pca.pkl', 'rb') as file:
            pca = pickle.load(file)
        return model, scaler, pca
