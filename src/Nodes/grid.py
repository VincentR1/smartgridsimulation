import numpy as np
from src.Nodes.consumer import Consumer
from src.Nodes.producer import Producer
from src.Nodes.node import Node


class Grid(Node):
    def start(self, step):
        balance_loss = self.get_balance(step)
        self.settle(balance_loss[0], step)
        return balance_loss;

    # gives back (balance,loss)
    def get_balance(self, step: int) -> (float, float):
        external_balances_losses = [n.get_balance(step) for n in self.nodes]
        local_balance = 0
        local_loss = 0
        for i in range(len(self.nodes)):
            external_balance = external_balances_losses[i][0]
            self.external_balance_in_step[i] = external_balance
            transport_eff = self.transport_efficiencies[i]
            if external_balance < 0:
                local_balance = local_balance + external_balance * (2 - transport_eff);
            else:
                local_balance = local_balance + external_balance * transport_eff
            external_loss = external_balances_losses[i][1]
            local_loss = local_loss + external_loss * (2 - transport_eff)
            self.external_loss_in_step[i] = external_loss
        return local_balance, local_loss

    def __init__(self, steps: int, nodes: Node[], transport_efficiencies: float[]):
        self.nodes = nodes
        self.transport_efficiencies = transport_efficiencies
        self.steps = steps
        self.local_balances = [0] * steps
        self.local_losses = [0] * steps
        self.external_demand_in_step = [0] * len(nodes)
        self.external_loss_in_step = [0] * len(nodes)

    ##ToDo: Agam
    ##import graph struckture from node x graph
    def import_graph_from_networkx(self, graph:):
        pass

    ##import graph from text json example in the wiki
    def import_graph_from_file(self, ):
        pass

    def settle(self, step, overflow):
        overflow = overflow
        node_demand_loss = zip(self.nodes, self.external_demand_in_step, self.external_loss_in_step)
        if (overflow < 0):
            nodes_demand_loss_consumers = [ndlc for ndlc in node_demand_loss if ndlc[1] < 0]
            nodes_demand_loss_consumers_sorted = [ndlc for ndlc in node_demand_loss if ndlc[1] < 0].sort(key=lambda
                x: x[2]);
            for ndl in nodes_demand_loss_consumers_sorted:
                if (overflow - ndl[1] <= 0):
                    overflow = overflow - ndl[1]
                    ndl[0].settle(step, overflow);
                elif (overflow - ndl[1] > 0):
                    overflow = 0;
                    ndl[0].settle(step, ndl[1] + overflow);
                if overflow == 0:
                    return;
        elif (overflow > 0)
