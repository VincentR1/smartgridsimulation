from abc import ABC

import numpy as np
from src.Nodes.consumer import Consumer
from src.Nodes.producer import Producer
from src.Nodes.node import Node


class Grid(Node):
    def start(self, step):
        balance_loss = self.get_balance(step)
        result = self.start_settling(step, balance_loss[0])
        return result

    # gives back (balance,loss)
    def get_balance(self, step: int) -> (float, float, float):
        external_balances_losses_mineff = [n.get_balance(step) for n in self.nodes]
        min_eff_consumer_producer = [1, 1]
        for i in range(len(self.nodes)):
            ## calculating balance
            external_balance = external_balances_losses_mineff[i][0]
            transport_eff = self.transport_efficiencies[i]
            min_eff = transport_eff * external_balances_losses_mineff[i][2]

            if external_balance < 0:
                external_balance_after_transport = external_balance / transport_eff
                loss_on_link = -external_balance_after_transport + external_balance
                if min_eff < min_eff_consumer_producer[0]:
                    min_eff_consumer_producer[0] = min_eff
            else:
                external_balance_after_transport = external_balance * transport_eff
                loss_on_link = external_balance - external_balance_after_transport
                if min_eff < min_eff_consumer_producer[0]:
                    min_eff_consumer_producer[1] = min_eff

            self.local_balances[step] += external_balance_after_transport;
            external_loss_after_transport = loss_on_link + external_balances_losses_mineff[i][1]
            self.local_losses[step] += external_loss_after_transport

            self.unsetteld_nodes_eff_balance_loss_mineff.append((self.nodes[i], transport_eff,
                                                                 external_balance_after_transport,
                                                                 external_loss_after_transport, min_eff))

        self.min_eff = min_eff_consumer_producer[self.local_balances[step] > 0]
        return self.local_balances[step], self.local_losses[step], self.min_eff

    def __init__(self, steps: int, nodes, transport_efficiencies):
        self.nodes = nodes
        self.transport_efficiencies = transport_efficiencies
        self.steps = steps
        self.local_balances = [0] * steps
        self.local_losses = [0] * steps
        self.min_eff = 1
        self.unsetteld_nodes_eff_balance_loss_mineff = []

    ##ToDo: Agam
    ##import graph struckture from node x graph
    def import_graph_from_networkx(self, graph):
        pass

    ##import graph from text json example in the wiki
    def import_graph_from_file(self, ):
        pass

    ##Adding one node to a Grid
    def adding_node(self, node: Node, transport_eff: float):
        self.nodes.app

    def start_settling(self, step, overflow):
        overflow = overflow
        while overflow < 0:
            result = self.settle(step, overflow)
            overflow -= result[0]
        return result;

    def settle(self, step, overflow):
        overflow = overflow
        ##underproduction
        if overflow < 0:
            consumers_eff_demand_loss_mineff = [ndlc for ndlc in self.unsetteld_nodes_eff_balance_loss_mineff if
                                                ndlc[2] < 0]
            print([a[2] for a in consumers_eff_demand_loss_mineff])
            consumers_eff_demand_loss_mineff.sort(
                key=lambda x: x[3])
        consumer, transport_eff, external_balance, external_loss, local_min_eff = consumers_eff_demand_loss_mineff.pop()
        self.unsetteld_nodes_eff_balance_loss_mineff.remove(
            (consumer, transport_eff, external_balance, external_loss, local_min_eff))

        return_flow, updated_external_balance, updated_external_loss, updated_mineff, settled = consumer.settle(step,
                                                                                                                overflow * transport_eff)

        if not settled:
            self.unsetteld_nodes_eff_balance_loss_mineff.append((consumer, transport_eff,
                                                                 updated_external_balance / transport_eff,
                                                                 updated_external_loss, updated_mineff * transport_eff))

        # updating local values
        return_flow_after_transport = return_flow / transport_eff
        self.local_balances[step] -= overflow - return_flow_after_transport
        self.local_losses[step] -= (transport_eff - 1) * (
                return_flow_after_transport - overflow) - external_loss + updated_external_loss

        if consumers_eff_demand_loss_mineff:
            external_min_eff_after_transport = [neblm[1] for neblm in self.unsetteld_nodes_eff_balance_loss_mineff]
            self.min_eff = min(external_min_eff_after_transport)
            return_settled = False
        else:
            self.min_eff = 1
            return_settled = True

        return return_flow_after_transport, self.local_balances[step], self.local_losses[
            step], self.min_eff, return_settled
