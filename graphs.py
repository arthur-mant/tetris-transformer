import matplotlib.pyplot as plt
import numpy as np

def plot_mean_score(mean_scores, episode, name):

    plt.plot(mean_scores[:episode+1])
    plt.title("Pontuação média por episódio de treinamento")
    plt.xlabel("Episódio")
    plt.ylabel("Pontuação Média")
    plt.savefig("graphs/"+name+"mean_score.png")
    plt.close()

def plot_max_score(max_scores, episode, name):

    plt.plot(max_scores[:episode+1])
    plt.title("Pontuação máxima atingida em cada episódio de treinamento")
    plt.xlabel("Episódio")
    plt.ylabel("Pontuação Máxima")
    plt.savefig("graphs/"+name+"max_score.png")
    plt.close()

def plot_accumulated_loss(loss, episode, name):
    plt.plot(loss[:episode+1])
    plt.title("Loss acumulada por episódio de treinamento")
    plt.xlabel("Episódio")
    plt.ylabel("Perda acumulada")
    plt.savefig("graphs/"+name+"loss.png")
    plt.close()

def plot_lines_cleared(lines_cleared, episode, name):
    for i in range(4):
        plt.plot(lines_cleared[i][:episode+1], label = str(i+1))
    plt.title("Quantidade de n linhas completas simultaneamente")
    plt.xlabel("Episódio")
    plt.ylabel("Quantidade")
    plt.legend()
    plt.savefig("graphs/"+name+"line_completion.png")
    plt.close()

