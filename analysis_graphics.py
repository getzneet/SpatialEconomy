from pylab import plt, np
from os import path, mkdir

from save.import_data import import_data


class GraphProportionChoices(object):
    def __init__(self):

        pass

    @classmethod
    def plot(cls, suffix, multi=0):

        parameters, direct_exchange, indirect_exchange = import_data(suffix=suffix)

        if multi:

            nb_list = len(direct_exchange)
            t_max = len(direct_exchange[0])

            agents_proportions = np.zeros((t_max, 3))

            for i in range(nb_list):

                for k in range(t_max):

                    for j in range(3):
                        agents_proportions[k, j] = direct_exchange[i][k][j]

                cls.draw(agents_proportions=agents_proportions, t_max=t_max, suffix=suffix)
        else:

            t_max = len(direct_exchange)

            agents_proportions = np.zeros((t_max, 3))

            for i in range(t_max):

                for j in range(3):
                    agents_proportions[i, j] = direct_exchange[i][j]

            cls.draw(agents_proportions=agents_proportions, t_max=t_max, suffix=suffix)

    @classmethod
    def draw(cls, t_max, agents_proportions, suffix):

        color_set = ["green", "blue", "red"]

        for agent_type in range(3):
            plt.plot(np.arange(t_max), agents_proportions[:, agent_type],
                     color=color_set[agent_type], linewidth=2.0)

            plt.ylim([-0.1, 1.1])

        # plt.suptitle('Direct choices proportion per type of agents', fontsize=14, fontweight='bold')
        # plt.legend(loc='lower left', frameon=False)

        if not path.exists("../figures"):
            mkdir("../figures")

        plt.savefig("../figures/figure_{}.pdf".format(suffix))
        plt.show()
