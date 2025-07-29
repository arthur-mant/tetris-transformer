import matplotlib.pyplot as plt
import numpy as np

def plot_mean_score(mean_scores, episode):

    plt.plot(mean_scores[:episode])
    plt.title("Pontuação média por episódio de treinamento")
    plt.xlabel("Episódio")
    plt.ylabel("Pontuação Média")
    plt.savefig("graphs/mean_score.png")
    plt.close()

def plot_max_score(max_scores, episode):

    plt.plot(max_scores[:episode])
    plt.title("Pontuação máxima atingida em cada episódio de treinamento")
    plt.xlabel("Episódio")
    plt.ylabel("Pontuação Máxima")
    plt.savefig("graphs/max_score.png")
    plt.close()

def plot_accumulated_loss(loss, episode):
    plt.plot(loss[:episode])
    plt.title("Loss acumulada por episódio de treinamento")
    plt.xlabel("Episódio")
    plt.ylabel("Perda acumulada")
    plt.savefig("graphs/loss.png")
    plt.close()

def plot_lines_cleared(lines_cleared, episode):
    for i in range(4):
        plt.plot(lines_cleared[i][:episode], label = str(i+1))
    plt.title("Quantidade de n linhas completas simultaneamente")
    plt.xlabel("Episódio")
    plt.ylabel("Quantidade")
    plt.legend()
    plt.savefig("graphs/line_completion.png")
    plt.close()

