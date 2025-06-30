import matplotlib.pyplot as plt
import numpy as np

def plot_mean_score(mean_scores):

    plt.plot(mean_scores)
    plt.title("Pontuação média por episódio de treinamento")
    plt.xlabel("Episódio")
    plt.ylabel("Pontuação Média")
    plt.savefig("graphs/mean_score.png")

def plot_max_score(max_scores):

    plt.plot(max_scores)
    plt.title("Pontuação máxima atingida em cada episódio de treinamento")
    plt.xlabel("Episódio")
    plt.ylabel("Pontuação Máxima")
    plt.savefig("graphs/max_score.png")

def plot_accumulated_loss(loss):
    plt.plot(loss)
    plt.title("Loss acumulada por episódio de treinamento")
    plt.xlabel("Episódio")
    plt.ylabel("Perda acumulada")
    plt.savefig("graphs/loss.png")
